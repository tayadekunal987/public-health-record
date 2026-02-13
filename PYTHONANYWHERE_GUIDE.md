# Deploying to PythonAnywhere (Best for SQLite)

PythonAnywhere is the **best free option** for your app because it keeps your database safe (it won't be deleted daily like on Render).

## Step 1: Create an Account
1.  Go to [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  Sign up for a **Beginner** (Free) account.

## Step 2: Upload Your Code
1.  Log in and go to the **Dashboard**.
2.  Click on **Consoles** -> **Bash**.
3.  In the black terminal window, run this command to download your code from GitHub:
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    ```
    *(Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual details)*

## Step 3: Install Requirements
1.  Go into your project folder:
    ```bash
    cd YOUR_REPOSITORY_NAME
    ```
2.  Install the libraries your app needs:
    ```bash
    pip3 install -r requirements.txt
    ```

## Step 4: Set Up the Web App
1.  Go to the **Web** tab (top right).
2.  Click **Add a new web app**.
3.  Click **Next**.
4.  Select **Flask**.
5.  Select **Python 3.10** (or the latest version available).
6.  **Path**: It will ask for the path to your flask app. Enter:
    `/home/yourusername/YOUR_REPOSITORY_NAME/app.py`
    *(Replace `yourusername` with your PythonAnywhere username and `YOUR_REPOSITORY_NAME` with your folder name)*

## Step 5: Configure the Database
1.  Go to the **Files** tab.
2.  Click on your project folder.
3.  Check if there is an `instance` folder. If not, create it.
4.  **Important**: You need to initialize the database. Go back to the **Bash** console and run:
    ```bash
    python3 init_db.py
    ```
    *(This creates the `site.db` file)*

## Step 6: Final Configuration (WSGI File)
1.  Go to the **Web** tab.
2.  Scroll down to the **Code** section.
3.  Click the link next to **WSGI configuration file** (it looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
4.  **Delete everything** in that file.
5.  Paste this code (replace `yourusername` and `YOUR_REPOSITORY_NAME`):

```python
import sys
import os

# add your project directory to the sys.path
project_home = '/home/yourusername/YOUR_REPOSITORY_NAME'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from app import app as application
```
6.  Click **Save**.

## Step 7: Launch!
1.  Go back to the **Web** tab.
2.  Click the big green **Reload** button at the top.
3.  Click the link to your site (e.g., `yourusername.pythonanywhere.com`).

**Your app is now live and your database is safe!**
