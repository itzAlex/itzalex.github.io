import requests 
import json 
import sys
import argparse
import time
import os

# 7TV API
API_7TV_URL = 'https://api.7tv.app/v2/gql'

# Colors
windows_check = sys.platform.startswith('win')
if not windows_check:
	G = '\033[92m'  	# green
	Y = '\033[93m'  	# yellow
	B = '\033[94m'  	# blue
	R = '\033[91m'  	# red
	W = '\033[0m'   	# white
	P = '\033[35m'		# purple
	CYAN = '\033[36m'	# cyan
	BOLD = '\033[1m'	# bold
else:
	G = Y = B = R = P = W = CYAN = BOLD = ''

def globalEmoteAdd(data, filename='./emotes'):
	with open(filename, 'r+') as file:
		file_data = json.load(file)

		for i in range(0, len(file_data['data']['global_emotes'])):
			if file_data['data']['global_emotes'][i]['id'] == data['id']:
				print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - This emote is already global" + W)
				sys.exit()

		file_data['data']['global_emotes'].append(data)
		file.seek(0)
		json.dump(file_data, file, indent = 4)

def channelEmoteAdd(data, filename='./emotes'):
	with open(filename, 'r+') as file:
		file_data = json.load(file)

		if channelID not in file_data['data']['channel_emotes']:
			print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " New channel detected. Initializing..." + Y)
			file_data['data']['channel_emotes'][channelID] = {}
			file_data['data']['channel_emotes'][channelID]['emotes'] = []

		for i in range(0, len(file_data['data']['channel_emotes'][channelID]['emotes'])):
			if file_data['data']['channel_emotes'][channelID]['emotes'][i]['id'] == data['id']:
				print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - This emote is already in that channel" + W)
				sys.exit()

		file_data['data']['channel_emotes'][channelID]['emotes'].append(data)
		file.seek(0)
		json.dump(file_data, file, indent = 4)

def globalEmoteRemove(filename='./emotes'):
	with open(filename, 'r+') as file:
		file_data = json.load(file)

		for i in range(0, len(file_data['data']['global_emotes'])):
			if file_data['data']['global_emotes'][i]['id'] == emoteID:
				file_data['data']['global_emotes'].pop(i)
				
				open(filename, 'w').write(
					json.dumps(file_data, indent = 4)		
				)

				print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " The given global emote has been removed" + Y)
				sys.exit()

	print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - The provided emote was not found in the global emotes" + W)			

def channelEmoteRemove(filename='./emotes'):
	with open(filename, 'r+') as file:
		file_data = json.load(file)

		if channelID not in file_data['data']['channel_emotes']:
			print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - The given channel ID does not have any emote" + W)
			sys.exit()

		for i in range(0, len(file_data['data']['channel_emotes'][channelID]['emotes'])):
			if file_data['data']['channel_emotes'][channelID]['emotes'][i]['id'] == emoteID:
				file_data['data']['channel_emotes'][channelID]['emotes'].pop(i)

				open(filename, 'w').write(
					json.dumps(file_data, indent = 4)		
				)

				print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " The given channel emote has been removed" + Y)
				sys.exit()

	print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - The provided emote was not found in the channel emotes" + W)

def addEmote():
	payload = {"query":"{emote(id: \"" + emoteID + "\") {...FullEmote}}fragment FullEmote on Emote {name, owner {display_name}}"}
	request = requests.post(API_7TV_URL, payload)
	response = request.json()

	if response['data']['emote'] == None:
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - The provided emote ID does not exist" + W)
		sys.exit()

	if not emoteName:
		emote_name = response['data']['emote']['name']
	else:
		emote_name = emoteName

	author = response['data']['emote']['owner']['display_name']

	if not os.path.isdir('./emote/' + emoteID): 
		os.makedirs('./emote/' + emoteID)
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " Downloading emote... (" + response['data']['emote']['name'] + ")" + Y)
		
		request3X = requests.get('https://cdn.7tv.app/emote/' + emoteID + '/3x')
		request2X = requests.get('https://cdn.7tv.app/emote/' + emoteID + '/2x')
		request1X = requests.get('https://cdn.7tv.app/emote/' + emoteID + '/1x')

		open('./emote/' + emoteID + '/3x', 'wb').write(request3X.content)
		open('./emote/' + emoteID + '/2x', 'wb').write(request2X.content)
		open('./emote/' + emoteID + '/1x', 'wb').write(request1X.content)

		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " Emote downloaded successfully" + Y)

		new_emote_data = {
						  "id":emoteID,
						  "name": emote_name,
						  "author": author
						 }

		if globalEmote:
			globalEmoteAdd(new_emote_data)

		if channelID:	
			channelEmoteAdd(new_emote_data)

		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " Emote added successfully" + Y)
	
	else:
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " Skipping emote download since it already exists... (" + response['data']['emote']['name'] + ")" + Y)

		new_emote_data = {
						  "id":emoteID,
						  "name": emote_name,
						  "author": author
						 }

		if globalEmote:
			globalEmoteAdd(new_emote_data)

		if channelID:	
			channelEmoteAdd(new_emote_data)

		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + "+" + W + "]" + " Emote added successfully" + Y)

def removeEmote():
	if globalEmote:
		globalEmoteRemove()
	if channelID:
		channelEmoteRemove()

def banner():
	print(f'{BOLD}{Y}🛠 {W} {BOLD}Chatterino{W} - {BOLD}{G}Homies{W} {BOLD}{G}Emotes{Y} 🛠{W}\n')

def parser_error(errmsg):
	banner()
	print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + G + BOLD + "+" + W + "]" + " Usage: " + Y + "python " + sys.argv[0] + W + " (use -h for help)")
	print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error: " + Y + errmsg)
	sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " -a")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-a', '--add', help="Add emote", required=False, action="store_true")
    parser.add_argument('-r', '--remove', help="Remove emote", required=False, action="store_true")
    parser.add_argument('-e', '--emote', help="7TV emote ID", required=True)
    parser.add_argument('-g', '--globalemote', help="Set emote to global", required=False, action="store_true")
    parser.add_argument('-c', '--channelemote', help="Set emote to specific channel", default=False)
    parser.add_argument('-n', '--name', help="Set emote name", default=False)
    return parser.parse_args()

def interactive():
	global emoteID, globalEmote, channelID, emoteName

	args = parse_args()
	banner()
	if not (args.globalemote or args.channelemote):
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - One of the following arguments are required: " + Y + "-g/--global" + W + "," + Y + " -c/--channel" + W)
		sys.exit()

	if not (args.add or args.remove):
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - One of the following arguments are required: " + Y + "-a/--add" + W + "," + Y + " -r/--remove" + W)
		sys.exit()	

	if (args.globalemote and args.channelemote):
		print(W + "[" + B + time.strftime("%H:%M:%S") + W + "]" + W + "[" + R + BOLD + "!" + W + "]" + " Error - You can only use one of the follow arguments: " + Y + "-g/--global" + W + "," + Y + " -c/--channel" + W)
		sys.exit()	

	emoteID = args.emote
	globalEmote = True if args.globalemote else False
	channelID = args.channelemote
	emoteName = args.name

	if args.add: addEmote()
	if args.remove: removeEmote()

if __name__ == "__main__":
	interactive()