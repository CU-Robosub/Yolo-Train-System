# Robosub-Weight-Retrieve
Script that allows users to select and download weight files from Google drive and distribute them easily in darknet_config. Clone the repo, and when authenticating, sign in using your personal Google account.



### Install the Google Client Library
- pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
- (if given a warning about improper permissions, use sudo pip install --upgrade...)



### Run script and authenticate into Google account
Format for running script:
./get_weights.sh <weight folder name>

When running the script for the first time, a web browser will open asking to authenticate.
