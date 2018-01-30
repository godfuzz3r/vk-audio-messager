#!/usr/bin/env python3
import sys
import os
import json
import argparse
from vk_api import VkApi
import subprocess
import requests

def connect(login, password):
	try:
		conn = VkApi(login=login, password=password)
		conn.auth()
		return conn
	except Exception as e:
		print(e)
		sys.exit(0)

def create_voice(message, speed):
	file_name = "message.wav"
	cmd_1 = 'espeak -vru -s{0} -z "{1}" -w prepare.wav'.format(speed, message)
	cmd_2 = 'ffmpeg -i prepare.wav -map_channel 0.0.0 {}'.format(file_name)
	subprocess.call(cmd_1, shell=True)
	subprocess.call(cmd_2, shell=True)
	os.system("rm prepare.wav")
	return file_name

def upload_file(path, vk):
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

def get_user_id(link, vk):
	id = link
	if 'vk.com/' in link:
		id = link.split('/')[-1]
	if not id.replace('id', '').isdigit():
		id = vk.method('users.get', {'user_ids':id})[0]['id']
	else:
		id = id.replace('id', '')
	#print('user_id: ', id)
	return int(id)

def get_chat_id(link, vk):
	chats = vk.method("messages.searchDialogs", {"q": link})
	print(chats)
	for chat in chats:
		if chat['type'] == 'chat':
			pass
			return chat['id']
		

def send_msg(msg, user_id, vk):
	attach = 'doc%s_%s' % (msg['owner_id'], msg['id'])
	#print(attach)
	vk.method('messages.send',{'user_id': user_id, 'attachment': attach})

def send_chat_msg(msg, chat_id, vk):
	attach = 'doc%s_%s' % (msg['owner_id'], msg['id'])
	#print(attach)
	vk.method('messages.send',{'chat_id': chat_id, 'attachment': attach})

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-c', '--chat', dest='chat',
				  help = 'Name of chate to send a message', 
				  metavar = 'CHAT')
	parser.add_argument('-u', '--user', dest='user',
				  help = 'link or id to user, who needs to send a message', 
				  metavar = 'USER')
	parser.add_argument('-f', '--file', dest='file',
				  help = 'Read voice/music form file', 
				  metavar = 'FILE')
	parser.add_argument('-t', '--text', dest='text',
				  help = 'Voice this text by robot',
				  metavar = '"Some QUOTED text"')
	parser.add_argument('-s', '--speed', dest='speed',
				  help = 'Voice speed. Default: 3',
				  default='3')

	args = parser.parse_args()

	if args.file != None:
		voice = "message.wav"
		subprocess.call('ffmpeg -i {} -map_channel 0.0.0 {}'.format(file_name, voice), shell=True)
	elif args.text != None:
		voice = create_voice(args.text, args.speed)

	config = json.loads(open("config.json").read(), encoding='utf-8')
	login = config["login"]
	password = config["password"]

	connection = connect(login, password)
	uploaded_voice = upload_file(voice, connection)

	if args.user != None:
		user_id = get_user_id(args.user, connection)
		send_msg(uploaded_voice, user_id, connection)
	elif args.chat != None:
		chat = get_chat_id(args.chat, connection)
		send_chat_msg(uploaded_voice, chat, connection)

	print("Done")


if __name__ == "__main__":
	main()
