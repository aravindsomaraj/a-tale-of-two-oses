import os
import shutil
import zipfile
import io

class ConcatenatedFiles(io.RawIOBase):
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.current_index = 0
        self.current_file = None
        self._open_next_file()

    def _open_next_file(self):
        if self.current_file:
            self.current_file.close()
        if self.current_index < len(self.file_paths):
            self.current_file = open(self.file_paths[self.current_index], 'rb')
            self.current_index += 1
        else:
            self.current_file = None

    def read(self, size=-1):
        if self.current_file is None:
            return b''  # No more files to read

        data = self.current_file.read(size)
        while not data:
            # Switch to the next file if the current one is fully read
            self._open_next_file()
            if self.current_file:
                data = self.current_file.read(size)
            else:
                break
        return data

def extract_zip_from_byte_stream(byte_stream):
    with zipfile.ZipFile(io.BytesIO(byte_stream), 'r') as zip_ref:
        zip_ref.extractall('destination_folder')

# Example usage
file_paths = ['./zipped/chunk_1.zip', './zipped/chunk_2.zip', './zipped/chunk_3.zip']

concatenated_file = ConcatenatedFiles(file_paths)


extract_zip_from_byte_stream(concatenated_file)

# Now you can use 'concatenated_file' like a regular file object
# Reading from it will seamlessly continue through all the files in the list.
# data_chunk = concatenated_file.read(1024)


def restore_from_chunks(chunk_folder, output_folder):
    # Create the output folder if it doesn't exist

    os.makedirs(output_folder, exist_ok=True)

    # Get the list of chunk files
    chunk_files = sorted([f for f in os.listdir(chunk_folder) if f.startswith('chunk_') and f.endswith('.zip')])

    # Iterate through the chunks and extract the content
    for chunk_file in chunk_files:
        with zipfile.ZipFile(os.path.join(chunk_folder, chunk_file), 'r') as zip_file:
            zip_file.extractall(output_folder)



# Example usage
chunk_folder = './zipped'
output_folder = './extracted'
# restore_from_chunks(chunk_folder, output_folder)
