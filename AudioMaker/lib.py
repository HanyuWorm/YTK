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

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
#         self.tts = data
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
        
    #backup file full.mp3
    def backup(self, short_direct):
        direc = '{}/'.format(short_direct)

        if short_direct not in os.listdir():
            os.mkdir(short_direct)
        if 'full.wav' in os.listdir('{}'.format(direc)):
            #create folder backup if not exists
            if 'backup' not in os.listdir('{}'.format(direc)):
                os.mkdir('{}backup'.format(direc))

            now = str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")
            os.rename("{}full.wav".format(direc), "{}backup/{}.wav".format(direc, now))
            print('backup file full mp3 to {}backup/{}.wav'.format(direc, now))
    def remove_files(self, short_direct):
        direc = '{}/'.format(short_direct)
        for item in os.listdir('{}'.format(direc)):
            if item.endswith(".wav"):
                os.remove(os.path.join(direc, item))
        print('remove all file wav')
            
    def save_audio(self, filename):
        chapter = filename.split('-')[1]
        greeting = f'Xin kính chào toàn thể các quý thính giả của truyện au đi ô giải trí. hôm nay chúng ta sẽ đến với truyện mao sơn tróc quỷ nhân của tác giả. Thanh tử. chương {chapter}. . '
        ending = ' .Xin chào và hẹn gặp lại.'
        
        
        data = open(f'{filename}.txt','r', encoding='utf-8').read()
        
        data = greeting + data + ending
        
        self.backup(filename)
        self.remove_files(filename)
        
        wraptexts = wrap(data, 1000)
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME',
            'cache-control': 'no-cache'
        }
        count = 0
        for i in range(len(wraptexts)):
            text = wraptexts[i]
            body = "<speak version='1.0' xml:lang='en-US'><voice xml:lang='vi-VN' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (vi-VN, An)'><prosody rate='-30.00%'>" + text + "</prosody></voice></speak>"
            body = body.encode('utf-8')
            if count>100:
                print(f'ERROR ERROR ERROR ERROR {filename}')
                return		
            while True:
                try:
                    if count > 100:
                        f = open('error.err', 'a')
                        f.write(filename)
                        f.close()
                        break
                    response = requests.post(constructed_url, headers=headers, data=body)
                    if response.status_code == 200:
                        with open('{}/{:03}.mp3'.format(filename, i), 'wb') as audio:
                            audio.write(response.content)
            #                 audio.write(response.content)
                            print("download success {} / {} : {}/{:03}.mp3".format(i+1, len(wraptexts), filename, i))
                            count = 0
                        break
                    else:
                        print("Reloading...", end="")
                        count += 1
                except:
                    pass
                    
        self.merge_files(filename)
        self.remove_files(filename)
    def merge_files(self, short_direct):
        direc = '{}/'.format(short_direct)
        f = open("{}create_list.bat".format(direc), "w")
        f.write("(for %%i in (*.wav) do @echo file '%%i') > list.txt")
        f.close()
        s = "{}create_list.bat".format(direc)
        os.chdir(short_direct)
        print(os.listdir())
        print(s)

        # os.system("create_list2.bat".format(direc))
        subprocess.Popen("create_list.bat")
        os.chdir('..')

        #merge file for create 
        #output: full.mp3
        p = subprocess.run('ffmpeg -f concat -safe 0 -i {}list.txt -c copy {}full.wav'.format(direc, direc))
        
        print('COMPLETE')

subscription_key = "c2bc67df48a64a5f929684b39491c8b3"
app = TextToSpeech(subscription_key)
# app.get_token()
# args = sys.argv
# for i in range(int(args[1]), int(args[2]) + 1):
#     app.save_audio(f'chuong-{i}')

#backup file full.mp3
def backup(short_direct):
	try:
		direc = '{}/'.format(short_direct)
		print(not os.path.exists(short_direct))
		
		if not os.path.exists(short_direct):
			# print('???')
			os.mkdir(short_direct)
			# print(short_direct)
		
		# if 'full.mp3' in os.listdir('{}'.format(direc)):
		# 	print(f'{direc}full.mp3 EXIST')
		# 	return False
		# 	#create folder backup if not exists
		# 	if 'backup' not in os.listdir('{}'.format(direc)):
		# 		os.mkdir('{}backup'.format(direc))
			
		# 	now = str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")
		# 	os.rename("{}full.mp3".format(direc), "{}backup/{}.mp3".format(direc, now))
		# 	print('backup file full mp3 to {}backup/{}.mp3'.format(direc, now))
		# print('True')
		# return False
		return True	
	except:
		print('False')
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
	content = title.read() + ' . . , . . , . . .' + file.read()
	wraptexts = wrap(content, 480)

	if voice == 'an':
		
		wraptexts = wrap(content, 1000)
		base_url = 'https://westus.tts.speech.microsoft.com/'
		path = 'cognitiveservices/v1'
		constructed_url = base_url + path
		headers = {
			'Authorization': 'Bearer ' + app.access_token,
			'Content-Type': 'application/ssml+xml',
			'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3',
			'User-Agent': 'YOUR_RESOURCE_NAME',
			'cache-control': 'no-cache'
		}
		count = 0
		for i in range(len(wraptexts)):
			if os.path.exists("{}{:03}.mp3".format(direc, i)):
				continue
			text = wraptexts[i]
			body = "<speak version='1.0' xml:lang='en-US'><voice xml:lang='vi-VN' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (vi-VN, An)'><prosody rate='-30.00%'>" + text + "</prosody></voice></speak>"
			body = body.encode('utf-8')
			if count>100:
				print(f'ERROR ERROR ERROR ERROR {short_direct}')
				return		
			while True:
				try:
					if count > 100:
						f = open('error.err', 'a')
						f.write(short_direct)
						f.close()
						break
					response = requests.post(constructed_url, headers=headers, data=body)
					if response.status_code == 200:
						with open('{}/{:03}.mp3'.format(short_direct, i), 'wb') as audio:
							audio.write(response.content)
			#                 audio.write(response.content)
							print("download success {} / {} : {}/{:03}.mp3".format(i+1, len(wraptexts), short_direct, i))
							count = 0
						break
					else:
						print("Reloading...", end="")
						count += 1
				except:
					pass
	else:
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

	short_direct = f'../data/{short_direct}'
	is_first = True
	for i in range(start, end + 1, step):
		start_chapter = i
		if  i + step - 1 < end:
			end_chapter = i + step - 1
		else:
			end_chapter = end

		
		
		direc = f'{short_direct}/chuong-{start_chapter}-{end_chapter}'

		#chay xong thi an dong nay di nhe
		try:
			os.remove(direc + '/full.mp3')
		except:
			pass
		# os.mkdir(direc)

		
		if os.path.exists(f'{direc}/full.mp3'):
			print(f'chuong-{start_chapter}-{end_chapter} full.mp3 EXIST')
		else:
			f = open("{}/list.txt".format(direc), "w")
			shutil.copy(f'{short_direct}/start.mp3', f'{direc}/start.mp3')
			# shutil.copy(f'{short_direct}/tao_chao.mp3', f'{direc}/tao_chao.mp3')
			# shutil.copy(f'{short_direct}/dau_cach.mp3', f'{direc}/dau_cach.mp3')
			f.write('file start.mp3\n') # ấấn Ctrl / đđể ấấẩn hiêện dong nay 
			# f.write('file dau_cach.mp3\n')
			print(is_first)
			
			
			for i in range(start_chapter, end_chapter + 1):
				# print("??")
				shutil.copy(f'{short_direct}/chuong-{i}/full.mp3', f'{direc}/chuong-{i}.mp3')
				# if is_first:
				# 	is_first = False
				# else:
				# 	f.write('file tao_chao.mp3\n')
				# 	f.write('file dau_cach.mp3\n')
				f.write(f'file chuong-{i}.mp3\n')
				# f.write(f'file dau_cach.mp3\n')
				# print("????")

			
			f.write('file end.mp3\n')
			shutil.copy(f'{short_direct}/end.mp3', f'{direc}/end.mp3')
			f.close()
			print('create list.txt successful')
			p = subprocess.run('ffmpeg -f concat -safe 0 -i {}/list.txt -c copy {}/full.mp3'.format(direc, direc))
		
		if os.path.exists(f'{direc}/out.mp3'):
			print('out.mp3 EXIST')
		else:
			print('')
			# shutil.copy(f'{short_direct}/background.mp3', f'{direc}/background.mp3')
			# subprocess.run(f'ffmpeg -i {direc}/full.mp3 -filter_complex "amovie={direc}/background.mp3:loop=0,asetpts=N/SR/TB[beep];[0][beep]amix=duration=shortest" {direc}/out.mp3')
			# # os.remove(f'{direc}/full.wav')
			# p = subprocess.run(f'ffmpeg -i {direc}/full.mp3 -filter_complex "amovie={direc}/background.mp3:loop=0,asetpts=N/SR/TB[beep];[0][beep]amix=duration=shortest,volume=10,dynaudnorm" {direc}/out.mp3')


		remove_files(direc)


	
def run_all(short_direct, voice=voice, speed=speed, prosody=prosody):
	if backup(short_direct):
		print('ok')
		# remove_files(short_direct)
		result = download(short_direct, voice, speed, prosody)
		if result:
			merge_files(short_direct)
			remove_files(short_direct)
		else:
			print('SOME FILE IS NOT OK')
	

	