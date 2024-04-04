import os
import pandas as pd
from .size_utils import get_size, convert_size

def list_files(startpath):
    data = []
    file_dict = {}
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        folder = os.path.basename(root)
        folder_size = get_size(root)
        folder_size_str = convert_size(folder_size)
        data.append({'Level': level, 'Type': 'Folder', 'Name': folder, 'Path': root, 'FileType': 'Folder', 'Size': folder_size_str, 'Duplicate': ''})
        subindent = ' ' * 4 * (level + 1)
        
        for f in files:
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            file_size_str = convert_size(file_size)
            _, file_ext = os.path.splitext(f)
            
            # Check for duplicate files
            file_key = (f, file_ext[1:])
            if file_key in file_dict:
                duplicate = "Yes"
                file_dict[file_key].append(file_path)
            else:
                duplicate = "No"
                file_dict[file_key] = [file_path]
            
            data.append({'Level': level + 1, 'Type': 'File', 'Name': f, 'Path': file_path, 'FileType': file_ext[1:], 'Size': file_size_str, 'Duplicate': duplicate})
    
    # Update duplicate information for files with multiple occurrences
    for entry in data:
        if entry['Type'] == 'File':
            file_key = (entry['Name'], entry['FileType'])
            if len(file_dict[file_key]) > 1:
                entry['Duplicate'] = "Yes"
    
    return pd.DataFrame(data), file_dict