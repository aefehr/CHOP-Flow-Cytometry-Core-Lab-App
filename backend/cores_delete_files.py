import os
import datetime

def read_folders_from_file(file_path, N):
    with open(file_path, 'r') as file:
        folders = [line.strip() for line in file]

    # Ask for confirmation before proceeding
    user_confirmation = input(f"Do you want to delete old files and folders from the list of folders in the file you provided? (yes/no): ").upper()
    if (user_confirmation == 'NO' or user_confirmation == 'N'): 
        print("Operation aborted.")
        return

    delete_old_files_and_folders(folders, N)

def delete_old_files_and_folders(folders, N):
    for folder in folders:
        if os.path.exists(folder):
            # loop to check all files and folders one by one  
            # os.walk returns 3 things: current path, files in the current path, and folders in the current path  
            for (root, dirs, files) in os.walk(folder, topdown=True): 
                for f in files: 
                    # temp variable to store path of the file  
                    file_path = os.path.join(root, f) 
                    # get the timestamp, when the file was modified  
                    timestamp_of_file_modified = os.path.getmtime(file_path) 
                    # convert timestamp to datetime 
                    modification_date = datetime.datetime.fromtimestamp(timestamp_of_file_modified) 
                    # find the number of days when the file was modified 
                    number_of_days = (datetime.datetime.now() - modification_date).days 
                    if number_of_days > N: 
                        # remove file  
                        os.remove(file_path) 
                        print(f"Deleted file: {file_path}")
                
                for d in dirs:
                    # temp variable to store path of the folder
                    dir_path = os.path.join(root, d)
                    # get the timestamp, when the folder was modified (considering modification time of its contents)
                    timestamp_of_folder_modified = os.path.getmtime(dir_path)
                    # convert timestamp to datetime 
                    modification_date_folder = datetime.datetime.fromtimestamp(timestamp_of_folder_modified)
                    # find the number of days when the folder was modified
                    number_of_days_folder = (datetime.datetime.now() - modification_date_folder).days
                    if number_of_days_folder > N:
                        # remove folder and its contents
                        for root_folder, dirs_folder, files_folder in os.walk(dir_path, topdown=False):
                            for file_folder in files_folder:
                                file_path_folder = os.path.join(root_folder, file_folder)
                                os.remove(file_path_folder)
                                print(f"Deleted file: {file_path_folder}")
                            os.rmdir(root_folder)
                            print(f"Deleted folder: {root_folder}")

        else:
            print(f"Folder '{folder}' not found.")

def main():
    # Example file containing a list of folder paths
    folders_file_path = '/path/to/folders.txt'
    
    # N is the number of days for which we have to check whether the file is older than the specified days or not  
    N = 90

    read_folders_from_file(folders_file_path, N)

if __name__ == "__main__":
    main()


