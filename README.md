# BOT-Discord-Ranking-Profile
This project is a Discord bot that generates and displays player profiles and rankings based on data retrieved from an external API. The bot is built using Python, with the discord.py library to handle interactions with Discord, and the Pillow library to generate images.

Features
Player Profile Command (!perfil): Fetches and displays a player's profile, including their level, discovered and caught Pokémon, quests, and clan affiliation. The profile is presented as a generated image.
Top Players Ranking Command (!ranking): Fetches and displays the top 10 players based on their levels. The ranking is presented as a generated image.

Prerequisites:
- Python 3.7 or higher
- Discord Bot Token
- An API that provides player data and ranking (Replace the API URLs in the code with your actual endpoints)

Clone this repo, open the paste in CMD:

pip install -r requirements.txt
python bot.py

In discord:
!perfil AshKetchum
!ranking

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
discord.py: For providing an easy-to-use library to interact with the Discord API.
Pillow: For the image processing capabilities used in this project.
Troubleshooting
Bot not responding to commands: Ensure that your bot has the necessary permissions in the server and that it is running.
Image not generating correctly: Check the paths to the profile images and ensure that the profiles/ directory exists and contains the correct images.
