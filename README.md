# Call Center QA Agent

A comprehensive web-based application for automated quality assurance evaluation of call center recordings. This tool helps call center managers and QA teams efficiently review and assess agent performance through AI-powered transcription and evaluation.

## 🎯 Purpose

The Call Center QA Agent is designed to streamline the quality assurance process for call centers, particularly those handling Final Expense campaigns. It automates the transcription of call recordings and provides AI-powered evaluations based on established QA criteria.

## ✨ Features

### Core Functionality
- **Audio Transcription**: Automatically transcribes call recordings using Deepgram API
- **AI-Powered Evaluation**: Evaluates calls using OpenAI GPT-3.5-turbo based on comprehensive QA criteria
- **User Management**: Secure login and registration system with user-specific data storage
- **Dashboard Analytics**: Real-time performance metrics and employee analytics
- **Excel Integration**: Import/export call data via Excel files

### QA Evaluation Criteria
The system evaluates calls based on 12 key criteria:

1. **DNC Status**: Detects Do Not Call (DNC) violations
2. **Customer Tone Analysis**: Identifies customer sentiment (polite, abusive, frustrated, neutral)
3. **No Call List Compliance**: Flags customers who mention being on no-call lists
4. **DNC Indicators**: Analyzes context for potential DNC situations
5. **Agent Pushiness**: Evaluates if agents are overly aggressive or interrupting
6. **Licensed Agent Requests**: Flags when customers request licensed agent transfers
7. **Multiple Calls Complaints**: Identifies customers who mention receiving multiple calls
8. **Customer Name Validation**: Checks for inappropriate or abusive customer names
9. **Agent Conduct**: Verifies proper microphone usage and English-only communication
10. **Professionalism**: Assesses agent tone and delivery quality
11. **Compliance**: Evaluates script adherence and legal standards
12. **Effectiveness**: Measures call success and sales approach

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Required Python packages (install via pip):
  ```
  pip install flask flask-cors pandas openpyxl openai requests
  ```

### API Keys Required
1. **OpenAI API Key**: For call evaluation and analysis
2. **Deepgram API Key**: For audio transcription

### Installation & Setup

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install flask flask-cors pandas openpyxl openai requests
   ```

3. **Configure API Keys**:
   - Open `qa_script.py`
   - Replace the placeholder API keys with your actual keys:
     ```python
     OPENAI_API_KEY = "your-openai-api-key-here"
     DEEPGRAM_API_KEY = "your-deepgram-api-key-here"
     ```
   - **Important**: Never commit your actual API keys to version control

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open your web browser
   - Navigate to: `http://127.0.0.1:5000`

## 📊 How to Use

### 1. User Registration/Login
- Register a new account or login with existing credentials
- Each user has their own dashboard with personalized data

### 2. Call Data Management
- **Excel Import**: Use the provided `call_center_data.xlsx` template
- **Required Fields**:
  - Name: Customer name
  - Campaign: Campaign type (e.g., "Final Expense")
  - Serial Number: Unique call identifier
  - Date: Call date
  - Recording Link: Direct download URL to audio file

### 3. Call Review Process
1. Upload or update your Excel file with call data
2. The system automatically:
   - Transcribes audio recordings
   - Evaluates calls based on QA criteria
   - Generates comprehensive reviews
   - Updates the Excel file with results

### 4. Dashboard Analytics
- **Performance Metrics**: View overall call center performance
- **Employee Analytics**: Individual agent performance tracking
- **Success Rates**: Approval rates and improvement areas
- **Token Usage**: Track API usage and costs

## 📁 File Structure

```
Prototype3.6/
├── app.py                 # Flask web application
├── qa_script.py          # Core QA evaluation logic
├── index.html            # Web interface
├── users.json            # User data storage
├── call_center_data.xlsx # Sample call data template
└── README.md            # This documentation
```

## 🔧 Configuration

### Excel File Format
The application expects an Excel file with the following columns:
- **Name**: Customer name
- **Campaign**: Campaign type
- **Serial Number**: Unique identifier
- **Date**: Call date
- **Recording Link**: Audio file URL
- **Transcription**: (Auto-filled by system)
- **Review**: (Auto-filled by system)

### Audio File Requirements
- Supported formats: MP3, WAV, FLAC, M4A, MP4, OGG, WEBM
- Must be accessible via direct download URL
- Recommended: Clear audio quality for accurate transcription

## 🛡️ Security Features

- **User Authentication**: Secure login system
- **Data Isolation**: User-specific data storage
- **API Key Protection**: Secure API key management
- **CORS Support**: Cross-origin request handling

### Security Best Practices
- **Never commit API keys**: Use placeholder values in code, replace with actual keys locally
- **Environment Variables**: Consider using environment variables for sensitive configuration
- **Access Control**: Implement proper user access controls for production use
- **Data Privacy**: Ensure compliance with data protection regulations when handling call recordings

## 📈 Performance Tracking

The system tracks various metrics:
- **Recorded Calls**: Total calls processed
- **Target Calls**: Set goals for call volume
- **Token Usage**: OpenAI API usage tracking
- **Request Count**: API call monitoring
- **Employee Performance**: Individual agent analytics

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify your OpenAI and Deepgram API keys are correct
   - Ensure you have sufficient API credits

2. **Audio Transcription Failures**:
   - Check that audio URLs are accessible
   - Verify audio file format is supported
   - Ensure audio quality is sufficient

3. **Excel File Issues**:
   - Use the provided template format
   - Ensure all required columns are present
   - Check file permissions

4. **Server Connection**:
   - Verify the Flask app is running on port 5000
   - Check firewall settings if accessing remotely

## 🚀 Deployment

### Development
- The application runs on Flask's development server
- Suitable for testing and development use

### Production
- Use a production WSGI server (e.g., Gunicorn, uWSGI)
- Configure proper security headers
- Set up HTTPS for production environments
- Implement proper logging and monitoring

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Verify API key configurations
- Ensure all dependencies are in

---

**Note**: This application is designed specifically for Final Expense campaign call evaluation but can be adapted for other call center use cases by modifying the evaluation criteria in `qa_script.py`. 