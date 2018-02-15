import discord
import asyncio
import pickle
import os
import random
from urllib.request import urlopen
import bs4
import time
import re

class RepSelf(Exception):
    pass
class WrongUsage(Exception):
	pass

client = discord.Client()
	
errorMessD = {'error': '```Error```', 'nofile': '```Files not found```', 'alreadyReg': '```Already Registered.```',
				'notReg': '```Person is not registered```', 'repSelf':  '```You can\'t rep yourself```',
				'usage+rep': '```Usage: +rep @PersonYouWantToRep```', 'usage-rep': '```Usage: -rep @PersonYouWantToRep```',
				'usagePlay':'```Usage: !play <youtube url>```',
				'usagePoll': '```Usage: !poll Question:<your question> 1:<first option> 2:<second option> 3:<third option> ...\n    (Seperate each question with a space. Max 9 Options.)```'}

@client.event
async def on_ready():
	print('------')
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	messageLower = message.content.lower()
		
	if messageLower.startswith('!rephelp'):
		retMessage = '```\
!rephelp - Reputation related commands\n\
!help - Other commands\n\
--------------------------------\n\n\
!repregister - Register for reputation list\n\
!replist - Show the reputation standings\n\
+rep @Person - Add reputation of a member\n\
-rep @Person - Deduct reputation of a member\
```'
		await client.send_message(message.channel, retMessage)
		
	if messageLower.startswith('!help'):
		retMessage = '```\
!rephelp - Reputation related commands\n\
!help - Other commands\n\
--------------------------------\n\n\
!hi - Say hello to Reputation Bot!\n\
!flip - Flip a coin\n\
!roll <number> - Roll 1 to <number> (default is 100)\n\
!advice - Seek advice from Reputation Bot\n\
\
!wordoftheday - The Word of the Day\n\
!poll Question:<your question> 1:<first option> 2:<seco ... - Start a poll! Max 9 Options.\n\
!play <youtube url> - Play a youtube video\
```'
		await client.send_message(message.channel, retMessage)

	if message.author.id == '393835788401639437' and (message.content in errorMessD.values() or message.content.startswith('```Wait ')):
		await asyncio.sleep(10)
		await client.delete_message(message)

	if messageLower.startswith('!break'):
		while True:
			await client.send_message(message.channel, 'fuck jem!')
			
	if messageLower.startswith('!hi'):
		await client.send_message(message.channel, 'Hello!')

	if messageLower.startswith('!flip'):
		if random.random() >= 0.5:
			await client.send_message(message.channel, 'Heads')
		else:
			await client.send_message(message.channel, 'Tails')
    
	if messageLower.startswith('!roll'):
		splitMess = message.content.split()
		try:
			if len(splitMess) >= 2:
				if splitMess[1].isdigit() == True:
					await client.send_message(message.channel, random.randrange(1, int(splitMess[1])+1))
				else:
					raise
			else:
				raise
		except:
			await client.send_message(message.channel, random.randrange(1, 101))

	if messageLower.startswith('!wordoftheday'):
		clientBS4 = urlopen('https://www.merriam-webster.com/word-of-the-day')
		page_html = clientBS4.read()
		soup = bs4.BeautifulSoup(page_html, 'html.parser')
		clientBS4.close()
		wordday = {}
		wordday['name'] = soup.findAll('div', {'class': 'word-and-pronunciation'})[0].h1.contents[0]
		wordday['type'] = soup.findAll('div', {'class': 'word-attributes'})[0].findAll('span')[0].contents[0]
		wordday['pro'] = soup.findAll('div', {'class': 'word-attributes'})[0].findAll('span')[1].contents[0]
		tag = soup.findAll("div", {'class': 'wod-definition-container'})[0].find('p')
		tagmeanings = []
		meanings = []
		while True:
			if isinstance(tag, bs4.element.Tag):
				if tag.name == 'span':
					break
				else:
					tagmeanings.append(tag)
					tag = tag.nextSibling
			else:
				tag = tag.nextSibling
		for i in tagmeanings:
			meanings.append(i.get_text())
		wordday['meaning'] = '\n'.join(meanings)
		if len(meanings) == 1:
                    wordday['meaning'] = '1' + wordday['meaning']
		await client.send_message(message.channel, '{} ({}) - {}\n ```{}```'.format(wordday['name'], wordday['pro'], wordday['type'], wordday['meaning']))

	if messageLower.startswith('!advice'):
		choices = ['Yes', 'Yeah', 'You may rely on it', 'Signs point to yes', 'It is certain', 'Without a doubt', 'Yes, definitely', 'Outlook is good', 'Most likely',
					'No', 'No!', 'Nope', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful',
					'Maybe', 'Better not tell you now', 'I\'m not sure', 'Ask again later']
		await client.send_message(message.channel, random.choice(choices))

	if messageLower.startswith('!repregister'):
		try:
			with open('repList.pk1', 'rb') as file:
				repList = pickle.load(file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)
		if message.author.id in repList:
			await client.send_message(message.channel, errorMessD['alreadyReg'])
		else:
			repList[message.author.id] = {'name': message.author.name, 'Did': message.author.discriminator, 'display': message.author.display_name, 'rep': 0}
			try:
				with open('repList.pk1', 'wb') as file:
					pickle.dump(repList, file)
			except FileNotFoundError as e:
				if e.errno == 2:
					await client.send_message(message.channel, errorMessD['noFile'])
					print(e)
				else:
					raise
			except Exception as e:
				await client.send_message(message.channel, errorMessD['error'])
				print(e)
			else:
				await client.send_message(message.channel, 'Successfully Registered!')
			

	if messageLower.startswith('!replist'):
		try:
			with open('repList.pk1', 'rb') as file:
				repList = pickle.load(file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)
		strM = 'Reputation\n--------------------\n'
		for i in repList:
			strM = strM + '{}({}#{}): {}\n'.format(repList[i]['display'], repList[i]['name'], repList[i]['Did'], repList[i]['rep'])
		strM = strM[:-1]
		await client.send_message(message.channel, strM)

	if messageLower.startswith('+rep') or messageLower.startswith('-rep'):
		kind = ''
		if messageLower.startswith('+rep'):
			kind = '+'
		else:
			kind = '-'
		try:
			with open('repVotes.pk1', 'rb') as file:
				votes = pickle.load(file)
			with open('repList.pk1', 'rb') as file:
				repList = pickle.load(file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)

		mess = message.content.split()
		reSearch = re.compile(r'<@!?[\d]+>')
		try:
			repID = re.findall(reSearch, mess[1])[0]
			if '!' in repID:
				repID = repID[3:-1]
			else:
				repID = repID[2:-1]
		except IndexError:
			if kind == '+':
				await client.send_message(message.channel, errorMessD['usage+rep'])
			else:
				await client.send_message(message.channel, errorMessD['usage-rep'])
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)
		else:
			try:
				timeThreshold = 21600
				cooldown = '6 hour'
				finish = time.time()
				initial = votes[message.author.id]
				if (finish - initial) > timeThreshold:
					try:
						if repID != message.author.id:
							if kind == '+':
								repList[repID]['rep'] += 1
								await client.send_message(message.channel, '{}: {} -> {}'.format(repList[repID]['display'], repList[repID]['rep']-1, repList[repID]['rep']))
							else:
								repList[repID]['rep'] -= 1
								await client.send_message(message.channel, '{}: {} -> {}'.format(repList[repID]['display'], repList[repID]['rep']+1, repList[repID]['rep']))
						else:
							raise RepSelf
					except KeyError:
						await client.send_message(message.channel, errorMessD['notReg'])
					except RepSelf:
						await client.send_message(message.channel, errorMessD['repSelf'])
					except Exception as e:
						await client.send_message(message.channel, errorMessD['error'])
						print(e)
					else:
						votes[message.author.id] = time.time()
				else:
					waitTime = round(timeThreshold - finish + initial)
					minutes = waitTime//60
					seconds = waitTime - minutes*60
					hours = minutes//60
					minutes = minutes - hours*60
						
					if waitTime >= 60:
						if waitTime >= 3600:
							await client.send_message(message.channel, '```Wait {} hour/s and {} minutes before repping again ({} cooldown)```'.format(hours, minutes, cooldown))
						else:
							await client.send_message(message.channel, '```Wait {} minute/s and {} seconds before repping again ({} cooldown)```'.format(minutes, seconds, cooldown))
					else:
						await client.send_message(message.channel, '```Wait {} seconds before repping again ({} cooldown)```'.format(seconds, cooldown))
			except KeyError:
				try:
					if repID != message.author.id:
						if kind == '+':
							repList[repID]['rep'] += 1
							await client.send_message(message.channel, '{}: {} -> {}'.format(repList[repID]['display'], repList[repID]['rep']-1, repList[repID]['rep']))
						else:
							repList[repID]['rep'] -= 1
							await client.send_message(message.channel, '{}: {} -> {}'.format(repList[repID]['display'], repList[repID]['rep']+1, repList[repID]['rep']))
					else:
						raise RepSelf
				except KeyError:
					await client.send_message(message.channel, errorMessD['notReg'])
				except RepSelf:
					await client.send_message(message.channel, errorMessD['repSelf'])
				except Exception as e:
					await client.send_message(message.channel, errorMessD['error'])
					print(e)
				else:
					votes[message.author.id] = time.time()
			except Exception as e:
					await client.send_message(message.channel, errorMessD['error'])
					print(e)
				
		try:
			with open('repVotes.pk1', 'wb') as file:
				pickle.dump(votes, file)
			with open('repList.pk1', 'wb') as file:
				pickle.dump(repList, file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)

	if messageLower.startswith('!poll'):
		try:
			messL = message.content.split()
			if not messL[1].lower().startswith('question:') or not messL[0] == '!poll':
				raise WrongUsage
			mess = message.content
			if mess.find(f' {1}:') == -1:
				raise WrongUsage
			else:
				question = mess[16:mess.find(f' {1}:')]
			options = []
			print(f'message: {mess} \n')
			for i in range(1, 10):
				optionIndex = mess.find(f' {i}:')
				optionIndex2 = mess.find(f' {i+1}:')
				if optionIndex == -1:
					break
				if optionIndex2 == -1:
					options.append(mess[optionIndex + 1:])
					break
				options.append(mess[optionIndex + 1: optionIndex2])
				mess = mess[optionIndex + 1:]
			
			print('question, option',  question, options)
			retMessage = f'```POLL: {question}```'
			for i in options:
				retMessage += '\n' + i
			await client.send_message(message.channel, retMessage)
		except WrongUsage:
			await client.send_message(message.channel, errorMessD['usagePoll'])
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)
		else:
			try:
				with open('polls.pk1', 'rb') as file:
					polls = pickle.load(file)
			except FileNotFoundError as e:
				if e.errno == 2:
					await client.send_message(message.channel, errorMessD['noFile'])
					print(e)
				else:
					raise
			except Exception as e:
				await client.send_message(message.channel, errorMessD['error'])
				print(e)

			append = {'original': message, 'question': question, 'options': options}
			polls.append(append)

			try:
				with open('polls.pk1', 'wb') as file:
					pickle.dump(polls, file)
			except FileNotFoundError as e:
				if e.errno == 2:
					await client.send_message(message.channel, errorMessD['noFile'])
					print(e)
				else:
					raise
			except Exception as e:
				await client.send_message(message.channel, errorMessD['error'])
				print(e)

	if message.content.startswith('```POLL: ') and message.author.id == '393835788401639437':
		await asyncio.sleep(1)
		try:
			with open('polls.pk1', 'rb') as file:
				polls = pickle.load(file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)

		polls[-1]['object'] = message

		try:
			with open('polls.pk1', 'wb') as file:
				pickle.dump(polls, file)
		except FileNotFoundError as e:
			if e.errno == 2:
				await client.send_message(message.channel, errorMessD['noFile'])
				print(e)
			else:
				raise
		except Exception as e:
			await client.send_message(message.channel, errorMessD['error'])
			print(e)

		emojiL = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
		for i in range(len(polls[-1]['options'])):
			await client.add_reaction(message, emojiL[i + 1])

	if messageLower.startswith('!play'):
		mess = message.content.split()
		try:
			if len(mess) != 2:
				raise WrongUsage
			if message.author.voice.voice_channel == None:
				pass
			else:
				try:
					voice = await client.join_voice_channel(message.author.voice.voice_channel)
				except ClientException:
					pass
				player = await voice.create_ytdl_player(mess[1])
				player.start()
		except WrongUsage:
			await client.send_message(message.channel, errorMessD['usagePlay'])
		
	print('({}) {} || {}'.format(message.timestamp, message.author.name, message.content))

client.run('MzkzODM1Nzg4NDAxNjM5NDM3.DUjfBw.3sF9G_zZpJaYPqDpKhUIAo0Ztow')

#pynacl
#youtube_dl
#ffmpeg
