import os
import argparse
from utils.file_utils import list_files
from utils.duplicate_utils import copy_duplicate_files
from utils.media_utils import move_media_files
from utils.summary_utils import generate_summary

def main(folder_path):
    try:
        analysis_foldername = os.path.basename(folder_path)
        current_working_dir = os.getcwd()

        # Create multiple directories recursively
        directory_path = f"completed_{analysis_foldername}"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        list_files_csv = f"completed_{analysis_foldername}/{analysis_foldername}_analysis_results.csv"
        duplicate_files_csv = f"completed_{analysis_foldername}/{analysis_foldername}_duplicate_files_data.csv"
        moved_files_csv = f"completed_{analysis_foldername}/{analysis_foldername}_media_files_moved.csv"
        summary_file = f"completed_{analysis_foldername}/{analysis_foldername}_analysis_summary.txt"

        # Perform file analysis
        df_list_files, file_dict = list_files(folder_path)
        df_list_files.to_csv(list_files_csv, index=False)
        print(f"List files data exported to {list_files_csv}.")

        # Perform copying of duplicate files and analysis
        duplicate_folder = f"completed_{analysis_foldername}/{analysis_foldername}_copied_duplicate_files"
        os.makedirs(duplicate_folder, exist_ok=True)
        df_duplicate_files = copy_duplicate_files(file_dict, duplicate_folder)
        df_duplicate_files.to_csv(duplicate_files_csv, index=False)
        print(f"Duplicate files data exported to {duplicate_files_csv}.")

        # Perform moving of media files
        media_folder = f"completed_{analysis_foldername}/{analysis_foldername}_copied_media_files"
        os.makedirs(media_folder, exist_ok=True)
        df_moved_files = move_media_files(folder_path, media_folder)
        df_moved_files.to_csv(moved_files_csv, index=False)
        print(f"Moved files data exported to {moved_files_csv}.")

        # Generate summary
        generate_summary(df_list_files, df_duplicate_files, df_moved_files, summary_file)
        print(f"Summary generated and saved to {summary_file}.")

    except Exception as e:
        print(f"An error occurred during the file analysis process: {e}")
        # Consider logging the error or taking further action here

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a target folder.")
    parser.add_argument("folder_path", help="Path to the target folder.")
    args = parser.parse_args()

    folder_path = args.folder_path
    if not os.path.exists(folder_path):
        print(f"The specified folder does not exist: {folder_path}")
    else:
        main(folder_path)
