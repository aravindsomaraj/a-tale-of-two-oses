

import os, math, sys, hashlib
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))  # replace '..' if needed
sys.path.insert(0, parent_dir)
from telethon import TelegramClient
from progressbar import *
from configuration import config_extractor
from tqdm import tqdm
from concat_archive import ConcatenatedFiles
from utils import *
from datetime import datetime
import argparse                                                                                                        

# Use your own values from my.telegram.org
api_id, api_hash, channel_link = config_extractor.fetchIDHashChannel()

client = TelegramClient('saarang', api_id, api_hash)

def file_info(file_name,size,segments) -> str:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return f"**{file_name}** \n size: **{pprint_size(size)}** \n segments: **{segments}** \n Date: {datetime.now().strftime(now)}"

async def upload_data(data_chunk,name,caption,channel,p_bar):
    print(name,pprint_size(len(data_chunk)))
    print(caption)
    # with open(name, 'wb') as file:
    #     file.write(data_chunk)
    up_chunk = await client.upload_file(data_chunk,file_name=f"{name}",progress_callback=p_bar.update_progress)
    # await client.send_file(channel, up_chunk, caption=caption, force_document=True)
    return up_chunk

async def upload_file_to_channel(file_name, channel,chunk_size = GB): # 1GB
    file_name = os.path.normpath(file_name)
    file_name = os.path.abspath(file_name)
    display_name = os.path.basename(file_name)

    file_size = folder_size(file_name)
    total_segments = math.ceil (file_size / chunk_size)

    p_bar = progress_bar(file_size)
    print(file_name, pprint_size(file_size))
    segment_list = []
    caption_list = []
    await client.send_message(channel, file_info(display_name,file_size,total_segments))
    i = 0
    while True:
        data_chunk = sys.stdin.buffer.read(chunk_size)
        hash_object = hashlib.sha256(data_chunk)
        hash_value = hash_object.hexdigest()
        caption = f"**{display_name}** | **{i+1}**/**{total_segments}** | **{pprint_size(len(data_chunk))}** | hash: {hash_value}"
        
        if not data_chunk:
            break  # Break the loop if there's no more data
        segment_list.append(await upload_data(data_chunk,f"{display_name}_0{i}.part",caption,channel,p_bar))
        caption_list.append(caption)
        i += 1
    await client.send_file(channel, segment_list, caption=caption_list, force_document=True)
    
async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    channel = await client.get_entity(channel_link)
    file_name = None
    chunk_size = GB
    
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    elif len(sys.argv) > 2:
        # chunk_size = int(sys.argv[2])
        file_name = sys.argv[1]

    if file_name == None:
        print("Please specify a file name")
        return

    await upload_file_to_channel(file_name,channel,chunk_size=chunk_size)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())