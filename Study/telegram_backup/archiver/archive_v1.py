import os
import argparse
import json
# import pickle as pk

class archiver:
    def __init__(self, folder_name) -> None:
        
        # pre-processing foldername
        self.folder_abs_path = folder_name
        self.folder_abs_path = os.path.normpath(self.folder_abs_path)
        self.folder_abs_path = os.path.abspath(self.folder_abs_path)
        self.folder_abs_path = self.folder_abs_path.replace("\\","/")

        # storing only the folder name. Only the name of the top folder
        self.folder_name = os.path.basename(self.folder_abs_path)

        self.parent_folder = os.path.dirname(self.folder_abs_path)   

        self.files_abs_path = []
        self.files_rel_path = []

        for foldername, subfolders, filenames in os.walk(self.folder_abs_path):

            for filename in filenames:
                file_abs_path = os.path.join(folder_name, filename)
                file_rel_path = os.path.relpath(file_abs_path,self.parent_folder)
                file_size = os.path.getsize(file_abs_path)

                self.files_abs_path.append((file_abs_path, file_size))
                self.files_rel_path.append((file_rel_path, file_size))

        files_list_dump = json.dumps(self.files_rel_path).encode()
        files_list_dump_size = len(files_list_dump).to_bytes(8, byteorder='big')
        self.header = files_list_dump_size + files_list_dump
        self.num_files = len(self.files_abs_path)
        
        # starting location of each file
        self.file_start_addr = [len(self.header)]
        for i in range(1,len(self.num_files)):
            file_name, _ = self.files_abs_path[i]
            _, prev_size = self.files_abs_path[i]
            self.file_start_addr.append((file_name,self.file_start_addr[i-1] + prev_size))
             
        
        

    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process files')
    # parser.add_argument('--dest', type=str, nargs='?', default=None, help='Specify the destination folder name.')
    parser.add_argument('--src', type=str, nargs='?', default=None, help='Specify the src file name.')

    args = parser.parse_args()
    # folder_name = args.dest
    archive_name = args.src

    if(archive_name != None):
        archive = archiver(archive_name)
        # print(archive.folder_abs_path)
        # print(archive.parent_folder)
        # print(archive.folder_name)
    else:
        print("Please specify a source.")