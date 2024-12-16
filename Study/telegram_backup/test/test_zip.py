import os
import shutil
import zipfile
import io

class ConcatenatedBytes:
    def __init__(self, *file_streams):
        self.file_streams = iter(file_streams)
        self.current_stream = next(self.file_streams, None)  # Initialize with the first stream

    def read(self, size=-1):
        if self.current_stream is None:
            return b""  # Return empty bytes if all streams are exhausted

        data = self.current_stream.read(size)
        if not data:
            self.current_stream = next(self.file_streams, None)  # Move to the next stream
            data += self.read(size)  # Recursively read from the next stream if needed
        return data

def extract_zip_from_byte_stream(byte_stream):
    with zipfile.ZipFile(io.BytesIO(byte_stream), 'r') as zip_ref:
        zip_ref.extractall('destination_folder')

with open('./zipped/chunk_1.zip',"rb") as file1, open('./zipped/chunk_2.zip', "rb") as file2:
    concatenated = ConcatenatedBytes(file1, file2)

    extract_zip_from_byte_stream(concatenated)


    # # Read in chunks of 1024 bytes
    # data = concatenated.read(1024)
    # while data:
    #     print(data)  # Process the chunk
    #     data = concatenated.read(1024)


