import os
import re
import chardet
import pandas as pd
import tkinter as tk
from tkinter import ttk



def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']
  
def search_files(root_folder, exclude_extensions, include_extensions, regex_pattern):
    file_list = []
    total_cnt = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                total_cnt += 1

    cnt = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:  
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if (not exclude_extensions or file_ext not in exclude_extensions) and (not include_extensions or file_ext in include_extensions):
                cnt += 1
                progress_var.set(int(cnt / total_cnt * 100))
                progress_bar.update()
                try:
                    with open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
                        lines = file.readlines()
                        for i, line in enumerate(lines):
                            match = re.search(regex_pattern, line)
                            if match :
                                file_list.append({
                                    'File Path': os.path.relpath(dirpath, root_folder),
                                    'File Name': filename,
                                    'Extension': file_ext,
                                    'Line Count': i,
                                    'Content': match.group(),
                                    'Org-Content': line
                                })
                except (IOError, UnicodeDecodeError):
                    continue
    return file_list

def perform_search(root_folder, exclude_extensions, include_extensions, regex_pattern):
    from tkinter import messagebox
    exclude_extensions = [ext.strip().lower() for ext in exclude_extensions.split(',') if ext.strip()]
    include_extensions = [ext.strip().lower() for ext in include_extensions.split(',') if ext.strip()]
    file_list = search_files(root_folder, exclude_extensions, include_extensions, regex_pattern)

    if file_list:
        df = pd.DataFrame(file_list)
        file_name = "file_search_results.xlsx"
        df.to_excel(file_name, index=False)
        tk.messagebox.showinfo("Search Results", f"Search results saved to: {file_name}")
    else:
        tk.messagebox.showinfo("No Results", "No files found matching the search criteria.")

    progress_var.set(0)
    progress_bar.update()

def main():
    global progress_var, progress_bar
    root = tk.Tk()
    root.title("File Search")

    # 입력 필드 생성
    label_root_folder = tk.Label(root, text="시작할 폴더:")
    entry_root_folder = tk.Entry(root)
    label_exclude_extensions = tk.Label(root, text="제외할 확장자 (comma-separated):")
    entry_exclude_extensions = tk.Entry(root)
    label_include_extensions = tk.Label(root, text="포함할 확장자 (comma-separated):")
    entry_include_extensions = tk.Entry(root)
    label_regex_pattern = tk.Label(root, text="정규식:")
    entry_regex_pattern = tk.Entry(root)

    # 진행율 표시를 위한 요소 추가
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)

    # 버튼 생성
    button_search = tk.Button(root, text="Search", command=lambda: perform_search(
        entry_root_folder.get(),
        entry_exclude_extensions.get(),
        entry_include_extensions.get(),
        entry_regex_pattern.get()
    ))

    # 레이아웃 설정
    label_root_folder.grid(row=0, column=0, padx=5, pady=5)
    entry_root_folder.grid(row=0, column=1, padx=5, pady=5)
    label_exclude_extensions.grid(row=1, column=0, padx=5, pady=5)
    entry_exclude_extensions.grid(row=1, column=1, padx=5, pady=5)
    label_include_extensions.grid(row=2, column=0, padx=5, pady=5)
    entry_include_extensions.grid(row=2, column=1, padx=5, pady=5)
    label_regex_pattern.grid(row=3, column=0, padx=5, pady=5)
    entry_regex_pattern.grid(row=3, column=1, padx=5, pady=5)
    progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    button_search.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
