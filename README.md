# auto-aither
## What is this?
auto-aither is a python3 script which provides a convenient and easy to use interface for each step of the torrent upload process. This includes 
- .torrent file generation 
- taking and uploading screenshots and mediainfo
- proper naming and categorisation

It can then upload all this directly to aither.cc. You can also use the script in a modular fashion if you just want to do one certain thing.

## Installation
> git clone https://github.com/Ser4ph2/auto-aither.git

> cd auto-aither

> pip3 install -r requirements.txt

> chmod +x main.py

> ./main.py

Obviously you will need Python3 and pip3 installed. To install these:
> apt install python3

> apt install python3-pip

## FAQ
- What is my PID and where do I find it?

Your PID allows the tracker to identify you in the swarm. This is how it tracks your upload/download amount etc. If someone else discovers your PID they could download torrents using it and all data transfer would be attributed to your account.

Your PID can be located by clicking your profile picture in the top right > Security > Pass Key

- What is my API key and where do I find it?

Your API key is a unique token that allows your account to authenticate with the site without the usual username/password. This is useful in scripts such as this where it is easier not to.

Your API key can be located by clicking your profile picture in the top right > Security > API Token

## Bugs / Suggestions / Further Questions
Please feel free to either PM me on aither.cc, discord or open a github issue. Contributions are encouraged :)
