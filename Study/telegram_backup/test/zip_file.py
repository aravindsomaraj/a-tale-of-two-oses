import os
import zipfile
from io import BytesIO

def zip_and_chunk(folder_path, chunk_size, destination_folder):
    # Create a folder for the chunks if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Use zipfile to create a zip file
    with BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Walk through the folder and add all files to the zip file
            for foldername, subfolders, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, folder_path))

        # Rewind the buffer to the beginning
        zip_buffer.seek(0)

        # Split the zip file into chunks and write to the file system
        chunk_number = 1
        while True:
            chunk = zip_buffer.read(chunk_size)
            if not chunk:
                break

            chunk_filename = f'chunk_{chunk_number}.zip'
            chunk_filepath = os.path.join(destination_folder, chunk_filename)

            with open(chunk_filepath, 'wb') as chunk_file:
                chunk_file.write(chunk)

            chunk_number += 1

# Example usage
folder_path = './ID'
chunk_size = 3*1024 * 1024  # 3 MB chunks, adjust as needed
destination_folder = './'
zip_and_chunk(folder_path, chunk_size, destination_folder)
