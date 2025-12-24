# Quick GitHub & Streamlit Cloud Setup Guide

## ✅ Step 1: Git Repository Initialized
Your local git repository is ready! (Commit created: 620ec37)

## 📝 Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `stock-intelligence-platform`
3. Description: "Comprehensive real-time stock market analytics and ML prediction system"
4. Choose: **Public** or **Private**
5. **DO NOT** check:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Click **"Create repository"**

## 🚀 Step 3: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Navigate to your project (if not already there)
cd C:\Users\ashri\Downloads\stock-intelligence-platform

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/stock-intelligence-platform.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note**: You'll be prompted for GitHub credentials. Use:
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
  - Create one at: https://github.com/settings/tokens
  - Select scope: `repo` (full control)

## 🌐 Step 4: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select `stock-intelligence-platform`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/app.py`
   - **App URL**: (auto-generated, or choose custom)
5. Click **"Deploy!"**

## ⏱️ Wait for Deployment

- First deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Build your app
  - Deploy it

## 🎉 Success!

Your app will be live at:
`https://YOUR_APP_NAME.streamlit.app`

## 📋 Quick Commands Reference

```bash
# Check git status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# View remote
git remote -v
```

## 🔄 Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy (usually 1-2 minutes).

## ⚠️ Important Notes

1. **Data Files**: Streamlit Cloud is stateless. Large data files won't persist.
   - Solution: Use sample data or external storage (S3, database)

2. **Environment Variables**: If you need API keys:
   - Go to Streamlit Cloud → Your App → Settings → Secrets
   - Add in TOML format

3. **Dependencies**: All packages in `requirements.txt` will be installed automatically

4. **File Size**: Keep repository under 1GB for best performance

## 🐛 Troubleshooting

### Push Fails
- Check internet connection
- Verify GitHub credentials
- Ensure repository exists on GitHub

### Streamlit Deployment Fails
- Check `requirements.txt` has all dependencies
- Verify `streamlit_app/app.py` exists
- Check deployment logs in Streamlit Cloud dashboard

### App Won't Load
- Check file paths (use relative paths)
- Verify imports are correct
- Check Streamlit Cloud logs

---

**Need Help?**
- GitHub Docs: https://docs.github.com/
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud

