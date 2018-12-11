import sys
import requests
import os
import datetime
from textwrap import wrap
import time
import wget
import random
import subprocess

keys = open('keys.txt', 'r').read().split()
voice = "female"
speed= "0"
prosody= "0"

#backup file full.mp3
def backup(short_direct):
	try:
		direc = '{}/'.format(short_direct)
		
		if not os.path.exists(short_direct):
			os.mkdir(short_direct)
		
		if 'full.mp3' in os.listdir('{}'.format(direc)):
			print(f'{direc}full.mp3 EXIST')
			return False
			#create folder backup if not exists
			if 'backup' not in os.listdir('{}'.format(direc)):
				os.mkdir('{}backup'.format(direc))
			
			now = str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")
			os.rename("{}full.mp3".format(direc), "{}backup/{}.mp3".format(direc, now))
			print('backup file full mp3 to {}backup/{}.mp3'.format(direc, now))

		return True	
	except:
		pass
	
def remove_files(short_direct):
	direc = '{}/'.format(short_direct)
	for item in os.listdir('{}'.format(direc)):
		if item.endswith(".mp3") and item !='full.mp3':
			os.remove(os.path.join(direc, item))
	print('remove all file mp3')
	
def download(short_direct, voice=voice, speed=speed, prosody=prosody):
	direc = '{}/'.format(short_direct)
	title = open("{}.title".format(short_direct), "r", encoding="utf-8") 
	file = open("{}.txt".format(short_direct), "r", encoding="utf-8") 
	content = title.read() + ' . , . , . .' + file.read()
	wraptexts = wrap(content, 480)
	count = 0

	for i in range(len(wraptexts)):
		while True:
			try:
				if count >= 10:
					return False
				text = wraptexts[i]
				api_key = random.choice(keys)
				print('\n', api_key)
				url = "http://api.openfpt.vn/text2speech/v4?api_key={}&voice={}&speed={}&prosody={}".format(api_key, voice, speed, prosody)
				# print(voice)
				response = requests.post(url, data=text.encode('utf-8'), headers={'voice':voice, 'speed':speed, 'prosody':prosody})
				response = response.json()
				print('\n', response['async'])
				file = response['async']
				
				count2 = 0
				while True:
					if count2 >= 300:
						break
					try:
						print("downloading file {}/{} ".format(i+1, len(wraptexts)), "{}{:03}.mp3".format(direc, i))
						wget.download(file, "{}{:03}.mp3".format(direc, i))
						count2 = 0
						count = 0
						break
					except:
						count2 += 1
						time.sleep(0.1)
				if count2 == 0:
					break
			except :
				
				print('Waiting...', end='')
				count += 1
				continue
			
	print('\nCOMPLETE')
	return True
	
def merge_files(short_direct):
	direc = '{}/'.format(short_direct)
	f = open("{}list.txt".format(direc), "w")
	for item in os.listdir(short_direct):
		if '.mp3' in item:
			f.write(f'file {item}\n')
	f.close()

	p = subprocess.run('ffmpeg -f concat -safe 0 -i {}list.txt -c copy {}full.mp3'.format(direc, direc))
	
def run_all(short_direct, voice=voice, speed=speed, prosody=prosody):
	if backup(short_direct):
		remove_files(short_direct)
		result = download(short_direct, voice, speed, prosody)
		if result:
			merge_files(short_direct)
			remove_files(short_direct)
		else:
			print('SOME FILE IS NOT OK')

	