import os, math, sys, hashlib
parent_dir  = os.path.abspath(os.getcwd())
# print(parent_dir)
sys.path.insert(0, parent_dir)
from telethon import TelegramClient
from progress.progressbar import *
from utils.configuration import config_extractor
from tqdm import tqdm
from archiver.concat_archive import ConcatenatedFiles
from utils.listdocumentstelegram import pprint_size

# Use your own values from my.telegram.org
api_id, api_hash, channel_link, session_location = config_extractor.fetchIDHashChannelSession()

client = TelegramClient(session_location, api_id, api_hash)

async def upload_file_to_channel(file_name, channel,chunk_size = 1*1024 * 1024 * 1024): # 1GB
    file_name = os.path.normpath(file_name)

    if(os.path.isfile(file_name)):
        file_size = os.path.getsize(file_name)
        p_bar = progress_bar(file_size)
        total_segments = math.ceil (file_size / chunk_size)

        print(f"Segmenting {file_name} to {total_segments} segments")
        with open(file_name, 'rb') as file:
            offset = 0
            i = 0
            chunk_list = []
            while offset < file_size:

                chunk = file.read(chunk_size)
                up_chunk = await client.upload_file(chunk,file_name=f"{file_name}_segment{i}",progress_callback=p_bar.update_progress)
                chunk_list.append(up_chunk)
                offset += len(chunk)
                i += 1
            caption = f"**{file_name}** ; **{total_segments}** segments; {pprint_size(file_size)}"
            await client.send_file(channel, chunk_list,caption=caption,force_document=True)

    elif(os.path.isdir(file_name)):
        archive = ConcatenatedFiles(file_name)
        file_size = archive.size() # Get total size of archive
        p_bar = progress_bar(file_size)
        total_segments = math.ceil (file_size / chunk_size)

        display_name = os.path.basename(file_name)

        print(f"Segmenting {display_name} to {total_segments} segments!")
        offset = 0
        i = 0
        # chunk_list = []
        
        while offset < file_size:
            print(f"Uploading segment {i} of {total_segments}")
            chunk = archive.read(chunk_size)
            if (i>3):
                hash_object = hashlib.sha256(chunk)
                hash_value = hash_object.hexdigest()

                up_chunk = await client.upload_file(chunk,file_name=f"{display_name}_segment{i}",progress_callback=p_bar.update_progress)
                caption = f"**{display_name}** | Segment **{i}** of **{total_segments}** | **{pprint_size(len(chunk))}** | hash *{hash_value}*"
                # print(caption)
                await client.send_file(channel, up_chunk,caption=caption ,force_document=True)
            # chunk_list.append(up_chunk)
            offset += len(chunk)
            i += 1
        # caption = f"**{display_name}**| **{total_segments}** segments| **{pprint_size(file_size)}**"
    else:
        print(f"{file_name} is not a file or directory.")

async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    channel = await client.get_entity(channel_link)
    file_name = None
    chunk_size = 1*1024 * 1024 * 1024
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    elif len(sys.argv) > 2:
        chunk_size = int(sys.argv[2])
        file_name = sys.argv[1]


    if file_name == None:
        print("Please specify a file name")
        return

    await upload_file_to_channel(file_name,channel,chunk_size=chunk_size)
    '''
    await upload_file_to_channel("./segmentfile.py",test_channel)
    await client.send_message(test_channel, '```Hello, myself!```')
    client.loop.run_until_complete(client.send_message("me", 'test hello'))
    '''

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())