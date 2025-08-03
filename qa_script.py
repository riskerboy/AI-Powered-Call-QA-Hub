import pandas as pd
import os
import urllib.request
import requests
from datetime import datetime
from openai import OpenAI

# Configuration
EXCEL_FILE = "call_center_data.xlsx"
OUTPUT_FILE = "call_center_qa_results.xlsx"
OPENAI_API_KEY = "your-openai-api-key-here"  # Replace with your OpenAI API key
DEEPGRAM_API_KEY = "your-deepgram-api-key-here"  # Replace with your Deepgram API key

# Check for openpyxl
try:
    import openpyxl
except ImportError:
    print("Error: 'openpyxl' is not installed. Run 'pip install openpyxl' and try again.")
    exit()

# Check for requests
try:
    import requests
except ImportError:
    print("Error: 'requests' is not installed. Run 'pip install requests' and try again.")
    exit()

# Initialize OpenAI client
try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Error: Failed to initialize OpenAI client - {str(e)}. Check your API key.")
    exit()

# Deepgram headers
deepgram_headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}

# Enhanced, structured QA prompt for OpenAI evaluation
QA_PROMPT = """
You are a rockstar QA executive for a call center evaluating a Final Expense campaign call. Speaker 1 is the dialer (agent), and Speaker 2 is the customer. Analyze the transcription and customer name, then provide a concise one-line review (max 100 words) based on the following criteria:

### Evaluation Criteria
1. **DNC Status**: Is this a Do Not Call (DNC) situation? Check if the customer explicitly states they are on a Do Not Call list.
2. **Customer Tone**: Describe the customer's tone—too polite (overly agreeable, possibly insincere), abusive (hostile, rude), frustrated, neutral, etc.
3. **No Call List Mention**: Did the customer say they were supposed to be on a no-call list? Quote any relevant statement.
4. **DNC Indicators**: If the customer says "sounds good," "I suppose," or "correct," flag as potential DNC, but analyze context (e.g., genuine interest vs. dismissal).
5. **Pushiness**: Is the dialer overly pushy, aggressive, or interrupting the customer? Assess if the approach is respectful.
6. **Licensed Agent Request**: If the customer says, "I want to talk to the licensed agent, please transfer me," flag as DNC.
7. **Multiple Calls Complaint**: If the customer mentions "I got several calls" or similar, flag as DNC due to prior unwanted contact.
8. **Customer Name Accuracy**: Is the customer name valid? Check if it’s abusive, inappropriate (e.g., slur, joke), or blank.
9. **Dialer Conduct**: Is the dialer’s mic muted when not speaking? Does the dialer speak only in English (no Urdu or other languages)? If not, reject the call and dock the closer.
10. **Professionalism**: Is the dialer polite, clear, and professional in tone and delivery?
11. **Compliance**: Does the dialer follow the Final Expense campaign script and legal standards (e.g., identify themselves, respect DNC requests)?
12. **Effectiveness**: Does the dialer address customer needs and move toward a sale without overstepping?

### Output Format
Provide a one-line review summarizing:
- DNC status (e.g., "DNC flagged" or "No DNC issue")
- Key findings (tone, name accuracy, dialer conduct, etc.)
- Call outcome (e.g., "Approved" or "Call rejected, dock closer")

Example: "DNC flagged: Customer (valid name) with frustrated tone said 'I got several calls' and 'on no-call list'; dialer not pushy, used English, professional, but prior contact violates DNC—call rejected, dock closer."

### Input
- Transcription: {transcription}
- Customer Name: {customer_name}
"""

def setup_excel():
    # Create sample Excel file if it doesn't exist
    if not os.path.exists(EXCEL_FILE):
        data = {
            "Name": ["Your Agent Name"],  # Replace with real customer name
            "Campaign": ["Final Expense"],
            "Serial Number": ["CALL-001"],
            "Date": [datetime.now().strftime("%Y-%m-%d")],
            "Recording Link": [
                "https://drive.google.com/uc?export=download&id=191790CYx6x3_axe_sJDqW5rcj9io3Vkv"
            ],
            "Transcription": [""],
            "Review": [""]
        }
        df = pd.DataFrame(data, dtype=str)
        try:
            df.to_excel(EXCEL_FILE, index=False)
            print(f"Created sample Excel file: {EXCEL_FILE}")
            print("NOTE: Open 'call_center_data.xlsx' and update 'Name', 'Campaign', 'Serial Number', 'Date', and 'Recording Link' with your real data. Ensure the MP3 URL is a direct download link, points to a valid audio file (e.g., MP3, WAV), and is accessible.")
        except Exception as e:
            print(f"Error creating Excel file: {str(e)}")
            exit()

def transcribe_audio(audio_url):
    try:
        # Test URL accessibility
        req = urllib.request.Request(audio_url, method="HEAD")
        response = urllib.request.urlopen(req)
        if response.getcode() != 200:
            return f"Transcription Error: URL not accessible (status code: {response.getcode()})"
        content_type = response.headers.get("Content-Type", "")
        valid_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/flac", "audio/m4a", "audio/mp4", "audio/ogg", "audio/webm"]
        if not any(t in content_type for t in valid_types):
            return f"Transcription Error: Invalid content type ({content_type}); expected audio format (e.g., MP3, WAV)"

        # Use Deepgram API for transcription
        deepgram_url = "https://api.deepgram.com/v1/listen"
        data = {
            "url": audio_url,
            "model": "nova-3",
            "language": "en"
        }
        response = requests.post(deepgram_url, headers=deepgram_headers, json=data)
        if response.status_code != 200:
            return f"Transcription Error: Deepgram API request failed (status code: {response.status_code}) - {response.text}"

        result = response.json()
        if "results" not in result or "channels" not in result["results"]:
            return "Transcription Error: Invalid response from Deepgram API"
        
        transcript_text = result["results"]["channels"][0]["alternatives"][0]["transcript"]
        if not transcript_text:
            return "Transcription Error: Empty transcript returned"
        return transcript_text

    except Exception as e:
        return f"Transcription Error: {str(e)}"

def evaluate_call(transcription, customer_name):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a rockstar QA executive for a call center."},
                {"role": "user", "content": QA_PROMPT.format(transcription=transcription, customer_name=customer_name)}
            ],
            max_tokens=500
        )
        review = response.choices[0].message.content.strip()
        return review
    except Exception as e:
        return f"Review Error: API Error - {str(e)}"

def process_calls():
    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        exit()
    
    for index, row in df.iterrows():
        audio_url = row["Recording Link"]
        customer_name = row["Name"]
        if pd.isna(row["Transcription"]) or row["Transcription"] == "":
            transcription = transcribe_audio(audio_url)
            df.at[index, "Transcription"] = transcription
            review = evaluate_call(transcription, customer_name)
            df.at[index, "Review"] = review
        else:
            print(f"Skipping row {index + 2}: Already processed")
    
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")
        exit()

if __name__ == "__main__":
    setup_excel()
    process_calls()