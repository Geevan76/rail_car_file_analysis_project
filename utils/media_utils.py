import os
import shutil
import pandas as pd

def move_media_files(startpath,media_folder):
    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov']  # Add more media file extensions if needed
    moved_files = []
    duplicate_files = {}

    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() in media_extensions:
                destination_path = os.path.join(media_folder, file)
                if os.path.exists(destination_path):
                    # Handle duplicate media files
                    if file in duplicate_files:
                        duplicate_files[file] += 1
                    else:
                        duplicate_files[file] = 1
                    version = duplicate_files[file]
                    file_name, file_ext = os.path.splitext(file)
                    folder_name = file_name[:7]  # Shorten the folder name to the first 7 characters
                    folder_path = os.path.join(media_folder, "duplicates", folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    if version == 1:
                        new_file_name = file
                    else:
                        new_file_name = f"{file_name}_dup_ver_{version}{file_ext}"
                    duplicate_path = os.path.join(folder_path, new_file_name)
                    shutil.copy2(file_path, duplicate_path)
                    moved_files.append({'File': new_file_name, 'Original Path': file_path, 'Moved To': duplicate_path})
                else:
                    # Move non-duplicate media files
                    shutil.move(file_path, destination_path)
                    moved_files.append({'File': file, 'Original Path': file_path, 'Moved To': destination_path})

    df_moved_files = pd.DataFrame(moved_files)
    return df_moved_files
