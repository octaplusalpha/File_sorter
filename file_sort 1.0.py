import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import shutil
import logging

logging.basicConfig(level=logging.DEBUG)


class FileSorter:
    def __init__(self):
        # initialize the window
        self.window = ctk.CTk()
        # add a title to the window
        self.window.title('File Sorter')
        # set window size
        self.window.geometry("300x400")
        # restrict window sizing
        self.window.resizable(False, False)
        # set padding for the window
        self.padding: dict = {'padx': 20, 'pady': 10}

        # Initialize folder path variable
        self.folder_path = None

        # Set description
        self.description = ctk.CTkLabel(self.window, text='Sort files by creating folders for each file type')
        self.description.grid(row=0, **self.padding)

        # Create the select folder button
        self.select_folder_button = ctk.CTkButton(self.window, corner_radius=5, text='Select Folder',
                                                  command=self.select_folder)
        self.select_folder_button.grid(row=1, **self.padding)

        # Create the sort button
        self.sort_button = ctk.CTkButton(self.window, corner_radius=5, text='Sort', command=self.sort_files)
        self.sort_button.grid(row=2, **self.padding)

        # create a status head label
        self.status_head_label = ctk.CTkLabel(self.window, text='Status:')
        self.status_head_label.grid(row=3, **self.padding)

        # Create the status label
        self.status_label = ctk.CTkLabel(self.window, text='None Sorted', wraplength=300, text_color='red')
        self.status_label.grid(row=4, **self.padding)

    # Create the file select command
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.status_label.configure(text=f'Selected Folder: {self.folder_path}', text_color='green')

    # Function to create a folder for file types
    def create_folder(self, path: str, extension: str):
        folder_name = extension[1:]
        folder_path: str = os.path.join(path, folder_name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        return folder_path

    # Function to sort files
    def sort_files(self):
        if self.folder_path:
            self.status_label.configure(text='Sorting Files...')
            for root_dir, sub_dir, filenames in os.walk(self.folder_path):
                for filename in filenames:
                    file_path: str = os.path.join(root_dir, filename)
                    extension: str = os.path.splitext(filename)[1]

                    if extension:
                        target_folder: str = self.create_folder(self.folder_path, extension)
                        target_path: str = os.path.join(target_folder, filename)
                        shutil.move(file_path, target_path)

            self.remove_empty_folders(self.folder_path)
            self.status_label.configure(text='Files Sorted Successfully!')
        else:
            self.status_label.configure(text='No folder selected.')

    # Function to remove empty folders

    def remove_empty_folders(self, source_path: str):
        for root_dir, sub_dir, filenames in os.walk(source_path, topdown=False):
            for current_dir in sub_dir:
                folder_path: str = os.path.join(root_dir, current_dir)

                if not os.listdir(folder_path):
                    os.rmdir(folder_path)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    fs = FileSorter()
    fs.run()
