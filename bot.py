import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests

# Token do bot, coloque aqui o seu token real (não compartilhe publicamente)
TOKEN = 'SEU_TOKEN_AQUI'

# Definir intents para o bot
intents = discord.Intents.default()
intents.message_content = True  # Necessário para receber o conteúdo das mensagens

# Prefixo para os comandos do bot (!comando)
bot = commands.Bot(command_prefix='!', intents=intents)

# Função que obtém os dados do jogador usando o nome dele
def get_player_data(player_name):
    # Fazendo a requisição à API de perfil
    response = requests.get(f'https://api.exemplo.com/profile/{player_name}')
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        return response.json()  # Retorna os dados do jogador em formato JSON
    else:
        return None  # Retorna None se a requisição falhar

# Função que obtém o nível do jogador usando o ID dele
def get_player_level(player_id):
    # Fazendo a requisição à API para obter o nível do jogador
    response = requests.get(f'https://api.exemplo.com/player/{player_id}')
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]["level"]  # Acessando diretamente o nível
        elif isinstance(data, dict):
            return data.get("level")  # Se for um dicionário, pega o nível
    return None  # Retorna None se algo der errado

# Função que obtém os 10 melhores jogadores
def get_top_players():
    # Fazendo a requisição à API para obter a lista de jogadores
    response = requests.get('https://api.exemplo.com/players')
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        players = response.json()
        # Retornando a lista de jogadores diretamente
        return players
    else:
        return []  # Retorna uma lista vazia se a requisição falhar

# Função que gera uma imagem do perfil do jogador
def generate_profile_image(player_data, player_level):
    # Tamanho da imagem
    width, height = 800, 450
    img = Image.new('RGBA', (width, height), color=(0, 45, 89))  # Fundo azul escuro
    d = ImageDraw.Draw(img)
    
    # Carregar fonte padrão do sistema
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 20)

    # Criar um degradê azul claro no fundo das caixas de texto
    for i in range(30, 400):
        color_value = int(45 + (110 - 45) * ((i - 30) / (400 - 30)))  # Gradiente linear
        d.line([(250, i), (750, i)], fill=(color_value, color_value + 20, color_value + 96), width=1)
    
    # Adicionar a imagem do perfil no lado esquerdo
    profile_image_path = f'profiles/{player_data["picture"]}.png'
    try:
        profile_img = Image.open(profile_image_path).convert("RGBA")
    except FileNotFoundError:
        profile_img = Image.open('profiles/default.png').convert("RGBA")
    
    profile_img = profile_img.resize((150, 150))
    img.paste(profile_img, (50, 40), profile_img)
    
    # Centralizar o nome do jogador abaixo da imagem de perfil
    text_bbox = d.textbbox((0, 0), player_data["player_name"], font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = 50 + (150 - text_width) // 2  # Centralizando o texto abaixo da imagem de 150px
    d.text((text_x, 200), f'{player_data["player_name"]}', fill=(255, 255, 255), font=font)

    # Adicionar nível do jogador no lado direito
    d.text((260, 40), f'Level: {player_level}', fill=(255, 255, 255), font=font)

    # Adicionar informações adicionais
    d.text((260, 90), f'Discovered Pokemons: {len(player_data["discovered_pokemons"])}', fill=(255, 255, 255), font=font_small)
    d.text((260, 130), f'Caught Pokemons: {len(player_data["caught_pokemons"])}', fill=(255, 255, 255), font=font_small)
    
    # Exibir quests
    d.text((260, 170), 'Quests:', fill=(255, 255, 255), font=font)
    quests = player_data["quests"]
    d.text((260, 210), quests, fill=(255, 255, 255), font=font_small)
    
    # Adicionar Clan
    d.text((260, 300), f'Clan: {player_data["clan"]}', fill=(255, 255, 255), font=font_small)

    # Converter a imagem para RGB antes de salvar
    img = img.convert("RGB")
    img.save('profile_image_generated.png')

# Função que gera uma imagem com o ranking dos jogadores
def generate_rank_image(top_players):
    # Tamanho da imagem
    width, height = 800, 600
    img = Image.new('RGBA', (width, height), color=(0, 45, 89))
    d = ImageDraw.Draw(img)
    
    # Carregar fonte padrão do sistema
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
    
    # Adicionar título
    d.text((300, 20), "Top 10 Players", fill=(255, 255, 255), font=font)
    
    # Adicionar cada jogador no ranking
    for i, player in enumerate(top_players):
        y_position = 70 + i * 50
        
        # Adicionar posição, nome e nível
        d.text((50, y_position), f'{i+1}. {player["name"]} (Level: {player["level"]})', fill=(255, 255, 255), font=font)
        
        # Adicionar imagem de perfil
        profile_image_path = f'profiles/{player["picture"]}.png'
        try:
            profile_img = Image.open(profile_image_path).convert("RGBA")
        except FileNotFoundError:
            profile_img = Image.open('profiles/default.png').convert("RGBA")
        
        profile_img = profile_img.resize((40, 40))
        img.paste(profile_img, (700, y_position - 10), profile_img)
    
    # Converter a imagem para RGB antes de salvar
    img = img.convert("RGB")
    img.save('rank_image_generated.png')

# Comando para obter o perfil de um jogador
@bot.command(name='perfil')
async def perfil(ctx, player_name: str):
    player_data = get_player_data(player_name)
    
    if player_data:
        player_level = get_player_level(player_data["player_id"])
        generate_profile_image(player_data, player_level)
        await ctx.send(file=discord.File('profile_image_generated.png'))
    else:
        await ctx.send('Perfil não encontrado ou erro ao acessar a API.')

# Comando para obter o ranking dos jogadores
@bot.command(name='ranking')
async def rank(ctx):
    top_players = get_top_players()
    
    if top_players:
        generate_rank_image(top_players)
        await ctx.send(file=discord.File('rank_image_generated.png'))
    else:
        await ctx.send('Não foi possível obter o ranking ou não há jogadores disponíveis.')

# Inicia o bot (não esqueça de substituir pelo seu token real)
bot.run(TOKEN)
