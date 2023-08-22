# IPAnator-bot
By jontiben, 2023, in Python

**[X-SAMPA](https://en.wikipedia.org/wiki/X-SAMPA)** is a system for transcribing the [International Phonetic Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) (IPA) using the [ASCII](https://en.wikipedia.org/wiki/ASCII) character set. It's probably easier to type than IPA if your keyboard doesn't have keys for all ~155 IPA symbols. This small project is primarily a discord bot for automatically converting X-SAMPA text in user messages to the IPA, but it can also run in single-shot mode in the command line.

Please contact me (@jontiben) on Discord for any suggestions, requests, and questions.

## Usage:

Requires the `discord` and `dotenv` libraries for Python:

`pip install discord`

`pip install python-dotenv`

### In the Command Line:

Note: Most command lines/terminals will fail on some special characters, including `.

To run in single-shot command-line mode, just run main.py with your target X-SAMPA string. Surround it with quotation marks to get better, though often not perfect (or functional) text processing.

**Example:**

```
> python main.py "[O:lr\E.di]"
[ɔːlɹɛ.di]
```

### Self-Hosting the Discord Bot:

First, download the code and unzip it. Next, follow one of the following tutorials to set up your application and bot framework:

- https://discordpy.readthedocs.io/en/stable/discord.html
- https://realpython.com/how-to-make-a-discord-bot-python/

Create a file inside the folder with your `main.py` called `.env`.

Put the following into `.env`:
```
# .env
DISCORD_TOKEN=XXXX
```

Copy your bot's token and replace `XXXX` with it.

Go back to the Discord Developer Portal you were just working in and, in the sidebar, click on OAuth2 and then URL Generator. Under "SCOPES" select "bot" and under "BOT PERMISSIONS" select "Read Messages/View Channels," "Send Messages," "Send Messages in Threads," and "Read Message History." It should look like this:

![image](https://user-images.githubusercontent.com/25780026/229337588-69a3a77e-4656-4cd1-bd0d-19cdfe895247.png)

Then copy the URL at the bottom and visit it in your browser. In the menu that comes up, select the server you'd like the bot to be active in and agree to the permissions requests.

Once that's set up, use your command line to run `main.py` with the argument `-dc`. It'll look like:

```
> python main.py -dc
2023-04-02 02:54:36 INFO     discord.client logging in using static token
2023-04-02 02:54:36 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 5fd4957d98cac60b4513e5554a3fb9d9).
2023-04-02 02:54:38.877288 LOG     IPAnator-bot is online
2023-04-02 02:54:38.877288 LOG     IPAnator-bot is connected to Test Server/0208061229038359115
2023-04-02 02:54:38.877288 LOG     Connected to 1 total servers
```

Use Ctrl+C at any time to exit. The bot will only be active while it's running on your computer. If you would like to set it up on a server feel free, just don't ask me for help.

To interact with the bot in the server, type a message that includes a section formatted like x/******/ or x[******]. The bot will read those sections as X-SAMPA and send a message with the converted IPA.

**Example:**

![image](https://user-images.githubusercontent.com/25780026/229337856-b492f39e-b79b-48ff-87de-0435a6d2fcc0.png)

At any time you can use x/h, x/?, or x/help to get help.

### Using my Discord Bot Hosting:

Contact me on Discord where I'm jontiben#7855 and maybe we can work something out.

### Importing from Another Python Module:

Make sure to keep `resources.py` and `main.py` together. `main.py` can be renamed, and the `xsampa_to_ipa` function called normally. It takes an X-SAMPA string and a max X-SAMPA key length integer (which should be 4, it'll generate in the module when it's imported and can be accessed with `main.max_key_len`) as inputs. It outputs an IPA string.

```python
def xsampa_to_ipa(word: str, max_key_len: int) -> str:
  <...>
  return output_string.replace("\\","")
```

**Example:**
With `main.py` and `resources.py` in the same directory as the following code, and `main.py` renamed to `xsampa_ipa.py`:

```python
import xsampa_ipa

test_word = "/tEst/"

print(xsampa-ipa.xsampa_to_ipa(test_word, xsampa-ipa.max_key_len))
```

Which, when run, outputs
`/tɛst/`.

## License:

This project uses the MIT license.
