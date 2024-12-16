import os 
GB = 1024 * 1024 * 1024
MB = 1024 * 1024
KB = 1024

def folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

def pprint_size(size):
    if size > GB:
        return f"{size/GB:.2f} GB"
    elif size > MB:
        return f"{size/MB:.2f} MB"
    elif size > KB:
        return f"{size/KB:.2f} KB"
    else:
        return f"{size} B"  