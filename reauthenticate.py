import os
import sys

def set_project_root():
    """ Sets the root directory for the project dynamically. """
    root_dir = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(root_dir, '.project_root')) and root_dir != '/':
        root_dir = os.path.dirname(root_dir)
    assert root_dir != '/', "The .project_root file was not found. Make sure it exists in your project root."
    sys.path.append(root_dir)
    return root_dir

root_dir = set_project_root()

import yaml
from GoogleDrive import GoogleDriveService


def reauthenticate(auth_method):
    yml = f"{root_dir}/config/config.yml"
    with open(yml, 'r') as file:
        cfg = yaml.safe_load(file)

    # delete the token file
    if auth_method == 'personal_account':
        token = cfg.get('personal_account_token_path')
        if os.path.exists(token):
            os.remove(token)

    gd = GoogleDriveService(auth_method)
    gd.build()
    print(f"Successfully reauthenticated using {auth_method} credentials.")
    return gd


if __name__ == '__main__':
    reauthenticate('personal_account')