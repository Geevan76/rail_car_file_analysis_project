from .size_utils import convert_size

def generate_summary(df_list_files, df_duplicate_files, df_moved_files, summary_file):
    total_files = len(df_list_files)
    total_folders = df_list_files['Type'].value_counts()['Folder']
    total_duplicates = len(df_duplicate_files)
    total_moved_files = len(df_moved_files)

    summary_text = f"File Analysis Summary\n\n"
    summary_text += f"Total Files: {total_files}\n"
    summary_text += f"Total Folders: {total_folders}\n"
    summary_text += f"Total Duplicate Files: {total_duplicates}\n"
    summary_text += f"Total Moved Media Files: {total_moved_files}\n\n"

    summary_text += "File Types Distribution:\n"
    file_types_count = df_list_files['FileType'].value_counts()
    for file_type, count in file_types_count.items():
        summary_text += f"{file_type}: {count}\n"

    # Convert 'Size' column to numeric dtype
    df_list_files['Size'] = df_list_files['Size'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) else x)

    summary_text += "\nTop 10 Largest Files:\n"
    largest_files = df_list_files[df_list_files['Type'] == 'File'].nlargest(10, 'Size')
    for _, row in largest_files.iterrows():
        summary_text += f"{row['Name']} - {convert_size(row['Size'])}\n"

    summary_text += "\nDuplicate Files:\n"
    for _, row in df_duplicate_files.iterrows():
        summary_text += f"Original: {row['File Name']}\n"
        summary_text += f"Duplicates: {row['Duplicate Names']}\n"
        summary_text += f"Source Path: {row['Source Path']}\n\n"

    summary_text += "Moved Media Files:\n"
    for _, row in df_moved_files.iterrows():
        summary_text += f"{row['File']} - Moved from: {row['Original Path']} to: {row['Moved To']}\n"

    with open(summary_file, 'w') as file:
        file.write(summary_text)