#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <file_name>"
    exit 1
fi

file_name=$1

# zip the file
folder="$(basename "$file_name")"
# echo $folder
tar -cf - -C "$file_name/.." "./$folder" | python stduploadtelegram.py "$file_name"