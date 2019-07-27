# Robosub-Weight-Retrieve
Script that allows users to select and download weight files from Google drive and distribute them easily in darknet_config

### Create Google Cloud project and activate Google Drive API
![](readme_screenshots/screen_1.png)
- Click "Console"

![](readme_screenshots/screen_2.png)
- Navigate to project creation
- Click "NEW PROJECT"

![](readme_screenshots/screen_3.png)
- Name project "Robosub Weight Retrieve"

![](readme_screenshots/screen_4.png)
- Click bell icon at the top right of the screen
- Click on your new project once it finishes loading

![](readme_screenshots/screen_5.png)
- Hover over "APIs & Services"
- Click "Credentials"

![](readme_screenshots/screen_6.png)
- Click "Create credentials"
- Click "OAuth client ID"

![](readme_screenshots/screen_7.png)
- Click "Configure consent screen"

![](readme_screenshots/screen_8.png)
- Enter "Application name" as "Robosub Weight Retrieve"
- Scroll down and click "Save"

![](readme_screenshots/screen_9.png)
- Click "Other"
- Enter "Name" as "Robosub Weight Retrieve"

![](readme_screenshots/screen_10.png)
- Click "OK"

![](readme_screenshots/screen_11.png)
- Click on new project "Robosub Weight Retrieve"

![](readme_screenshots/screen_12.png)
- Click "DOWNLOAD JSON"
- Move JSON file into the project directory
- Rename JSON file to "client_secret.json"



### Install the Google Client Library
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

(if given a warning about improper permissions, use sudo pip install --upgrade...)


### Run script and authenticate into Google account
Format for running script:
./get_weights.sh <weight folder name>

When running the script for the first time, a web browser will open asking to authenticate.
