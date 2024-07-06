from dotenv import load_dotenv
load_dotenv()
import os
import re
import time
import pandas as pd
import tempfile
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="File Searcher", page_icon="👀")

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
                    with open(file_path, 'r', encoding='utf-8') as file:
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

@st.cache_data
def get_regex(prompt):   
    client = OpenAI()
    assistant_id = 'asst_z3EJn8lrcE2zBxRZWxTydCqH'
    thread_id = ""
    if 'thread_id' not in st.session_state:
        thread = client.beta.threads.create()
        # print(thread)
        st.session_state.thread_id = thread.id
    thread_id = st.session_state.thread_id
    
    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role="user",
        content=prompt,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while run.status != 'completed' :
        time.sleep(0.1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
    messages = client.beta.threads.messages.list(thread_id=thread_id, run_id = run.id)
    regex_pattern = messages.data[0].content[0].text.value
    return regex_pattern
    
def main():
    st.title(":ladybug:")
    root_folder = st.text_input("시작할 폴더")
    exclude_extensions = st.text_input("제외할 확장자 (comma-separated):")
    include_extensions = st.text_input("포함할 확장자 (comma-separated):")
    prompt = st.text_input("검색하고 싶은 내용을 입력하세요")
    
    regex_pattern= ""
    if len(prompt) > 0:
        regex_pattern = get_regex(prompt)
    regex_pattern = st.text_input("정규식:", value=regex_pattern)
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
