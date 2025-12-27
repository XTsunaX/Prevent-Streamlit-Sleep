Cover image for Keeping your Streamlit app awake using Selenium and Github Actions
Benson King'ori
Benson King'ori Subscriber
Posted on 8月29日


2
Keeping your Streamlit app awake using Selenium and Github Actions
#
selenium
#
githubactions
#
webdev
#
programming
TLDR;
Streamlit apps sleep after a period of inactivity if hosted on Streamlit Community Cloud (free tier)
To wake your app up, you need to click a button
We can use Github actions + Selenium to automate this button clicking every couple of hours
Table of Contents
Introduction
Step 1: Create Repo
Step 2: Create Python Script
Step 3: Create Github Workflow
Step 4: Commit and Push
Step 5: Run the workflow manually
Conclusion
Introduction
Streamlit apps hosted on the Community Edition (free tier) go to sleep after some period of inactivity. This used to be 24 hours during weekdays and 72 hours on weekends but it had been cut down to 12 hours and that number might even be lower now. Given how we have used Streamlit for project demos and portfolio pages, this is quite a concern. In this article, I explore how to use Github actions to run a script every 4 hours that keep your Streamlit app from going to sleep.

Step 1: Create Repo
On your Github account, create a new repo and pull it locally in your desired folder.

Step 2: Create Python Script
In your local repository, paste the following code in main.py file:

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://benson-mugure-portfolio.streamlit.app/")

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 15)
        try:
            # Look for the wake-up button
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Wake-up button found. Clicking...")
            button.click()

            # After clicking, check if it disappears
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                print("Button clicked and disappeared ✅ (app should be waking up)")
            except TimeoutException:
                print("Button was clicked but did NOT disappear ❌ (possible failure)")
                exit(1)

        except TimeoutException:
            # No button at all → app is assumed to be awake
            print("No wake-up button found. Assuming app is already awake ✅")

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
    finally:
        driver.quit()
        print("Script finished.")

if __name__ == "__main__":
    main()
Replace the value of the STREAMLIT_URL variable with your own app’s URL as a string.

Step 3: Create Github Workflow
Also in your local repository, create the file .github/workflows/wake.yml and paste the code below:

name: Wake Streamlit App

on:
  schedule:
    - cron: "0 */4 * * *"   # every 4 hours
  workflow_dispatch:         # allow manual trigger

jobs:
  wake:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Selenium script
        run: python main.py
At the base of your repository, add a requirements.txt file with the following contents:

selenium
webdriver-manager
Step 4: Commit and Push
Run the following commands to add and commit your changes:

git add .
git commit -m “add files”
git push
Needless to say, you can modify the commit message as you wish

Step 5: Run the workflow manually
Go to your repository on Github and confirm that the changes have been made, i.e., your files have been pushed. On that repo, click on the Actions tab as can be seen below:

Github Menu

You should be able to see the Wake Streamlit App workflow on the right, right under All Workflows. Click on the Wake Streamlit App. On the right, you should see a button that says Run Workflow. Click it. Another green button with the same label appears. Click it too. You will now see the workflow is in progress. This takes about 2 minutes. After the time has lapsed, check if your Streamlit app is awake. If not, check the logs on Github and debug.

Conclusion
And there you have it, a simple and free way to keep your Streamlit app awake (hopefully forever). You can find the full code example in this repository here. There is also an option to modify this workflow so that it makes an empty commit to the repository that the Streamlit app is deployed from in that same branch. Perhaps you can explore this option as well if you are feeling adventurous. Empty commits do not necessarily wake your app up but they do reset the clock that is counting down idle time to set your app to sleep. Let me know if you found this article helpful.

Top comments (2)
Subscribe
pic
Add to the discussion
 
 
sherrydays profile image
Sherry Day
•
8月30日

Clever approach—appreciate this!


1
 like
Like

Reply
 
 
virgoalpha profile image
Benson King'ori Subscriber 
•
8月30日

Thank you, @sherrydays !


1
 like
Like

Reply
Code of Conduct • Report abuse

Benson King'ori 
Follow
Cogito ergo sum
Location
Mauritius
Joined
2023年8月20日
More from Benson King'ori
Resurrecting Google Reader for the modern web using Kiro
#kiroween #webdev #programming #kiro
AWS Cloud Resume Challenge - my attempt
#aws #serverless #githubactions #sam
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://benson-mugure-portfolio.streamlit.app/")

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 15)
        try:
            # Look for the wake-up button
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Wake-up button found. Clicking...")
            button.click()

            # After clicking, check if it disappears
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                print("Button clicked and disappeared ✅ (app should be waking up)")
            except TimeoutException:
                print("Button was clicked but did NOT disappear ❌ (possible failure)")
                exit(1)

        except TimeoutException:
            # No button at all → app is assumed to be awake
            print("No wake-up button found. Assuming app is already awake ✅")

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
    finally:
        driver.quit()
        print("Script finished.")

if __name__ == "__main__":
    main()
