import discord
import sys
from discord.ext import commands,tasks
from mcuuid.api import GetPlayerData
from mcuuid.tools import is_valid_minecraft_username, is_valid_mojang_uuid
from utils.api import Player
import asyncio
import datetime
import os
client = commands.Bot(command_prefix="h!")
api_key = os.environ.get('HypixelAPIToken')
bot_token = os.environ.get('HypixelBotToken')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="h!help"))
    print('---------- Logged In ----------')

@client.command(aliases=['sw'])
async def skywars(ctx, username):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])
    
    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        try:
            uuid = player.uuid
        except:
            return await ctx.send("There is no minecraft player with that username.")   
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")
    player = Player(api_key, uuid)
    try:
        stats = player.getSkywarsStats()
    except:
        return await ctx.send("This player hasn't played skywars!")
    embed = discord.Embed(title=f"{name}'s Skywars Stats")
    embed.set_thumbnail(url=skin_url)
    embed.add_field(name="General", value=f'``Level``: {stats["levelFormatted"]}\n``Games Played``: {stats["games_played_skywars"]}\n``Kills``: {stats["kills"]}\n``Deaths``: {stats["deaths"]}\n``KDR``: {stats["kdr"]}\n``Wins``: {stats["wins"]}\n``Losses``: {stats["losses"]}\n``Win Rate``: {stats["win_rate"]}\n``Bow Accuracy``: {stats["bow_accuracy"]}')
    embed.add_field(name="Miscellaneous", value=f'``Coins``: {stats["coins"]}\n``Current Souls``: {stats["souls"]}\n``Total Collected Souls``: {stats["souls_gathered"]}\n``Total EXP``: {stats["skywars_experience"]}\n``Fastest Win``: {stats["fastest_win"]} seconds\n``Chests Opened``: {stats["chests_opened"]}\n``Rage Quits``: {stats["quits"]}')
    embed.set_footer(text="Note: All of this data is from the Hypixel API. If there are any inaccuracies, it is not my fault.")
    await ctx.send(embed=embed)
    del player
@client.command(aliases=['bw'])
async def bedwars(ctx, username):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])
    
    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        uuid = player.uuid
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")    
    player = Player(api_key, uuid)
    try:
        stats = player.getBedwarsStats()
    except: 
        return await ctx.send("This player hasn't played bedwars!")
    embed = discord.Embed(title=f"{name}'s Bedwars Stats")
    embed.set_thumbnail(url=skin_url)
    embed.add_field(name="General", value=f'``Games Played``: {stats["games_played_bedwars"]}\n``Kills``: {stats["kills_bedwars"]}\n``Final Kills``: {stats["final_kills_bedwars"]}\n``Deaths``: {stats["deaths_bedwars"]}\n``KDR``: {stats["kdr"]}\n``Beds Broken``: {stats["beds_broken_bedwars"]}\n``Wins``: {stats["wins_bedwars"]}\n``Losses``: {stats["losses_bedwars"]}\n``Win Rate``: {stats["win_rate"]}\n``Win Streak``: {stats["winstreak"]}')
    embed.add_field(name="Miscellaneous", value=f'``Experience``: {stats["Experience"]}\n``Beds Lost``: {stats["beds_lost_bedwars"]}\n``Items purchased``: {stats["_items_purchased_bedwars"]}\n``Total Resources Collected``: {stats["resources_collected_bedwars"]}\n``Iron Collected``: {stats["iron_resources_collected_bedwars"]}\n``Gold Collected``: {stats["gold_resources_collected_bedwars"]}\n``Diamonds Collected``: {stats["diamond_resources_collected_bedwars"]}\n``Emeralds Collected``: {stats["emerald_resources_collected_bedwars"]}')
    embed.set_footer(text="Note: All of this data is from the Hypixel API. If there are any inaccuracies, it is not my fault.")
    await ctx.send(embed=embed)
    del player

@client.command()
async def uhc(ctx, username):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])

    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        uuid = player.uuid
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")    
    player = Player(api_key, uuid)   
    try:
        stats=player.getUHCStats()
    except:
        return await ctx.send("This player hasn't played UHC!")
    embed = discord.Embed(title=f"{name}'s UHC Stats")
    embed.set_thumbnail(url=skin_url)
    embed.add_field(name="General", value=f'``Kills``: {stats["kills"]}\n``Deaths``: {stats["deaths"]}\n``KDR``: {stats["kdr"]}\n``Wins``: {stats["wins"]}\n')
    try:
        equippedKit = stats["equippedKit"].lower().replace("_", " ").capitalize()
    except:
        equippedKit = "None"
    embed.add_field(name="Miscellaneous", value=f'``Coins``: {stats["coins"]}\n``Heads Eaten``: {stats["heads_eaten"]}\n``Ultimates Crafted``: {stats["ultimates_crafted"]}\n``Equipped Kit``: {equippedKit}') 
    embed.set_footer(text="Note: All of this data is from the Hypixel API. If there are any inaccuracies, it is not my fault.")
    await ctx.send(embed=embed)
    del player

@client.command(aliases=['hg'])
async def hungergames(ctx, username):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])
                
    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        uuid = player.uuid
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")    
    player = Player(api_key, uuid)
    stats = player.getHungerGamesStats()
    embed = discord.Embed(title=f"{name}'s Hunger Games Stats")
    embed.add_field(name="General", value=f'``Wins``: {stats["wins"]}\n``Kills``: {stats["kills"]}\n``Deaths``: {stats["deaths"]}\n``KDR``: {stats["kdr"]}')
    embed.add_field(name="Miscellaneous", value=f'``Coins``: {stats["coins"]}\n``Damage Dealt``: {stats["damage"]}\n``Damage Received``: {stats["damage_taken"]}\n``Chests Opened``: {stats["chests_opened"]}')
    embed.set_thumbnail(url=skin_url)
    embed.set_footer(text="Note: All of this data is from the Hypixel API. If there are any inaccuracies, it is not my fault.")
    await ctx.send(embed=embed)
    del player    

@client.command(aliases=['d'])
async def duels(ctx, username, mode=None):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])
                
    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        uuid = player.uuid
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")    
    player = Player(api_key, uuid)
    stats = player.getDuelsStats(mode=mode)
    if mode is None:
        embed = discord.Embed(title=f"{name}'s Duels Stats")
        embed.add_field(name="General", value=f'``Games Played``: {stats["games_played_duels"]}\n``Rounds Played``: {stats["rounds_played"]}\n``Melee Swings``: {stats["melee_swings"]}\n``Melee Hits``: {stats["melee_hits"]}\n``Melee Accuracy``: {stats["sword_accuracy"]}\n``Arrows Shot``: {stats["bow_shots"]}\n``Arrows Hit``: {stats["bow_hits"]}\n``Bow Accuracy``: {stats["bow_accuracy"]}')
        embed.add_field(name="Miscellaneous", value = f'``Coins``: {stats["coins"]}\n``Health Regenerated``: {stats["health_regenerated"]}\n``Damage Dealt``: {stats["damage_dealt"]}\n``Blocks Placed``: {stats["blocks_placed"]}')
        embed.set_footer(text="You can also use h!duels <username> [gamemode]")
    elif mode == "sw":
        embed = discord.Embed(title=f"{name}'s Skywars Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["sw_duel_rounds_played"]}\n``Equipped Kit``: {stats["sw_duels_kit"].replace("_"," ").capitalize()}\n``Bow Shots``: {stats["sw_duel_bow_shots"]}\n``Melee Accuracy``: {stats["sw_duel_sword_accuracy"]}')
        embed.add_field(name="Miscellaneous", value=f'``Health Regenerated``: {stats["sw_duel_health_regenerated"]}\n``Arrows Shot``: {stats["sw_duel_bow_shots"]}\n``Blocks Placed``: {stats["sw_duel_blocks_placed"]}\n``Damage Dealt``: {stats["sw_duel_damage_dealt"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    elif mode == "uhc":
        embed = discord.Embed(title=f"{name}'s UHC Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["uhc_duel_rounds_played"]}\n``Kills``: {stats["uhc_duel_kills"]}\n``Deaths``: {stats["uhc_duel_kills"]}\n``KDR``: {stats["uhc_duel_kdr"]}\n``Wins``: {stats["uhc_duel_wins"]}\n``Losses``: {stats["uhc_duel_losses"]}\n``Win Rate``: {stats["uhc_duel_win_rate"]}\n``Melee Accuracy``: {stats["uhc_duel_sword_accuracy"]}\n``Arrows Shot``: {stats["uhc_duel_bow_shots"]}\n``Arrows Hit``: {stats["uhc_duel_bow_hits"]}\n``Bow Accuracy``: {stats["uhc_duel_bow_accuracy"]}')
        embed.add_field(name="Miscellaneous", value=f'``Health Regenerated``: {stats["uhc_duel_health_regenerated"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    elif mode == "classic":
        embed = discord.Embed(title=f"{name}'s Classic Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["classic_duel_rounds_played"]}\n``Melee Accuracy``: {stats["classic_duel_sword_accuracy"]}\n``Arrows Shot``: {stats["classic_duel_bow_shots"]}\n``Arrows Hit``: {stats["classic_duel_bow_hits"]}\n``Bow Accuracy``: {stats["classic_duel_bow_accuracy"]}')
        embed.add_field(name="Miscellaneous", value=f'``Health Regenerated``: {stats["classic_duel_health_regenerated"]}\n``Damage Dealt``: {stats["classic_duel_damage_dealt"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    elif mode == "op":
        embed = discord.Embed(title=f"{name}'s OP Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["op_duel_rounds_played"]}\n``Deaths``: {stats["op_duel_deaths"]}\n``Wins``: {stats["op_duel_wins"]}\n``Losses``: {stats["op_duel_losses"]}\n``Win Rate``: {stats["op_duel_win_rate"]}\n``Melee Accuracy``: {stats["op_duel_sword_accuracy"]}')
        embed.add_field(name="Miscellaneous", value=f'``Damage Dealt``: {stats["op_duel_damage_dealt"]}\n``Health Regenerated``: {stats["op_duel_health_regenerated"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    elif mode == "bridge":
        embed = discord.Embed(title=f"{name}'s Bridge Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["bridge_doubles_rounds_played"]}\n``Melee Accuracy``: {stats["bridge_doubles_sword_accuracy"]}\n``Arrows Shot``: {stats["bridge_doubles_bow_shots"]}\n``Arrows Hit``: {stats["bridge_doubles_bow_hits"]}\n``Bow Accuracy``: {stats["bridge_doubles_bow_accuracy"]}')
        embed.add_field(name="Miscellaneous", value=f'``Damage Dealt``: {stats["bridge_doubles_damage_dealt"]}\n``Health Regenerated``: {stats["bridge_doubles_damage_dealt"]}\n``Blocks Placed``: {stats["bridge_doubles_blocks_placed"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    elif mode == "sumo":
        embed = discord.Embed(title=f"{name}'s Sumo Duels Stats")
        embed.add_field(name="General", value=f'``Rounds Played``: {stats["sumo_duel_rounds_played"]}\n``Kills``: {stats["sumo_duel_kills"]}\n``Deaths``: {stats["sumo_duel_deaths"]}\n``KDR``: {stats["sumo_duel_kdr"]}\n``Wins``: {stats["sumo_duel_wins"]}\n``Losses``: {stats["sumo_duel_losses"]}\n``Win Rate``: {stats["sumo_duel_win_rate"]}\n``Fist Swings``: {stats["sumo_duel_melee_swings"]}\n``Fist Hits``: {stats["sumo_duel_melee_hits"]}\n``Melee Accuracy``: {stats["sumo_duel_sword_accuracy"]}')
        embed.set_footer(text="Hypixel's API changes often is oddly specific, so many of the stats will look horribly wrong and not be the same across other duel types.")
    else:
        return await ctx.send("Invalid gamemode! Valid gamemodes are ``sw, uhc, classic, bridge, sumo``.")
    embed.set_thumbnail(url=skin_url)
    await ctx.send(embed=embed)
    del player

@client.command()
async def stats(ctx, username):
    timestamp = None
    if len(sys.argv) > 1:
        identifier = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[2].isdigit():
                timestamp = int(sys.argv[2])
                
    if username is None:
        username = ctx.author.name
    identifier = username
    if is_valid_minecraft_username(identifier) or is_valid_mojang_uuid(identifier):
        player = GetPlayerData(identifier, timestamp)
        uuid = player.uuid
        name = player.username
        skin_url = f"https://mc-heads.net/body/{uuid}"
    else:
        return await ctx.send("There is no minecraft player with that username!")    
    player = Player(api_key, uuid)
    stats = player.getBasicStats()
    embed = discord.Embed(title=f"{name}'s Basic Stats")    
    embed.add_field(name="Stats", value=f'``Most Recent Game``: {stats["mostRecentGameType"]}\n``Network EXP``: {stats["networkExp"]}\n``Karma``: {stats["karma"]}\n``Current Pet``: {stats["currentPet"]}\n``Particle Pack``: {stats["particlePack"]}\n``Chat Channel``: {stats["channel"]}\n``Total Rewards Claimed``: {stats["totalRewards"]}\n``Total Daily Rewards Claimed``: {stats["totalDailyRewards"]}')
    embed.set_thumbnail(url=skin_url)
    embed.set_footer(text="You can also retrieve stats for specific games using h!<game> <username> (not all games are supported right now)")
    await ctx.send(embed=embed)




@client.command(aliases=['jb', 'juke', 'music', 'play', 'p'])
async def jukebox(ctx, song):
    songs = ['11', '13', 'stal', 'ward', 'strad', 'mall', 'mellohi', 'blocks', 'cat', 'chirp', 'far']
    if song is str:
        pass
    else:
        song = str(song)
    song = song.lower()
    if song not in songs:
        embed = discord.Embed(title="Invalid Song!")
        embed.add_field(name='Valid songs', value='11, 13, Blocks, Cat, Chirp, Far, Mall, Mellohi, Stal, Strad, Ward')
        return await ctx.send(embed=embed)
    else:
        try:
            try:            
                voice = await ctx.author.voice.channel.connect()
            except:
                voice_clients = client.voice_clients
                for voice_client in voice_clients:
                    if voice_client.guild.id == ctx.guild.id and voice_client.channel != ctx.author.voice.channel:
                        await voice_client.move_to(ctx.author.voice.channel)
                        voice = voice_client
        except:
            return await ctx.send("Join a voice channel!")   
        try:
            try:
                def done_playing(error):
                    coro = voice.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except:
                        pass
                voice.play(discord.FFmpegPCMAudio('./music/{0}.mp3'.format(song)), after=done_playing)
            except UnboundLocalError:
                voice_clients = client.voice_clients
                for voice_client in voice_clients:
                    if voice_client.guild.id == ctx.guild.id:
                        voice = voice_client
                        voice.stop()
                        def done_playing(error):
                            coro = voice.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                            try:
                                fut.result()
                            except:
                                pass
                        voice.play(discord.FFmpegPCMAudio('./music/{0}.mp3'.format(song)), after=done_playing)
        except discord.ClientException:
            try:
                def done_playing(error):
                    coro = voice.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except:
                        pass
                voice.play(discord.FFmpegPCMAudio('./music/{0}.mp3'.format(song)), after=done_playing)
            except UnboundLocalError:
                voice_clients = client.voice_clients
                for voice_client in voice_clients:
                    if voice_client.guild.id == ctx.guild.id:
                        voice = voice_client
                        voice.stop()
                        def done_playing(error):
                            coro = voice.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                            try:
                                fut.result()
                            except:
                                pass
                        voice.play(discord.FFmpegPCMAudio('./music/{0}.mp3'.format(song)), after=done_playing)



@client.command()
async def skyblock(ctx, *, arg=None):
    await ctx.send("Hey, this command is a work in progress. The Hypixel Skyblock API is a pain to deal with, so for now, use this website: https://sky.lea.more")

client.run(bot_token)

