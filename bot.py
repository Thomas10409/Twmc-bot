from discord.ext import commands
import discord
import json
import urllib.request, csv, os, time
import threading
from pytube import YouTube
import ffmpeg
from pytube import YouTube
import os
from pydub import AudioSegment

print(os.getcwd())

def dl_audio(ctx, url):
    sound=AudioSegment.from_file(url[32:43] + ".mp3","mp3")
    time.sleep(sound.duration_seconds)
    time.sleep(1)
    ctx.send("播放完畢")
    os.remove(url[32:43]+".mp3")

def d_audio(url):
    target_path = "./Downloads"
    yt = YouTube(url)
    video=yt.streams.filter(only_audio=True).first()
    print(video)
    out_file =video.download(output_path=target_path)
    print(out_file)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    print(new_file)
    os.rename(out_file, new_file)
    print("target path = " + (new_file))
    print("mp3 has been successfully downloaded.")
    return new_file

def covid_event():
    global out
    url = "	https://od.cdc.gov.tw/eic/covid19/covid19_tw_stats.csv"
    md = False
    ddata = False
    count = 0
    localtime = time.localtime()
    result = time.strftime("%Y-%m-%d", localtime)
    npath = os.getcwd()
    print(npath)
    dpath = npath + "/data"
    outpath = npath + "/output"
    dname = result + "-" + "data.csv"
    gdata = []
    fdpath = os.path.join(dpath,dname)


    print("covid19確診自動抓取程式")
    print("-----------------")
    print("檢查Data資料夾...")
    if not os.path.isdir(dpath):
        print("創建資料夾")
        md = True
        while md:
            if count < 3:
                os.makedirs(dpath)
                if os.path.isdir(dpath):
                    print("創建資料夾成功")
                    print("-----------------")
                    ddata = True
                    md = False
                    break
                else:
                    count = count + 1
            else:
                print("創建資料夾失敗")
                print("-----------------")
                md = False
                out = "創建資料夾失敗"
                break
    else:
        print("Data資料夾已有")
        print("-----------------")
    print("-----------------")
    print("檢查Output資料夾...")
    if not os.path.isdir(outpath):
        print("創建資料夾")
        md = True
        while md:
            if count < 3:
                os.makedirs(outpath)
                if os.path.isdir(outpath):
                    print("創建資料夾成功")
                    print("-----------------")
                    ddata = True
                    md = False
                    break
                else:
                    count = count + 1
            else:
                print("創建資料夾失敗")
                print("-----------------")
                md = False
                break
    else:
        print("Output資料夾已有")
        print("-----------------")
        ddata = True
    count = 0
    os.chdir(outpath)
    with open("output.txt",'w',newline='',encoding="utf-8") as data:
        data.write("資料抓取中")
        data.close()
    while ddata:
        print("-----------------")
        print("從網路下載資料...")
        if count < 3:
            os.chdir(dpath)
            urllib.request.urlretrieve(url, dname)
            if not os.path.isfile(fdpath):
                count = count + 1
            else:
                print("下載成功")
                print("-----------------")
                print("-----------------")
                print("開始抓資料")
                with open(dname,newline='',encoding="utf-8") as data:

                    get = csv.reader(data)
                    print("抓出來的資料")
                    for gdata in get:
                        print(gdata)
                    print("-----------------")
                os.chdir(outpath)
                print("-----------------")
                with open("output.txt",'w',newline='',encoding="utf-8") as output:
                    output.write("昨日確診:" + "\"" + gdata[0] + "\"")
                    print("昨日確診:" + "\"" + gdata[0] + "\"")
                print("-----------------")
                out = "昨日確診:" + "\"" + gdata[0] + "\""
                ddata = False
                break
        else:
            print("下載資料失敗")
            print("-----------------")
            out = "下載資料失敗"
            ddata = False
            break

bot = commands.Bot(command_prefix="\\")
bot.remove_command('help')
#@bot.event
#async def on_message(message):
#  if message.author == bot.user:
#        return
#  if message.content == 'ㄐㄐ':
#        await message.channel.send("滾回你家吃啦e04! \*以下勝#略一萬字\*")
#        return

@bot.event
async def on_ready():
    print("Bot is online!")
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name="Thomas10409爆肝打code")

    await bot.change_presence(status= status_w, activity=activity_w)

@bot.command()
async def covid(ctx):
    w = threading.Thread(target = covid_event())
    w.start()
    w.join()
    await ctx.send(out + "\n僅限台灣地區")
    print("")

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)

@bot.command()
async def ping(ctx):
    embed=discord.Embed(title="延遲:", description="Ping:" + str(round(bot.latency*1000)) + "ms", color=0x2bff00)
    await ctx.send(embed=embed)

@bot.command()
async def rickroll(ctx):
    await ctx.send("Yo! 你被rick_roll了")
    await ctx.send("https://i.imgflip.com/4whwu5.gif")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="指令列表", color=0x1bff00)
    embed.add_field(name="所有指令", value="這裡都是可以使用的指令歡迎大家使用", inline=False)
    embed.add_field(name="---------------------------------------------------------------------------------", value="᲼", inline=False)
    embed.add_field(name="\help", value="查看這個你現在正在看的東西", inline=True)
    embed.add_field(name="\ping", value="pong!延遲阿不然勒", inline=True)
    embed.add_field(name="\covid", value="獲得昨天covid確診數", inline=True)
    embed.add_field(name="\\rickroll", value="恭喜你被rickroll了嘿嘿", inline=True)

    embed.add_field(name="\\\ㄐㄐ", value="用用看你就會知道了", inline=True)
    embed.add_field(name="---------------------------------------------------------------------------------", value="᲼", inline=False)
    embed.set_footer(text="Make by Thomas10409")
    await ctx.send(embed=embed)

@bot.command()
async def ㄐㄐ(ctx):
    await ctx.send("https://c.tenor.com/-F57q8019_8AAAAd/%E3%84%94%E3%84%90%E3%84%90-%E6%94%BE%E7%81%AB.gif")
    await ctx.send("ㄔㄐㄐ")

@bot.command()
async def join(ctx):
    voice_client = ctx.author.guild.voice_client
    print(voice_client)
    print(ctx.author.voice)
    if not str(ctx.author.voice) == "None":
        if str(voice_client) == "None":
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send("我已經加到一個頻道了")
    else:
        await ctx.send("你要老子加到哪裡啊!")
        await ctx.message.add_reaction('❌')
@bot.command()
async def leave(ctx):
        if not str(ctx.author.guild.voice_client) == "None":
            channel = ctx.author.voice.channel
            voice_client = ctx.author.guild.voice_client
            if voice_client.is_playing():
            	await voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send("我根本沒加頻道退個毛阿")
            await ctx.message.add_reaction('❌')

@bot.command()
async def play(ctx,arg):
    url = arg
    yt = YouTube(url)
    _filename = yt.title
    channel = ctx.author.voice.channel
    voice_client = ctx.author.guild.voice_client
    if not str(voice_client) == "None":
        if not voice_client.is_playing():
            try:
                yt.streams.filter().get_audio_only().download(filename=url[32:43]+".mp3")
            except:
                await ctx.send("<Download Error>好像發生了點事情\n音樂下載失敗了...")
            if os.path.isfile(str(os.getcwd) + "/" + url[32:43]+".mp3"):
                await ctx.send("<Fill Not Found>好像發生了點事情\n音樂下載失敗了...")
            else:
                channel = ctx.author.voice.channel
                try:
                    await channel.connect()
                except:
                    print("emm")
                await ctx.message.add_reaction('✅')
                voice_client = ctx.author.guild.voice_client
                await ctx.send("現在播放:" + yt.title)
                voice_client.play(discord.FFmpegPCMAudio(url[32:43] + ".mp3"))
        else:
            await ctx.send("現在正在播歌\n如果要放其他的\n須等這個歌播完或是直接用stop指令停止")
    else:
        await ctx.send("我沒地方可以播啊\n哭阿")

@bot.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if not voice_client.is_playing() :
        await voice_client.stop()
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send("我什麼都還沒播啊")
        await ctx.message.add_reaction('❌')

bot.run(data['token'])
