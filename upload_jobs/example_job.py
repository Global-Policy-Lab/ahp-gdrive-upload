from GoogleDrive import GoogleDriveService

# IF YOU NEED TO JUST UPLOAD ONE FILE
def main():

    gd = GoogleDriveService('personal_account')

    fp = "path/to/file"
    folder_id = "folder_id"   # the destination on Google Drive
    file_name = "file_name"

    gd.upload_file(fp, folder_id, file_name)

# IF YOU NEED TO UPLOAD MULTIPLE FILES

def main():

    gd = GoogleDriveService('personal_account')

    folder_id = "folder_id"

    # if we want to make subfolder in the folder_id
    subfolder_1_id = gd.create_folder("subfolder_name", folder_id)
    subfolder_2_id = gd.create_folder("subfolder_name", folder_id)

    # and if  we want further subfolders
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




if __name__ == "__main__": 

    pass