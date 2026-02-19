import discord
import os

bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'✅ {bot.user} está online!')

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if msg.content == '!ping':
        await msg.channel.send('🏓 Pong!')
    
    if msg.content == '!ola':
        await msg.channel.send(f'👋 Olá {msg.author.mention}!')
    
    if msg.content == '!ajuda':
        await msg.channel.send('''
📚 **Comandos:**
!ping - Testa o bot
!ola - Saudação
!ajuda - Esta mensagem
        ''')

# Pega o token das variáveis de ambiente (mais seguro)
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
