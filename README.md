# vk-audio-messager
Send text-to-speech voice and music via audio message.

You need to configure this in **config.json** file
***
requirements
=====================

* vk_api
* espeak
* ffmpeg

install requirements
=====================
```
pip3 install vk_api
sudo apt-get install espeak
sudo apt-get install ffmpeg
```
***
Usage example:
=====================

./ausio_messager.py --user="some_short_link_to_user" --text="Джони, они на деревьях!"

./ausio_messager.py --chat="DecSec conf" -t "Эй, кто съел мои чебупели?"

python3 ausio_messager.py -u "https://vk.com/id%some_id%" --file=some_music.wav

python3 ausio_messager.py -ch "Гражданская оборона" -f moya_oborona.mp3

***
Options:
=====================
```
  -h, --help            				show this help message and exit

  -u USER, --user=USER  				link or id to user, who needs to send a message

  -c CHAT, --chat=CHAT					Name of chate to send a message

  -f FILE, --file=FILE 					Read voice/music form file

  -t "Some QUOTED text", --text="Some QUOTED text" 	Voice this text by robot
```
Note that these are positional arguments, you can not permute them. 
The message must be written in quotes.
