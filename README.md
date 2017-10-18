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
pip3 vk_api
sudo apt-get install espeak
sudo apt-get install ffmpeg
```
***
Usage example:
=====================

./{} --user "some_short_link_to_user" "Джони, они на деревьях!"

./{} --chat "DecSec conf" "Эй, кто съел мои чебупели?"

python3 {} --user "https://vk.com/id%some_id%" --file some_music.wav

python3 {} --chat "Гражданская оборона" --file moya_oborona.mp3

***
Options:
=====================
```
--user  "iser_id"	           	link or id to user, who needs to send a message

--chat  "chat name"	         	Name of chate to send a message

--file	filename.wav          Read voice/music form file
```
Note that these are positional arguments, you can not permute them. 
The message must be written in quotes.
