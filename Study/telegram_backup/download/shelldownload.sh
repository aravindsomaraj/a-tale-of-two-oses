#!/bin/bash

# cat >> output.txt
# python stddownloadtelegram.py | tar -xvf - -C ./

tar -xvf - | sha256sum >> output.txt