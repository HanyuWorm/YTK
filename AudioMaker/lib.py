import sys
import requests
import os
import datetime
from textwrap import wrap
import time
import wget
import random
import subprocess
import shutil

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
		if item.endswith(".mp3") and item !='full.mp3' and item != "out.mp3":
			os.remove(os.path.join(direc, item))
	print('remove all file mp3')

def start_end(direct, voice=voice, speed=speed, prosody=prosody):
	start = open("{}/start.txt".format(direct), "r", encoding="utf-8").read()
	end = open("{}/end.txt".format(direct), "r", encoding="utf-8").read()

	count = 0
	print(start)
	print(end)
	while True:
		try:
			if count >= 50:
				return False
			time.sleep(1)
			text = start
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
					print("downloading start.mp3")
					wget.download(file, "{}/start.mp3".format(direct))
					count2 = 0
					count = 0
					print("download successfull start.mp3")
					break
				except:
					count2 += 1
					time.sleep(0.1)
			break
		except :
			print('Waiting...', end='')
			count += 1

	count = 0
	while True:
		try:
			if count >= 50:
				return False
			time.sleep(1)
			text = end
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
					print("downloading end.mp3")
					wget.download(file, "{}/end.mp3".format(direct))
					count2 = 0
					count = 0
					print("download successfull end.mp3")
					break
				except:
					count2 += 1
					time.sleep(0.1)
			break
		except :
			print('Waiting...', end='')
			count += 1
			continue

def download(short_direct, voice=voice, speed=speed, prosody=prosody):
	direc = '{}/'.format(short_direct)
	title = open("{}.title".format(short_direct), "r", encoding="utf-8") 
	file = open("{}.txt".format(short_direct), "r", encoding="utf-8") 
	content = title.read() + ' . , . , . .' + file.read()
	wraptexts = wrap(content, 480)
	count = 0

	for i in range(len(wraptexts)):
		if os.path.exists("{}{:03}.mp3".format(direc, i)):
			continue
		while True:
			try:
				if count >= 50:
					return False
				time.sleep(1)
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
						time.sleep(1)
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


def concat(short_direct, start, end, step):
	
	for i in range(start, end + 1, step):
		start_chapter = i
		if  i + step - 1 < end:
			end_chapter = i + step - 1
		else:
			end_chapter = end

		
		direc = f'{short_direct}/chuong-{start_chapter}-{end_chapter}'

		if os.path.exists(f'{direc}/full.mp3'):
			print(f'chuong-{start_chapter}-{end_chapter} full.mp3 EXIST')
		else:
			f = open("{}/list.txt".format(direc), "w")
			shutil.copy(f'{short_direct}/start.mp3', f'{direc}/start.mp3')
			f.write('file start.mp3\n')
			for i in range(start_chapter, end_chapter + 1):
				shutil.copy(f'{short_direct}/chuong-{i}/full.mp3', f'{direc}/chuong-{i}.mp3')
				f.write(f'file chuong-{i}.mp3\n')

			
			f.write('file end.mp3\n')
			shutil.copy(f'{short_direct}/end.mp3', f'{direc}/end.mp3')
			f.close()
			print('create list.txt successful')
			p = subprocess.run('ffmpeg -f concat -safe 0 -i {}/list.txt -c copy {}/full.mp3'.format(direc, direc))
		
		# if os.path.exists(f'{direc}/out.mp3'):
		# 	print('out.mp3 EXIST')
		# else:
		# 	shutil.copy(f'{short_direct}/background.mp3', f'{direc}/background.mp3')
		# 	p = subprocess.run(f'ffmpeg -i {direc}/full.mp3 -filter_complex "amovie={direc}/background.mp3:loop=0,asetpts=N/SR/TB[beep];[0][beep]amix=duration=shortest,volume=10,dynaudnorm" {direc}/out.mp3')


		remove_files(direc)


	
def run_all(short_direct, voice=voice, speed=speed, prosody=prosody):
	if backup(short_direct):
		# remove_files(short_direct)
		result = download(short_direct, voice, speed, prosody)
		if result:
			merge_files(short_direct)
			remove_files(short_direct)
		else:
			print('SOME FILE IS NOT OK')
	

	