#!/usr/bin/python3
import requests
import vk_api
import os
import sys
import subprocess
import json
import optparse

class Messager:
	def __init__(self):
		if sys.argv[0][0:2] == './':
			prog = sys.argv[0][3:]
		else:
			prog = sys.argv[0]
		banner = """
Usage examples:

./{} --user="some_short_link_to_user" --text="Джони, они на деревьях!"

./{} --chat="DecSec conf" -t "Эй, кто съел мои чебупели?"

python3 {} -u "https://vk.com/id%some_id%" --file=some_music.wav

python3 {} --ch "Гражданская оборона" -f moya_oborona.mp3

python3 {} --help
		""".format(prog, prog, prog, prog, prog)

		user, chat, text, file_name, Options = self.get_options(banner)

		auth = self.auth(Options)
		
		try:
			if file_name != None:
				voice = "message.wav"
				subprocess.call('ffmpeg -i {} -map_channel 0.0.0 {}'.format(file_name, voice), shell=True)
				uploaded_voice = self.upload_file(voice, auth)
			elif text != None:
				voice = self.create_voice(text)
				uploaded_voice = self.upload_file(voice, auth)
			else:
				sys.exit(0)

			if user != None:
				user_id = self.get_user_id(user, auth)
				self.send_msg(uploaded_voice, user_id, auth)
			elif chat != None:
				chat = self.get_chat_id(chat, auth)
				self.send_chat_msg(uploaded_voice, chat, auth)
			else:
				sys.exit(0)
			print("Done")
		except Exception as e:
			print(e)
			sys.exit(0)
		
	def get_options(self, banner):
		parser = optparse.OptionParser(banner)
		parser.add_option('-u', '--user', dest='username',
				  help = 'link or id to user, who needs to send a message', 
				  metavar = 'USER')
		parser.add_option('-c', '--chat', dest='chatname',
				  help = 'Name of chate to send a message', 
				  metavar = 'CHAT')
		parser.add_option('-f', '--file', dest='filename',
				  help = 'Read voice/music form file', 
				  metavar = 'FILE')
		parser.add_option('-t', '--text', dest='text',
				  help = 'Voice this text by robot',
				  metavar = '"Some QUOTED text"')
		
		(options, args) = parser.parse_args()		

		if (options.username == None and options.chatname == None) or (options.text == None and options.filename == None):
			print(parser.usage)
			sys.exit(0)
		user_name = options.username
		chat_name = options.chatname
		file_name = options.filename
		text = options.text
		Options = json.loads(open("config.json").read(), encoding='utf-8')
		return user_name, chat_name, text, file_name, Options	

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