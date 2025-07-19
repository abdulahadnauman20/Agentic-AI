# 🔑 Gemini API Key Setup Guide

## Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_api_key.py
```

### Option 2: Manual Setup

## 📋 Step-by-Step Instructions

### 1. Get Your API Key

1. **Visit Google AI Studio**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click **"Get API key"** or **"Create API key"**
   - If you have existing keys, click **"Create API key in new project"**
   - Give your project a name (e.g., "Career Mentor Agent")
   - Click **"Create"**

3. **Copy the Key**
   - Your API key will be displayed (starts with `AIza...`)
   - Copy the entire key
   - **Keep it secure** - don't share it publicly

### 2. Add to Your Project

#### Method A: Using the Setup Script
```bash
python setup_api_key.py
```

#### Method B: Manual Creation
1. Create a file named `.env` in your project root
2. Add this line:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with your copied key

### 3. Test Your Setup

```bash
python test_app.py
```

## 🔍 Troubleshooting

### Common Issues

1. **"API key not found"**
   - Make sure `.env` file is in the project root
   - Check the file name (should be exactly `.env`)
   - Verify the format: `GEMINI_API_KEY=your_key`

2. **"404 models/gemini-pro not found"**
   - Your API key might be invalid
   - Try generating a new key
   - Check if you have API access enabled

3. **"Permission denied"**
   - Make sure you're signed in with the correct Google account
   - Check if you have access to Gemini API in your region

### API Key Format
- ✅ Valid: `AIzaSyB...` (starts with AIza, about 39 characters)
- ❌ Invalid: `sk-...` (OpenAI format)
- ❌ Invalid: Empty or missing

## 🚀 After Setup

Once your API key is configured:

1. **Test the application**:
   ```bash
   python test_app.py
   ```

2. **Run the web app**:
   ```bash
   streamlit run app.py
   ```

3. **Open in browser**:
   - Navigate to: http://localhost:8501

## 🔒 Security Notes

- **Never commit your `.env` file** to version control
- **Don't share your API key** publicly
- **Use environment variables** in production
- **Monitor your API usage** in Google AI Studio

## 📞 Support

If you're still having issues:

1. Check the [Google AI Studio documentation](https://ai.google.dev/)
2. Verify your API key in the [Google AI Studio console](https://makersuite.google.com/app/apikey)
3. Test with a simple API call first

---

**Happy coding! 🚀** 