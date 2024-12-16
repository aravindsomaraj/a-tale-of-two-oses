import os
# import pickle as pk
from rich.progress import Progress
from concat_archive import ConcatenatedFiles
from listdocumentstelegram import pprint_size
# import pdb

import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    return total_size


GB = 1024 * 1024 * 1024
MB = 1024 * 1024
KB = 1024

folder_path = '/home/saarang/Downloads/'
folder_size = get_folder_size(folder_path)
print(pprint_size(folder_size))
archive = ConcatenatedFiles(folder_path)



with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=folder_size)

    with open('/home/saarang/down.archive','wb') as file:
        val = archive.read(GB)
        while val:
            file.write(val)
            progress.update(task, advance=len(val))
            val = archive.read(GB)
