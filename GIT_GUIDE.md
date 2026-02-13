# Git Fresh Start Guide

Since you have your code locally and a **brand new empty repository** on GitHub, follow these exact steps to connect them and upload your code.

## 1. Open Terminal
Open your terminal (Command Prompt or PowerShell) inside your project folder: `public health record`

## 2. Initialize Git (If not already done)
Run this command. If it says "Reinitialized existing Git repository", that is fine.
```bash
git init
```

## 3. Add Your Files
This prepares all your files to be saved.
```bash
git add .
```

## 4. Save Your Changes (Commit)
```bash
git commit -m "Initial commit of Public Health Record System"
```

## 5. Rename Branch to 'main' (Standard practice)
```bash
git branch -M main
```

## 6. Link to Your GitHub Repository
This connects your computer to the new empty repo you see in your screenshot.
*(If it says "remote origin already exists", run `git remote remove origin` first, then run this again)*
```bash
git remote add origin https://github.com/tayadekunal987/public-health-record.git
```

## 7. Push Your Code
This uploads everything to GitHub.
```bash
git push -u origin main
```

---
**Troubleshooting**
- If `git remote add` fails saying it **already exists**:
  Run: `git remote set-url origin https://github.com/tayadekunal987/public-health-record.git`
- If `git push` fails, try: `git push -f origin main` (Force push - only do this on a new empty repo).
