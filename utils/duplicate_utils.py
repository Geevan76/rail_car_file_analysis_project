import os
import shutil
import pandas as pd

def copy_duplicate_files(file_dict, duplicate_folder):
    data = []
    for file_key, file_paths in file_dict.items():
        if len(file_paths) > 1:
            file_name, file_ext = file_key
            folder_name = file_name[:7]  # Shorten the folder name to the first 7 characters
            folder_path = os.path.join(duplicate_folder, folder_name)
            
            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            
            duplicate_names = []
            for i, file_path in enumerate(file_paths, start=1):
                if i == 1:
                    # Keep the original file name for the first duplicate
                    new_file_name = file_name
                else:
                    # Add "_dup_ver_(n)" before the file extension for subsequent duplicates
                    new_file_name = f"{os.path.splitext(file_name)[0]}_dup_ver_{i-1}.{file_ext}"
                
                new_file_path = os.path.join(folder_path, new_file_name)
                shutil.copy2(file_path, new_file_path)
                
                if i > 1:
                    duplicate_names.append(new_file_name)
            
            data.append({'File Name': file_name, 'Duplicate Names': ', '.join(duplicate_names), 'Source Path': file_paths[0]})
    
    return pd.DataFrame(data)
