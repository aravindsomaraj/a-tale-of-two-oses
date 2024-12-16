import os, sys
parent_dir  = os.path.abspath(os.getcwd())
print(parent_dir)
sys.path.insert(0, parent_dir)
from telethon import TelegramClient
from utils.configuration import config_extractor
from telethon.tl.types import DocumentAttributeFilename
from progress.progressbar import progress_bar
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Document List")

table.add_column("ID", justify="right", style="cyan", no_wrap=True)
table.add_column("Name", style="magenta")
table.add_column("Size", style="green")

api_id, api_hash, channel_link, session_location = config_extractor.fetchIDHashChannelSession()

client = TelegramClient(session_location, api_id, api_hash)

def pprint_size(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    depth = 0
    while size > 1024:
        size /= 1024
        depth += 1
    return f'{size:.2f}{units[depth]}'

def get_document_name (document):
    for attribute in document.attributes:
        if type(attribute) == DocumentAttributeFilename:
            return attribute.file_name
    return None
async def printMessages(channel):
    async for message in client.iter_messages(channel):
        if message.document:

            table.add_row(str(message.id), get_document_name(message.document), pprint_size(message.document.size))

    console.print(table)


async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    test_channel = await client.get_entity(channel_link)
    # await upload_file_to_channel("./Perilloor Premier League (2024) S01 COMBINED EP(01-07) T.mkv",test_channel)
    # await upload_file_to_channel("./segmentfile.py",test_channel)
    await printMessages(test_channel)
    # await client.send_message(test_channel, '```Hello, myself!```')
    # client.loop.run_until_complete(client.send_message("me", 'test hello'))

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())