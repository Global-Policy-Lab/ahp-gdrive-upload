# Google Drive Upload Automation Script

Welcome to the **Google Drive Upload Automation Script** for the Aerial History Project! This repository contains code designed to facilitate the seamless upload of files and folders from your local machines or servers to Google Drive. Let’s dive into the details and get you set up!

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up Credentials](#setting-up-credentials)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [License](#license)
8. [Contact](#contact)

## Introduction

This script is your go-to tool for automating the upload process to Google Drive, ensuring your valuable data is securely backed up in the cloud. Whether you’re working on servers or local machines, our script is designed to make your life easier and your workflow smoother.

## Setting Up Credentials

To upload data to Google Drive, you'll need to set up OAuth authentication. This requires credentials generated from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Follow these steps to get your credentials ready:

1. **Create Credentials:**
   - Navigate to the Google Cloud Console.
   - Ensure you're in a project that belongs to your user account with the necessary Google Drive space.
   - Click on "Create credentials" and select the "OAuth client ID" option.

2. **Configure OAuth Client:**
   - Select the application type as "Desktop App" and give it a meaningful name, e.g., `Upload-Google_Drive`.
   - This will generate a credential file. Download this file.

3. **Rename and Store the Credential:**
   - Rename the downloaded credential file from `client_secret_...json` to `personal_key.json` or any other name of your choosing.
   - Place the renamed file in the `config` folder of the project.

## Installation

Clone the repository and navigate into the project directory:

```sh
git clone https://github.com/yourusername/google-drive-upload-automation.git
cd google-drive-upload-automation
```

Install the required dependencies using the provided `environment.yml` file:

```sh
conda env create -f environment.yml
```

This will create a new Conda environment named `gdrive`. Make sure to activate this environment:

```sh
conda activate gdrive
```

**Note:** If you want to share this project with friends, ensure that the `prefix` line in `environment.yml` is removed or replaced with their specific path to avoid installation issues. The file should look like this:

```yaml
name: gdrive
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pyyaml
  - oauth2client
  - google-api-python-client
  - google-auth-oauthlib
```

## Configuration

Ensure your `config/config.yml` file is set up correctly. This file should contain paths to your service account and personal account credentials:

```yaml
service_account_cred_path: "path/to/your/service_account_credentials.json"
personal_account_cred_path: "path/to/your/personal_key.json"
personal_account_token_path: "path/to/your/token.pickle"
```

### Authentication on a Server

If you are authenticating on a server, you will need port forwarding to authenticate. This can be set up in VSCode. After you authenticate on Google, it will redirect to a `localhost:XXXX` where the port number should be added to the port forwarding in VSCode. There are other ways also to do port forwarding, but this is the simplest.

### Token Expiry

After about a week, the token will expire. We have added a script called `reauthenticate.py` which deletes the token and re-runs the authentication workflow. This can be good to run if your code is not working, or if you know the token has expired, run this before working on the project.

## Usage

The script includes various functionalities to manage Google Drive uploads, including uploading files and folders, checking if a folder exists, and deleting items. 

There are some important arguments in the functions:

   - `file_name` is the name of the files as displayed in Google Drive. 
   - `file_path` is the path on your system to the file that is to be uploaded.
   - `mime_type` is a code indicating what kind of file is being uploaded. You can see different mime types [here](https://developers.google.com/drive/api/guides/ref-export-formats).
   - `folder_id` is the id of your destination folder. It is found in the URL after `/folder/`

Here’s a quick overview of how to use it:

### Uploading a File

To upload a single file, use the `upload_file` method:

```python
from your_script import GoogleDriveService

service = GoogleDriveService("personal_account")
service.upload_file("file_name.pdf", "/path/to/your/file.pdf", "application/pdf", "your_drive_folder_id")
```

### Uploading a Folder

To upload an entire folder, use the `upload_folder` method:

```python
service.upload_folder("/path/to/your/local/folder", "your_drive_folder_id", skip=["unwanted_file_or_folder"], overwrite=True)
```

### Additional Examples

You can find more examples in the `upload_jobs/example_job.py` file. Here are a couple of examples to get you started:

#### Uploading a Single File

```python
from GoogleDrive import GoogleDriveService

def main():
    gd = GoogleDriveService('personal_account')

    fp = "path/to/file"
    folder_id = "folder_id"   # the destination on Google Drive
    file_name = "file_name"

    gd.upload_file(fp, folder_id, file_name)
```

#### Uploading Multiple Files with Subfolders

```python
from GoogleDrive import GoogleDriveService

def main():
    gd = GoogleDriveService('personal_account')

    folder_id = "folder_id"

    # if we want to make subfolders in the folder_id
    subfolder_1_id = gd.create_folder("subfolder_name", folder_id)
    subfolder_2_id = gd.create_folder("subfolder_name", folder_id)

    # and if we want further subfolders
    subfolder_3_id = gd.create_folder("subfolder_name", subfolder_1_id)

    data = [
        {
            "fp": "path/to/file",
            "file_name": "file_name",
            "folder_id": folder_id
        },
        {
            "fp": "path/to/file",
            "file_name": "file_name",
            "folder_id": subfolder_1_id
        }, 
        {
            "fp": "path/to/file",
            "file_name": "file_name",
            "folder_id": subfolder_2_id
        },
        {
            "fp": "path/to/file",
            "file_name": "file_name",
            "folder_id": subfolder_3_id
        }
    ]

    for d in data:
        gd.upload_file(d['fp'], d['folder_id'], d['file_name'])
```

## Troubleshooting

Encountering issues? Here are some common problems and solutions:

- **.project_root file not found:** Ensure that the `.project_root` file is present in the root directory of your project.
- **Invalid credentials:** Double-check the paths in your `config.yml` file and ensure your credentials are correctly set up.
- **Permission errors:** Verify that your Google Drive API is enabled in the Google Cloud Console and that your credentials have the necessary permissions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, please contact jeffrey.clark@su.se or find Jeffrey Clark on Slack.

---

Happy uploading! 🚀