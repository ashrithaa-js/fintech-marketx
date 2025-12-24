# Deployment Guide - Stock Intelligence Platform

## 🚀 Deploying to Streamlit Cloud

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at https://streamlit.io/cloud)
3. Git installed on your machine

---

## Step 1: Push to GitHub

### 1.1 Initialize Git Repository

```bash
# Navigate to project directory
cd stock-intelligence-platform

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Stock Intelligence Platform"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `stock-intelligence-platform`)
3. **DO NOT** initialize with README, .gitignore, or license (we already have these)

### 1.3 Push to GitHub

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/stock-intelligence-platform.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Connect Repository

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `stock-intelligence-platform`
5. Set main file path: `streamlit_app/app.py`
6. Click "Deploy!"

### 2.2 Configure App Settings

**App URL**: `https://YOUR_APP_NAME.streamlit.app`

**Main file**: `streamlit_app/app.py`

**Python version**: 3.8+ (Streamlit Cloud will auto-detect)

### 2.3 Environment Variables (Optional)

If you need API keys or environment variables:

1. Go to your app settings in Streamlit Cloud
2. Click "Secrets" tab
3. Add secrets in TOML format:

```toml
ALPHA_VANTAGE_KEY = "your_api_key_here"
```

---

## Step 3: Post-Deployment

### 3.1 Verify Deployment

1. Visit your Streamlit Cloud URL
2. Check that all pages load correctly
3. Test stock selection functionality

### 3.2 Data Files

**Note**: Streamlit Cloud is stateless. Data files won't persist between deployments.

**Options**:
1. **Use sample data**: Include sample CSV files in the repository
2. **External storage**: Use cloud storage (S3, Google Cloud Storage)
3. **Database**: Connect to a database (PostgreSQL, MongoDB)
4. **API**: Fetch data from external APIs

### 3.3 Update Data

To update data files:
1. Update files locally
2. Commit and push to GitHub
3. Streamlit Cloud will automatically redeploy

---

## 📝 Important Notes

### File Structure for Streamlit Cloud

```
stock-intelligence-platform/
├── streamlit_app/
│   ├── app.py              # Main entry point
│   ├── pages/              # Dashboard pages
│   └── path_setup.py       # Path configuration
├── src/                    # Source code
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md
```

### Limitations

1. **No persistent storage**: Data files reset on each deployment
2. **Resource limits**: Free tier has CPU/memory limits
3. **No background processes**: Can't run continuous price streaming
4. **File size limits**: Large data files may cause issues

### Recommendations

1. **Use sample data**: Include small sample CSV files for demo
2. **External APIs**: Fetch data from APIs instead of files
3. **Database**: Use external database for persistent storage
4. **Scheduled updates**: Use external services for data updates

---

## 🔄 Updating Your App

### Making Changes

1. Make changes locally
2. Test locally: `streamlit run streamlit_app/app.py`
3. Commit changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. Streamlit Cloud will automatically redeploy (usually takes 1-2 minutes)

---

## 🐛 Troubleshooting

### App Won't Deploy

1. **Check requirements.txt**: Ensure all dependencies are listed
2. **Check file paths**: Verify `streamlit_app/app.py` exists
3. **Check imports**: Ensure all imports are correct
4. **Check logs**: View deployment logs in Streamlit Cloud dashboard

### Import Errors

- Ensure all Python files are in correct directories
- Check that `path_setup.py` is working correctly
- Verify all dependencies in `requirements.txt`

### Data Not Loading

- Check file paths (use relative paths)
- Ensure data files exist in repository (or use sample data)
- Check file permissions

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [GitHub Documentation](https://docs.github.com/)

---

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed on Streamlit Cloud
- [ ] All pages loading correctly
- [ ] Dependencies installed correctly
- [ ] Sample data included (if needed)
- [ ] README updated with deployment URL

---

## 🎉 Success!

Once deployed, your app will be available at:
`https://YOUR_APP_NAME.streamlit.app`

Share this URL with others to access your Stock Intelligence Platform!

