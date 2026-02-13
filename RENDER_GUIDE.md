# Deploying to Render.com

**Warning**: Since you are using SQLite, **all your data (users, appointments) will be deleted every time you deploy or the app restarts** (which happens automatically every day on the free plan).
*If you need your data to stay safe, use PythonAnywhere instead.*

If you still want to deploy to Render for testing/demo purposes, follow these steps:

## Step 1: Create Account
1.  Go to [render.com](https://render.com/).
2.  Sign up with your **GitHub** account.

## Step 2: Create Web Service
1.  Click **New +** and select **Web Service**.
2.  Select **Build and deploy from a Git repository**.
3.  Find your `public-health-record` repository and click **Connect**.

## Step 3: Configure Settings
Fill in the details exactly as below:

*   **Name**: `public-health-record` (or any name you like)
*   **Region**: `Singapore` (or `Frankfurt` - whichever is closest)
*   **Branch**: `main` (or `master`)
*   **Runtime**: `Python 3`
*   **Build Command**:
    ```bash
    pip install -r requirements.txt && python init_db.py
    ```
    *(This installs libraries AND creates the database file every time)*
*   **Start Command**:
    ```bash
    gunicorn app:app
    ```
*   **Plan**: `Free`

## Step 4: Deploy
1.  Click **Create Web Service**.
2.  Wait for the logs to finish. You should see "Your service is live".
3.  Click the URL at the top (e.g., `https://public-health-record.onrender.com`) to visit your site.

---
**Troubleshooting**
- If you see "Internal Server Error", check the **Logs** tab in Render.
- If it says "Table not found", verify your **Build Command** includes `&& python init_db.py`.
