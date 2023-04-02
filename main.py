import sys
import os
import discord
import dotenv
import datetime
from resources import *


def get_max_key_len() -> int:
	# Get the length of the longest key
	return max(len(key) for key in xsampa_ipa_dict.keys())



def xsampa_to_ipa(word: str, max_key_len: int) -> str:
	xsampa_keys = (xsampa_ipa_dict.keys())

	output_string = ""

	# First pass, figuring out what is the longest sequence of characters starting from the current character
	# present in the xsampa_ipa_dict's keys, and adding the item for that onto the output string.
	next_unused_pos = 0
	for c, char in enumerate(word):
		to_replace = ""
		if c >= next_unused_pos:
			for d in range(c+1, len(word)):
				if d == c + max_key_len:
					break
				else:
					if word[c:d] in xsampa_keys:
						to_replace = word[c:d]
						next_unused_pos = d
			if to_replace != "":
				#print(fr"{datetime.datetime.now()} LOG     Replacing {to_replace} with {xsampa_ipa_dict[to_replace]}") # debugging
				output_string += xsampa_ipa_dict[to_replace]
			else:
				output_string += char

	# Second pass for formatting
	for key in formatting_dict:
		if key in output_string:
			output_string = output_string.replace(key, formatting_dict[key])

	return output_string.replace("\\","")


# Program starts execution here
max_key_len = get_max_key_len()

if __name__ == "__main__":
	word = sys.argv[1]


	if sys.argv[1] == "-dc":
		# Module called as a Discord bot
		dotenv.load_dotenv()
		token = os.getenv('DISCORD_TOKEN')
		intents = discord.Intents.default()
		intents.message_content = True
		discord_client = discord.Client(intents=intents)


		async def out_help(message: discord.Message) -> None:
			print(f"{datetime.datetime.now()} LOG     Displaying help in [{message.guild}  #{message.channel}]")
			await message.channel.send(help_text)
		

		commands = { # Can't be stored in resources.py
			"x/?": out_help,
			"x/help": out_help,
			"x/h": out_help,
		}


		@discord_client.event
		async def on_ready() -> None:
			# After startup
			await discord_client.change_presence(activity=discord.Game(name="x/help"))
			print(f"{datetime.datetime.now()} LOG     IPAnator-bot is online")
			for g, guild in enumerate(discord_client.guilds):
				print(f"{datetime.datetime.now()} LOG     IPAnator-bot is connected to {guild.name}/{guild.id}")
			print(f"{datetime.datetime.now()} LOG     Connected to {g+1} total servers")


		@discord_client.event
		async def on_message(message: discord.Message) -> None:
			# Responding to messages

			# Shouldn't respond to itself
			if(message.author.id == discord_client.user.id):
				return;

			content = message.content # repr() breaks in cases with overlapping backslashes

			command = commands.get(content)
			if command:
				await command(message)
			
			last_checked = -1
			output_list = []
			for x in range(0, len(content)):
				# Find bounds of X-Sampa strings
				trimmed_content = content[x:]
				start_point, end_point = -1, -1
				if x >= last_checked:
					if "x/" in trimmed_content.lower():
						start_point = trimmed_content.lower().index("x/")
						if '/' in trimmed_content[start_point+2:]:
							end_point = trimmed_content[start_point+2:].index("/")+start_point+2
					elif "x[" in trimmed_content.lower():
						start_point = trimmed_content.lower().index("x[")
						if ']' in trimmed_content[start_point+2:]:
							end_point = trimmed_content.index("]")

				# Convert X-Sampa text to IPA and add to list of total
				if start_point == 0 and end_point != -1:
					last_checked = end_point+1
					word = trimmed_content[start_point:end_point+1]
					output = xsampa_to_ipa(word[1:], max_key_len)
					output_list.append(output)

			# Output list of IPA > X-Sampa conversions with the format `/x/`, `/y/`, etc.
			if len(output_list) > 0:
				print(f"{datetime.datetime.now()} LOG     Handled message {content} -> {output} [id {message.id}] in [{message.guild}  #{message.channel}]")
				output_string = "`, `".join(output_list)
				await message.channel.send(f"`{output_string}`")


		discord_client.run(token)


	else:
		# Module called in single-shot command-line mode, doesn't work with some special characters like `,
		# or escape characters when not surrounded by parentheses.
		# Surround the X-Sampa string with parentheses for best, if not perfect, results.
		#print(f"Input: {word}")
		if word[0] == 'x' and (word[1] == '/' or word[1] == '['):
			print(xsampa_to_ipa(word[1:], max_key_len))
		else:
			print(xsampa_to_ipa(word, max_key_len))
