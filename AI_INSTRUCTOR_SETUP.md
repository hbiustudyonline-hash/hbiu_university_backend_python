# AI Instructor Setup Guide

## Quick Start (5 minutes)

### Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "**Create new secret key**"
4. Copy the key (starts with `sk-proj-...`)
5. **Important**: Save it somewhere safe - you can't view it again!

### Step 2: Add API Key to Backend

1. Open `hbiu_university_backend_python/.env`
2. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-abcd1234...your-actual-key
   ```
3. Save the file

### Step 3: Start Python Backend

```bash
cd hbiu_university_backend_python
python -m pip install -r requirements.txt
python main.py
```

The backend will start on http://localhost:8000

### Step 4: Create Your First AI Instructor

1. Make sure both frontend (localhost:5173) and Python backend (localhost:8000) are running
2. Log in as a lecturer or admin
3. Go to any course
4. Click the "Home" tab
5. Click "**Create AI Instructor**"
6. Fill in:
   - **Upload instructor photo** (for avatar)
   - **Name**: e.g., "Dr. Sarah Johnson"
   - **Title**: e.g., "Associate Professor"
   - **Specialization**: e.g., "Psychology"
   - **Textbook content**: Paste your course textbook or PDF content
7. Click "Create Instructor"

### Step 5: Test It Out!

Click "**Start Live Video Session**" and ask:
- "Explain chapter 1 to me"
- "What are the key concepts in this course?"
- "Help me with my homework question"
- "Create a study plan for the midterm"

## Features You Get (Text/Voice Mode)

✅ **Instant Q&A**: Students can ask questions 24/7
✅ **Chapter Summaries**: AI explains topics from the textbook
✅ **Homework Help**: Step-by-step guidance (not direct answers)
✅ **Study Plans**: Personalized preparation strategies
✅ **8 Languages**: English, Spanish, French, Chinese, Swahili, Arabic, German, Portuguese
✅ **Voice Responses**: Natural text-to-speech

## Cost (Very Affordable)

- **Average cost per student interaction**: $0.01 - $0.05
- **100 AI conversations**: ~$1-5
- **Monthly for 50 students**: ~$10-25

## Optional Upgrades

### Add Video Animation (Later)
If you want full animated video:
1. Get D-ID API key from https://studio.d-id.com/
2. Add to `.env`: `DID_API_KEY=your_key_here`
3. Cost: ~$0.10-0.30 per video minute

### Add Premium Voice (Later)
For ultra-realistic voice:
1. Get ElevenLabs key from https://elevenlabs.io/
2. Add to `.env`: `ELEVENLABS_API_KEY=your_key_here`
3. Cost: Free tier available, then $11/month

## Troubleshooting

### "OpenAI client initialization failed"
- Check your API key is correct in `.env`
- Ensure it starts with `sk-proj-` or `sk-`
- Restart the Python backend

### "API key not found"
- Make sure `.env` file exists in `hbiu_university_backend_python/`
- Check the key is on a new line without spaces around `=`

### "Rate limit exceeded"
- OpenAI has usage limits based on your account tier
- Upgrade at https://platform.openai.com/account/billing

## Need Help?

Check the logs in the Python backend terminal for detailed error messages.
