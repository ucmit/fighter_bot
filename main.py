# Импортируем настройки бота
try:
    import conf
except ImportError:
    pass

# Импортируем библиотеки
import discord
from discord.ext import commands
import os, random

import img_handler as imhl
import fight as f



"""
    Настройка бота
"""
# Настраиваем расширенный доступ Intents
intents = discord.Intents.default()
# Даём права для просмотра участников сервера
intents.members = True
# Создаём бота, настравиваем префикс комманд и даём расширенные права
bot = commands.Bot(command_prefix="!", intents=intents)

# Список зарегистрированных Серверов
whitelist = {
    # guild_id => {channel_id => "guild_name / {channel_name}"}
    822806350886207538: {825215229725245450: "Bots / general"},
}
# Декоратор - чекер @allowed_channel    => True/False
def allowed_channel():
    async def predicate(ctx:commands.Context):
        # Если guild id И channel id валидны => True
        if ctx.guild.id in whitelist:
            if ctx.channel.id in whitelist[ctx.guild.id].keys():
                return True
        
        return False
        
    return commands.check(predicate)
"""
    Комманды бота
"""
@bot.command(name="join")
@allowed_channel()
async def vc_join(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f'Подключаюсь к {voice_channel.name}'
        await ctx.channel.send(   msg   )
        await voice_channel.connect()


@bot.command(name = "mka")
async def mka(ctx, f1:discord.Member = None, f2:discord.Member = bot.user):
    if f1 and f2:
        await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)
        await ctx.channel.send(file =discord.File(os.path.join("./img/result.gif")))

@bot.command(name="leave")
async def vc_leave(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f'Отключаюсь от {voice_channel.name}'
        await ctx.channel.send(   msg   )
        await ctx.voice_client.disconnect()

@bot.command(name="ost")
async def vs_ost(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    await ctx.channel.send(f'MORTAL COMBAAT')
    await voice_client.play(discord.FFmpegPCMAudio(source="./mp3/mk.mp3"))

@bot.command(name="fight")
@allowed_channel()
async def fight(ctx:commands.Context):
    # Первый претендент
    f1:discord.Member = None
    # Второй претендент
    f2:discord.Member = bot.user
    # Voice-канал участника
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        await vc_join(ctx)
        # Список активных пользователей
        voice_members = voice_channel.members
        # Фильтруем пользователей, оставляя только людей
        voice_members = [member for member in voice_members if member.bot == False]
        # Отбираем претендентов
        if len(voice_members) > 1:
            # a,b = [1, 2]   => a = 1    b = 2
            f1, f2 = [voice_members.pop(random.randint(0, len(voice_members)-1)), voice_members.pop(random.randint(0, len(voice_members)-1))]
        else:
            f1 = ctx.author
        # СОЗДАТЬ VS_SCREEN
        await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)

        embed = discord.Embed(
            title = "Let's Mortal Kombat Begins!",
            description = f'{f1.display_name} бьётся с {f2.display_name}',
            colour = discord.Colour.dark_purple(),
        )

        message = await ctx.channel.send(embed = embed, file=discord.File(os.path.join("./img/result.gif")))
        # ЗАПУСТИТЬ МУЗЫКУ
        voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        # await voice_client.play(discord.FFmpegPCMAudio(source="./mp3/mk.mp3"))

        await f.create_fighters(f1, f2, message)


        await voice_client.stop()

        
    else: 
        await ctx.channel.send("Зайдите в voice-канал пожажя")
"""
    Запуск бота
"""
bot.run(os.environ["BOT_TOKEN"])