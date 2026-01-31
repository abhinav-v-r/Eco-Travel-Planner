# 🚀 Deploying to Streamlit Cloud

This guide shows you how to deploy your Eco-Travel AI Planner to Streamlit Cloud for free.

## Prerequisites

- A GitHub account
- Your code pushed to a GitHub repository
- A Google Gemini API key

## Step 1: Push to GitHub

Make sure your code is on GitHub:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Note:** Your `.env` file will NOT be uploaded (it's in `.gitignore`). This is intentional for security.

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `your-username/eco-travel`
5. Set the main file path: `app.py`
6. Click **"Advanced settings"**

## Step 3: Add Your API Key as a Secret

In the **Advanced settings** section:

1. Find the **"Secrets"** text area
2. Add the following (replace with your actual key):

```toml
GOOGLE_API_KEY = "your_actual_google_api_key_here"
```

3. Click **"Save"**
4. Click **"Deploy"**

## Step 4: Wait for Deployment

Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Load your API key from secrets
- Launch your app

This usually takes 2-3 minutes.

## 🎉 Your App is Live!

Once deployed, you'll get a public URL like:
```
https://your-app-name.streamlit.app
```

Share this link with anyone!

## 🔄 Updating Your App

Any time you push changes to GitHub, Streamlit Cloud will automatically redeploy your app.

## 🔒 Security Notes

- Your API key is stored securely in Streamlit's secrets management
- The `.env` file stays on your local machine only
- Never commit API keys to GitHub

## 📊 Monitoring

- View logs and metrics in the Streamlit Cloud dashboard
- Monitor API usage at [Google AI Studio](https://aistudio.google.com)

---

**Need help?** Check the [Streamlit Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)
