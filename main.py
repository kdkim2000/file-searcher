import os
import re
import chardet
import pandas as pd
import tempfile
from tqdm import tqdm

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def search_files(root_folder, exclude_extensions, include_extensions, regex_pattern):
    file_list = []
    total_file_cnt = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                total_file_cnt += 1

def search_files(root_folder, regex_pattern, exclude_extensions=None, include_extensions=None):
    file_list = []
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        relative_path = os.path.relpath(dirpath, root_folder)
        total_files += len(filenames)

    with tqdm(total=total_files, unit="files", desc="Processing files") as pbar:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            relative_path = os.path.relpath(dirpath, root_folder)
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_ext = os.path.splitext(filename)[1][1:].lower()
                if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                    try:
                        with open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
                            lines = file.readlines()
                            for i, line in enumerate(lines):
                                if re.search(regex_pattern, line):
                                    file_list.append({
                                        'File Path': relative_path,
                                        'File Name': filename,
                                        'Extension': file_ext,
                                        'Line Count': i,
                                        'Content': line
                                    })
                    except (IOError, UnicodeDecodeError):
                        continue
                pbar.update(1)

    return file_list
def main():
    root_folder = input("시작할 폴더: ")
    exclude_extensions = input("제외할 확장자 (comma-separated): ")
    include_extensions = input("포함할 확장자 (comma-separated): ")
    regex_pattern = input("정규식: ")
    exclude_extensions = [ext.strip().lower() for ext in exclude_extensions.split(',') if ext.strip()]
    include_extensions = [ext.strip().lower() for ext in include_extensions.split(',') if ext.strip()]
    regex_pattern = "r'{}'".format(regex_pattern.replace("`", ""))

    file_list = search_files(root_folder, exclude_extensions, include_extensions, regex_pattern)

    if file_list:
        df = pd.DataFrame(file_list)
        print(df)
        temp_dir = tempfile.TemporaryDirectory()
        file_name = "file_search_results.xlsx"
        temp_filepath = os.path.join(temp_dir.name, file_name)
        df.to_excel(temp_filepath, index=False)
        print(f"Search results saved to: {temp_filepath}")
    else:
        print("No files found matching the search criteria.")

if __name__ == "__main__":
    main()
