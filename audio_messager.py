#!/usr/bin/python3
import requests
import vk_api
import os
import sys
import subprocess
import json

class Messager:
	def __init__(self):
		prog = sys.argv[0]
		helper = """
Usage example:

./audio_messager.py --user "some_short_link_to_user" "Джони, они на деревьях!"

./audio_messager.py --chat "DecSec conf" "Эй, кто съел мои чебупели?"

python3 audio_messager.py --user "https://vk.com/id%some_id%" --file some_music.wav

python3 audio_messager.py --chat "Гражданская оборона" --file moya_oborona.mp3


Options:
--user		link or id to user, who needs to send a message
--chat		Name of chate to send a message
--file		Read voice/music form file

Note that these are positional arguments, you can not permute them. 
The message must be written in quotes.
"""

		options = json.loads(open("config.json").read(), encoding='utf-8')

		auth = self.auth(options)
		
		try:
			if sys.argv[3] == "--file":
				voice = "message.wav"
				subprocess.call('ffmpeg -i {} -map_channel 0.0.0 {}'.format(sys.argv[4], voice), shell=True)
				uploaded_voice = self.upload_file(voice, auth)
			else:
				voice = self.create_voice(sys.argv[3])
				uploaded_voice = self.upload_file(voice, auth)

			if sys.argv[1] == "--user":
				user_id = self.get_user_id(sys.argv[2], auth)
				self.send_msg(uploaded_voice, user_id, auth)
			elif sys.argv[1] == "--chat":
				chat = self.get_chat_id(sys.argv[2], auth)
				self.send_chat_msg(uploaded_voice, chat, auth)
			print("Done")

		except IndexError:
			print("Incorrect input.")
			print(helper)
			sys.exit(0)

		except FileNotFoundError:
			print("File not found.")
			sys.exit(0)
			
		
	def create_voice(self, message):
		file_name = "message.wav"
		cmd_1 = 'espeak -vru -s3 -z "{}" -w prepare.wav'.format(message)
		cmd_2 = 'ffmpeg -i prepare.wav -map_channel 0.0.0 {}'.format(file_name)
		subprocess.call(cmd_1, shell=True)
		subprocess.call(cmd_2, shell=True)
		os.system("rm prepare.wav")
		return file_name
	
	def auth(self, options):
		try:
			login = options["login"]
			password = options["password"]
		except:
			print("You need to specify login and password in \nconfig.json\" file")
			sys.exit(0)

		try:
			vk = vk_api.VkApi(login=login, password=password)
			vk.auth()
			return vk
		except:
			print("Login failed. Check validation of your login and password in \"config.json\"")
			sys.exit(0)

	def upload_file(self, path, vk):
		audio = {'file': (path, open(path, 'rb'))}
		upload_url = vk.method('docs.getMessagesUploadServer', {'type': 'audio_message'})['upload_url']
		#print(upload_url)
		upload = requests.post(upload_url, files=audio)
		result = json.loads(upload.text)['file']
		#print(result)
		#print(result+'\n')

		saved = vk.method('docs.save', {'file': result, 'title': 'voice_message.ogg'})[0]
		os.system("rm -R {}".format(path))
		#print(saved)
		#print(msg)
		return saved

	def get_user_id(self, link, vk):
		id = link
		if 'vk.com/' in link:
			id = link.split('/')[-1]
		if not id.replace('id', '').isdigit():
			id = vk.method('users.get', {'user_ids':id})[0]['id']
		else:
			id = id.replace('id', '')
		#print('user_id: ', id)
		return int(id)

	def get_chat_id(self, link, vk):
		chats = vk.method("messages.searchDialogs", {"q": link})
		for chat in chats:
			if chat['type'] == 'chat':
				return chat['id']
		

	def send_msg(self, msg, user_id, vk):
		attach = 'doc%s_%s' % (msg['owner_id'], msg['id'])
		#print(attach)
		vk.method('messages.send',{'user_id': user_id, 'attachment': attach})

	def send_chat_msg(self, msg, chat_id, vk):
		attach = 'doc%s_%s' % (msg['owner_id'], msg['id'])
		#print(attach)
		vk.method('messages.send',{'chat_id': chat_id, 'attachment': attach})
		
messager = Messager()
