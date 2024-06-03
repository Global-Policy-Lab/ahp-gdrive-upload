# Google Drive Upload Automation Script

This repository contains code to set up an automated upload flow from local machines to Google Drive. 



## 1. Setting up Credentials

The uploading of data to Google Drive requires OAUTH authentication via a credential which is generated in https://console.cloud.google.com/apis/credentials

Make sure that you are are in a project that belongs to your user (that has the google drive space).



1. Clikc on create credentials, select OAUTH option
2. Select Application type to DESKTOP APP, give it a name e.g. Upload-Google_Drive
3. This will create the credential which you download. Rename the credential from `client_secret_...json` to `oath_key.json` or any name of your choosing.
4. Store the file in the projects Config folder

