import os
import pickle as pk
import argparse
import json


# folder_path = './ID'

class ConcatenatedFiles:
    def __init__(self,foldername) -> None:
        self.foldername = foldername
        self.file_info = []
        self.files = []
        self.file_start_index = []
        self.files_full_path = []
        parent_folder = os.path.basename(os.path.normpath(foldername))

        for foldername, subfolders, filenames in os.walk(foldername):

            for filename in filenames:
                rel_path_folder = os.path.join(os.path.relpath(foldername, self.foldername))
                rel_path_file = os.path.normpath(os.path.join(parent_folder,rel_path_folder,filename))
                
                fullname = os.path.join(foldername, filename)
                self.files_full_path.append(fullname)
                filesize = os.path.getsize(fullname)
                self.files.append((rel_path_file,filesize))
                if(len(self.file_start_index) == 0):
                    self.file_start_index.append(filesize)
                else:
                    self.file_start_index.append(self.file_start_index[-1]+filesize)

        self.file_info = pk.dumps(self.files)
        self.sizeof_file_info = (len(self.file_info)).to_bytes(8, byteorder='big')
        self.header = self.sizeof_file_info + self.file_info

        for i in range(len(self.file_start_index)):
            self.file_start_index[i] += len(self.header)
        self.file_start_index.insert(0,len(self.header))
        self.file_start_index.pop()
        if(self.files!=[]):
            self.full_size = self.file_start_index[-1] + os.path.getsize(self.files_full_path[-1])
        else:
            self.full_size = 0
        self.current_index = 0
        self.completed = False
    
    # returns the file to start reading from, the index to start reading from, the file to end reading from, the index to end reading from
    def _find_files_to_read(self, size) :

        start_file = None   # file to start reading from
        start_index = None  # index to start reading from

        end_file = None     # file to end reading from 
        end_index = None    # index to end reading from

        # computing start file and start index
        for i in range(len(self.file_start_index)-1,-1,-1):
            if self.current_index >= self.file_start_index[i]:
                start_file = i  # file to start reading from
                start_index = self.current_index - self.file_start_index[i]
                break
        
        if start_file == None:
            # safety check, this if case should always be true
            if self.current_index < self.file_start_index[0]:
                start_file = -1
                start_index = self.current_index
            else:
                raise Exception('start_file is None, this should not happen')
        
        if size == -1:
            end_file = len(self.file_start_index)-1
            end_index = -1
        else:
            # computing end file and end index
            for i in range(0,len(self.file_start_index)):
                if self.current_index + size <= self.file_start_index[i]:
                    end_file = i-1
                    if end_file == -1:
                        end_index = self.current_index + size
                    else:
                        end_index = self.current_index + size - self.file_start_index[i-1]
                    break

            if end_file == None:
                # safety check, this if case should always be true
                if self.current_index + size > self.file_start_index[-1]:
                    end_file = len(self.file_start_index)-1
                    end_index = self.current_index + size - self.file_start_index[-1]
                else:
                    raise Exception('end_file is None, this should not happen')
        
        # print(f"start_file: {start_file}, start_index: {start_index}, end_file: {end_file}, end_index: {end_index}")
        # print(f"current_index: {self.current_index}, size: {size}")
        # print(f"header_length: {len(self.header)}")
        # print(f"start_file_index: {self.file_start_index}")
        # print("-"*50)
        
        if start_file == None or end_file == None:
            raise Exception('start_file or end_file is None, this should not happen')

        return start_file, start_index, end_file, end_index 

    def read(self, size=-1) -> bytes:
        header_size = len(self.header)
        
        if self.completed:
            return b'' 

        if size < -1:
            raise Exception('size cannot be less than -1')
        elif size == 0:
            return b''


        start_file, start_index, end_file, end_index = self._find_files_to_read(size)    
        # print(start_file, start_index, end_file, end_index)
        if start_file == end_file:
            if(start_file == -1):
                self.current_index += size
                if end_index == -1: #this case should not happen
                    read_bytes = self.header[start_index:]
                else:
                    read_bytes = self.header[start_index:end_index]
            else:
                with open(self.files_full_path[start_file], 'rb') as f:
                    f.seek(start_index)
                    if end_index == -1:     
                        read_bytes = f.read()
                    else:
                        read_bytes = f.read(end_index - start_index)
                    self.current_index += size
        else:
            if(start_file == -1):
                read_bytes = self.header[start_index:]
                for i in range(start_file+1, end_file):   # start_file+1 = 0, always in this case
                    read_bytes += open(self.files_full_path[i], 'rb').read()
                with open(self.files_full_path[end_file], 'rb') as f:
                    read_bytes += f.read(end_index)
            else:
                with open(self.files_full_path[start_file], 'rb') as f:
                    f.seek(start_index)
                    read_bytes = f.read()
                for i in range(start_file+1, end_file):
                    read_bytes += open(self.files_full_path[i], 'rb').read()
                with open(self.files_full_path[end_file], 'rb') as f:
                    read_bytes += f.read(end_index)
            
            self.current_index += size

        if(self.current_index >= self.full_size):
            self.completed = True
        return read_bytes
    
    def seek(self, offset, whence=0):
        if whence == 0:
            self.current_index = offset
        elif whence == 1:
            self.current_index += offset
        elif whence == 2:
            self.current_index = self.full_size + offset
        else:
            raise Exception('whence can only be 0, 1 or 2')

        if self.current_index >= self.full_size:
            self.completed = True

    def size(self):
        return self.full_size

def store(folder_path):
    files = []

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            fullname = os.path.join(foldername, filename)
            filesize = os.path.getsize(fullname)
            files.append((fullname,filesize))

    list_bytes = pk.dumps(files)
    len_list_bytes = (len(list_bytes)).to_bytes(8, byteorder='big')

    # print(len_list_bytes)
    # files_restored = pk.loads(list_bytes)

    # for file in files_restored:
    #     print(file)

    with open('files_arc.archive', 'wb') as f:
        f.write(len_list_bytes+list_bytes)
        for file_name, size in files:
            with open(file_name, 'rb') as f1:
                f.write(f1.read())

def create_parent_directory(file_path):
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

def restore(archive_name,restore_folder):
    with open(archive_name, 'rb') as f:
        len_list_bytes = f.read(8)
        len_list = int.from_bytes(len_list_bytes, byteorder='big')
        list_bytes = f.read(len_list)
        files_restored = pk.loads(list_bytes)
        # for file in files_restored:
        #     print(file)

        # temp = f.read(4)
        # print(temp)
        # if temp == b'':
        #     print('empty')
        # else:
        #     print('not empty')

        for file_name, size in files_restored:
            join_name = os.path.join(restore_folder,file_name )
            print(join_name)
            create_parent_directory(join_name)
            with open(join_name, 'wb') as f1:
                f1.write(f.read(size))

        temp = f.read(4)

        if temp == b'':
            print('completed')
        else:
            print('restoration incomplete')
    
class RecoverConcatnateFiles():
    def __init__(self) -> None:
        self.len_list = None
        self.files_info = None
        self.restoration_started = False
        self.headers_acquired = False
        self.current_index = (0,0)  # (file_index, index_in_file) 
    
    def restore(self,archive_name:str,dest_fldr:str):
        with open(archive_name, 'rb') as f:
            self.len_list = int.from_bytes(f.read(8), byteorder='big')
            
            self.files_info = pk.loads(f.read(self.len_list))

            for file_name, size in self.files_info:
                join_name = os.path.join(dest_fldr,file_name )
                print(join_name)
                create_parent_directory(join_name)
                with open(join_name, 'wb') as f1:
                    f1.write(f.read(size))

            temp = f.read(4)

            if temp == b'':
                print('Restoration completed')
            else:
                print('Restoration incomplet!!')

    def partial_resotre(self,part_arc:bytes,dest_fldr:str):
        
        if not self.restoration_started:
            if(len(part_arc)>=8):
                self.len_list = int.from_bytes(part_arc[:8], byteorder='big')
            else:
                raise Exception('Invalid archive or handling such archive not supported')
            
            if len(part_arc)>=8+self.len_list:
                self.files_info = pk.loads(part_arc[8:self.len_list+8])
                self.restoration_started = True
                self.headers_acquired = True
            else:
                raise Exception('Invalid archive or handling such archive not supported')
                
            if self.headers_acquired:
                i = self.len_list+8
                for file_name, size in self.files_info:
                    join_name = os.path.join(dest_fldr,file_name)
                    print(join_name)
                    create_parent_directory(join_name)
                    if(len(part_arc)>=i+size):
                        with open(join_name, 'wb') as f1:
                            f1.write(part_arc[i:i+size])
                        i+=size
                    else:
                        with open(join_name, 'wb') as f1:
                            f1.write(part_arc[i:])
                        self.current_index = (self.files_info.index((file_name,size)),len(part_arc[i:]))
                        break
            else:
                raise Exception('Something went wrong, headers not acquired')
        else:

            current_file_index, current_index_in_file = self.current_index 

            file_name, size = self.files_info[current_file_index]
            join_name = os.path.join(dest_fldr,file_name)
            print(join_name)
            create_parent_directory(join_name)
            if(len(part_arc)>=size-current_index_in_file):
                with open(join_name, 'ab') as f1:
                    f1.write(part_arc[:size-current_index_in_file])
                i = size-current_index_in_file
                if(current_file_index+1<len(self.files_info)):
                    self.current_index = (current_file_index+1,0)
                    for file_name, size in self.files_info[current_file_index+1:]:
                        join_name = os.path.join(dest_fldr,file_name)
                        print(join_name)
                        create_parent_directory(join_name)
                        if(len(part_arc)>=i+size):
                            with open(join_name, 'wb') as f1:
                                f1.write(part_arc[i:i+size])
                            i+=size
                        else:
                            with open(join_name, 'wb') as f1:
                                f1.write(part_arc[i:])
                            self.current_index = (self.files_info.index((file_name,size)),len(part_arc[i:]))
                            break

            else:
                with open(join_name, 'wb') as f1:
                    f1.write(part_arc)
                self.current_index = (self.files_info.index((file_name,size)),len(part_arc)+current_index_in_file)

        

if __name__ == '__main__':
    # store('./ID')

    parser = argparse.ArgumentParser(description='Process files and a list of integers.')
    parser.add_argument('--dest', type=str, nargs='?', default=None, help='Specify the destination folder name.')
    parser.add_argument('--src', type=str, nargs='?', default=None, help='Specify the src file name.')

    args = parser.parse_args()
    folder_name = args.dest
    archive_name = args.src

    restore(archive_name=archive_name,restore_folder=folder_name)