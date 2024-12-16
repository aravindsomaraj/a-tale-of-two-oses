from telethon import TelegramClient
from configuration import config_extractor
from telethon.tl.types import DocumentAttributeFilename
from progressbar import progress_bar
import argparse
from listdocumentstelegram import pprint_size

api_id, api_hash = config_extractor.fetchIDandHash()

client = TelegramClient('saarang', api_id, api_hash)

def parse_integer_range(range_str):
    # Function to parse a range string and return a list of integers
    start, end = map(int, range_str.split('-'))
    return list(range(start, end + 1))

def get_document_name (document):
    for attribute in document.attributes:
        if type(attribute) == DocumentAttributeFilename:
            return attribute.file_name
    return None

# async def printMessages(channel):
#     file_list = []
#     async for message in client.iter_messages(channel):
#         if message.document:
#             if(message.id<=16 and message.id>=14):
#                 file_list.insert(0,message)

#         #     print(message.id, get_document_name(message.document))
#         # else:
#         #     print(message.id, message.text)

#     await download_file(channel,file_list,"./test.mkv")

async def returnMessages(channel, message_ids: list):
    file_list = []
    async for message in client.iter_messages(channel, ids=message_ids):
        if message.document:
            file_list.insert(0, message)
    
    file_list.sort(key=lambda message: message.id)  # Sort file_list in ascending order of message_ids
    return file_list


async def download_file(channel, file_name, messages_ids: list):
    file_size = 0
    messages = await returnMessages(channel, messages_ids)
    if(file_name==None):
        original_string = get_document_name(messages[0].document)
        file_name = original_string.split('_segment')[0]
    
    print("Downloading and merging files of ids",end=" ")
    for message in messages:
        if message.document:
            file_size += message.document.size
            print(message.id,end=" ")
    print()

    p_bar = progress_bar(file_size,description="Downloading...",color="yellow")
    print(f"Downloading {len(messages)} files to {file_name} of total size {pprint_size(file_size)}")
    
    with open(file_name, 'wb') as file:
        for message in messages:
            if message.document:
                blob = await message.download_media(bytes,progress_callback=p_bar.update_progress)
                file.write(blob)
            # else:
            #     print("Not a document: ",message.id, message.text)

async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    
    parser = argparse.ArgumentParser(description='Process files and a list of integers.')

    parser.add_argument('--file_name', type=str, nargs='?', default=None, help='Specify the file name.')
    parser.add_argument('--ids', type=parse_integer_range, help='Specify a range of integers (e.g., 1-5).')
    parser.add_argument('--folder', action='store_true', help='Specify if the file is a folder.')

    args = parser.parse_args()

    file_name = args.file_name
    message_ids = args.ids

    test_channel = await client.get_entity('https://t.me/+gs8Z_VnqR00wMWY1')

    await download_file(test_channel,file_name,message_ids)
    
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())