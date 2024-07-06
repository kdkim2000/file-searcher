# from dotenv import load_dotenv
# load_dotenv()
import os
import re
import time
import chardet
import pandas as pd
import tempfile
import streamlit as st

st.set_page_config(page_title="File Searcher", page_icon="👀")

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def search_files(root_folder, exclude_extensions, include_extensions, regex_pattern):
    file_list = []
    progress_bar = st.progress(0, text=root_folder)
    index = 0
    totla_file_cnt = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in  filenames:
            file_path = os.path.join(dirpath, filename)           
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                totla_file_cnt += 1
            
    for dirpath, dirnames, filenames in os.walk(root_folder):
        relative_path = os.path.relpath(dirpath, root_folder)
        for filename in  filenames:
            file_path = os.path.join(dirpath, filename)           
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                index += 1                
                progress_bar.progress(int(100 * index / totla_file_cnt), file_path)  
                relative_path = os.path.relpath(file_path, root_folder)  
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

    return file_list

def main():
    st.title("👀")
    root_folder = st.text_input("시작할 폴더:")
    exclude_extensions = st.text_input("제외할 확장자 (comma-separated):")
    include_extensions = st.text_input("포함할 확장자 (comma-separated):")
    regex_pattern = st.text_input("정규식:")
    regex_pattern = "r'{}'".format(regex_pattern.replace("`",""))

    if st.button("Search Files"):
        exclude_extensions = [ext.strip().lower() for ext in exclude_extensions.split(',') if ext.strip()]
        include_extensions = [ext.strip().lower() for ext in include_extensions.split(',') if ext.strip()]
        file_list = search_files(root_folder, exclude_extensions, include_extensions, regex_pattern)

        if file_list:
            df = pd.DataFrame(file_list)         
            st.write(df)
            temp_dir = tempfile.TemporaryDirectory()
            file_name="file_search_results.xlsx"
            temp_filepath = os.path.join(temp_dir.name, file_name)
            df.to_excel(temp_filepath, index=False)
            st.download_button(
                label="Download as Excel",
                data=temp_filepath,
                file_name=file_name,
                mime="application/vnd.ms-excel",
            )
        else:
            st.write("No files found matching the search criteria.")

if __name__ == "__main__":
    main()
