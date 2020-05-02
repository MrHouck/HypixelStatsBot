import json
import os
from urllib.request import urlopen, Request
import datetime
class Player:
    """
    Creates a player from the UUID. 
    
    Really what this does is allow us to use the hypixel API and pass in the uuid as an argument to the URL.
    Probably don't even need a class for this lmao
    """
    def __init__(self, api_key, uuid):
        self.uuid = uuid
        self.api_key = api_key
        base_url = "https://api.hypixel.net/player?key={0}&uuid={1}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=base_url.format(api_key, uuid), headers=headers)
        response = urlopen(req)
        data = json.loads(response.read())
        if data["success"] == False:
            raise Exception(data["cause"])
        stats = data["player"]["stats"]
        try:
            self.basic = data["player"]
        except:
            pass
        try:
            self.skywars = stats["SkyWars"]
        except:
            pass
        try:
            self.bedwars = stats["Bedwars"]
        except:
            pass
        try:
            self.hunger_games = stats["HungerGames"]
        except:
            pass
        try:
            self.uhc = stats["UHC"]
        except:
            pass
        try:
            self.duels = stats["Duels"]
        except:
            pass
    def getSkywarsStats(self):
        try:
            skywars = self.skywars
        except:
            raise Exception("Can't retrieve skywars stats")
        retrieve = ["souls","games_played_skywars","coins","deaths","losses", "quits", "skywars_experience", "fastest_win", "games", "kills", "souls_gathered", "wins", "chests_opened", "arrows_shot", "arrows_hit", "levelFormatted", "bow_accuracy", "kdr", "win_rate"]
        stats = {}
        for item in retrieve:
            try:
                stats[item] = skywars[item]
            except KeyError:
                stats[item] = 0 #doing this actually saves us a ton of work later on dealing with key errors
        level = stats["levelFormatted"]
        level = level[2:]
        stats["levelFormatted"] = level 

        try:
            stats["bow_accuracy"] = round(float(stats["arrows_hit"])/float(stats["arrows_shot"]), 2)  #this is where the try: except comes into play
        except ZeroDivisionError:
            stats["bow_accuracy"] = stats["arrows_hit"]

        try:
            stats["kdr"] = round(float(stats["kills"])/float(stats["deaths"]), 2)
        except ZeroDivisionError:
            stats["kdr"] = stats["kills"]

        try:
            stats["win_rate"] = round(float(stats["wins"])/float(stats["losses"]), 2)
        except ZeroDivisionError:
            stats["win_rate"] = stats["wins"]

        return stats
        
    
    def getBedwarsStats(self):
        try:
            bedwars = self.bedwars
        except:
            raise Exception("Can't retrieve bedwars stats")
        stats = {}
        retrieve = ["games_played_bedwars", "deaths_bedwars", "kills_bedwars", "beds_lost_bedwars", "_items_purchased_bedwars", "Experience", "losses_bedwars", "wins_bedwars", "beds_broken_bedwars", "final_kills_bedwars", "resources_collected_bedwars","iron_resources_collected_bedwars", "gold_resources_collected_bedwars", "diamond_resources_collected_bedwars", "emerald_resources_collected_bedwars", "winstreak", "kdr", "win_rate"]
        for item in retrieve:
            try:
                stats[item] = bedwars[item]
            except KeyError:
                stats[item] = 0
        stats["win_rate"] = round(float(stats["wins_bedwars"])/float(stats["losses_bedwars"]), 2)
        try:
            stats["kdr"] = round(float(stats["kills_bedwars"])/float(stats["deaths_bedwars"]), 2)
        except ZeroDivisionError:
            stats["kdr"] = stats["kills_bedwars"]
        
        return stats
                

    def getUHCStats(self): 
        try:
            uhc = self.uhc
        except:
            raise Exception("Can't retrieve UHC stats")
        retrieve = ["coins","heads_eaten","deaths","kills","wins","ultimates_crafted","equippedKit", "kdr"]
        stats = {}
        for item in retrieve:
            try:
                stats[item] = uhc[item]
            except KeyError:
                stats[item] = 0
        try:
            stats["kdr"] = round(float(stats["kills"])/float(stats["deaths"]))
        except ZeroDivisionError:
            stats["kdr"] = stats["kills"]
        return stats

    def getHungerGamesStats(self):
        try:
            hg = self.hunger_games
        except:
            raise Exception("Can't retrieve hunger games stats")
        retrieve = ["deaths", "coins", "kills", "wins", "damage", "damage_taken", "chests_opened", "kdr"]
        
        stats = {}
        for item in retrieve:
            try:
                stats[item] = hg[item]
            except KeyError:
                stats[item] = 0
        
        try:
            stats["kdr"] = round(float(stats["kills"])/float(stats["deaths"]), 2)
        except ZeroDivisionError:
            stats["kdr"] = stats["kills"]
        return stats
        
    def getDuelsStats(self, mode):
        try:
            duels = self.duels
        except:
            raise Exception("Can't retrieve skywars stats")
        #jesus christ 
        gamemodes = { "sw": { "sw_duel_rounds_played", "sw_duel_blocks_placed", "sw_duel_damage_dealt", "sw_duel_melee_swings", "sw_duel_melee_swings", "sw_duel_health_regenerated", "sw_duel_bow_shots", "sw_duels_kit", "sw_duel_sword_accuracy" }, "uhc":{"uhc_duel_kills", "uhc_duel_melee_hits", "uhc_duel_melee_swings", "uhc_duel_wins", "uhc_duel_losses", "uhc_duel_deaths", "uhc_duel_bow_hits", "uhc_duel_bow_shots", "uhc_duel_rounds_played", "uhc_duel_health_regenerated", "uhc_duel_kdr", "uhc_duel_bow_accuracy", "uhc_duel_sword_accuracy", "uhc_duel_win_rate" }, "classic": {"classic_duel_rounds_played", "classic_duel_melee_hits", "classic_duel_health_regenerated", "classic_duel_damage_dealt", "classic_duel_melee_swings", "classic_duel_bow_shots","classic_duel_bow_hits", "classic_duel_bow_accuracy", "classic_duel_sword_accuracy" }, "op": { "op_duel_damage_dealt", "op_duel_deaths", "op_duel_health_regenerated", "op_duel_losses", "op_duel_melee_hits", "op_duel_melee_swings", "op_duel_rounds_played", "op_duel_sword_accuracy", "op_duel_wins", "op_duel_win_rate" }, "bridge": { "bridge_doubles_bow_hits", "bridge_doubles_bow_shots", "bridge_doubles_blocks_placed", "bridge_doubles_damage_dealt", "bridge_doubles_health_regenerated", "bridge_doubles_melee_hits", "bridge_doubles_melee_swings", "bridge_doubles_rounds_played", "bridge_doubles_sword_accuracy", "bridge_doubles_bow_accuracy" }, "sumo" : { "sumo_duel_kills", "sumo_duel_wins", "sumo_duel_rounds_played", "sumo_duel_melee_swings", "sumo_duel_melee_hits", "sumo_duel_losses", "sumo_duel_deaths", "sumo_duel_sword_accuracy", "sumo_duel_kdr", "sumo_duel_win_rate"}}
        if mode is None:
            retrieve = ["games_played_duels", "rounds_played", "melee_swings", "melee_hits", "bow_shots", "bow_hits", "bow_accuracy", "sword_accuracy", "health_regenerated", "damage_dealt", "coins", "blocks_placed"]
        elif mode not in gamemodes.keys():
            return Exception('Invalid Gamemode')
        else:
            retrieve = gamemodes[mode]
        retrieve = list(retrieve)
        stats = {}
        for item in retrieve:
            try:
                stats[item] = duels[item]
            except KeyError as e:
                stats[item] = 0
        if mode is None:
            try:
                stats["bow_accuracy"] = round(float(stats["bow_hits"])/float(stats["bow_shots"]), 2)
            except: # it can't error to zero division since if an arrow is hit, it also counts as a shot, it's really weird
                stats["bow_accuracy"] = 0

            try:
                stats["sword_accuracy"] = round(float(stats["melee_hits"])/float(stats["melee_swings"]), 2)
            except: #same problem with bow_accuracy calculation
                stats["sword_accuracy"] = 0
        elif mode == "sw":
            try:
                stats["sw_duel_sword_accuracy"] = round(float(stats["sw_duel_melee_hits"])/float(stats["sw_duel_melee_swings"]), 2)
            except:
                stats["sw_duel_sword_accuracy"] = 0

            if stats["sw_duels_kit"] == 0:
                stats["sw_duels_kit"] = "None"
        elif mode == "uhc":
            try:
                stats["uhc_duel_kdr"] = round(float(stats["uhc_duel_kills"])/float(stats["uhc_duel_deaths"]), 2)
            except ZeroDivisionError:
                stats["uhc_duel_kdr"] = stats["uhc_duel_kills"]
            
            try:
                stats["uhc_duel_sword_accuracy"] = round(float(stats["uhc_duel_melee_hits"])/float(stats["uhc_duel_melee_swings"]), 2)
            except:
                stats["uhc_duel_sword_accuracy"] = 0

            try:
                stats["uhc_duel_bow_accuracy"] = round(float(stats["uhc_duel_bow_hits"])/float(stats["uhc_duel_bow_shots"]), 2)
            except:
                stats["uhc_duel_bow_accuracy"] = 0

            try:
                stats["uhc_duel_win_rate"] = round(float(stats["uhc_duel_wins"])/float(stats["uhc_duel_losses"]), 2)
            except ZeroDivisionError:
                stats["uhc_duel_win_rate"] = stats["uhc_duel_wins"]

        elif mode == "classic":
            try:
                stats["classic_duel_bow_accuracy"] = round(float(stats["classic_duel_bow_hits"])/float(stats["classic_duel_bow_shots"]))
            except:
                stats["classic_duel_bow_accuracy"] = 0
            
            try:
                stats["classic_duel_sword_accuracy"] = round(float(stats["classic_duel_melee_hits"])/float(stats["classic_duel_melee_swings"]))
            except:
                stats["classic_duel_sword_accuracy"] = 0
        elif mode == "op":
            try:
                stats["op_duel_sword_accuracy"] = round(float(stats["op_duel_melee_hits"])/float(stats["op_duel_melee_swings"]), 2)
            except:
                stats["op_duel_sword_accuracy"] = 0
            
            try:
                stats["op_duel_wins"] = stats["op_duel_rounds_played"] - stats["op_duel_losses"]
            except:
                stats["op_duel_wins"] = 0
            
            try:
                stats["op_duel_win_rate"] = round(float(stats["op_duel_wins"])/float(stats["op_duel_losses"]), 2)
            except ZeroDivisionError:
                stats["op_duel_win_rate"] = stats["op_duel_wins"]
        elif mode == "bridge":
            try:
                stats["bridge_doubles_sword_accuracy"] = round(float(stats["bridge_doubles_melee_hits"])/float(stats["bridge_doubles_melee_swings"]), 2)
            except:
                stats["bridge_doubles_sword_accuracy"] = 0
            
            try:
                stats["bridge_doubles_bow_accuracy"] = round(float(stats["bridge_doubles_bow_hits"])/float(stats["bridge_doubles_bow_shots"]), 2)
            except:
                stats["bridge_doubles_bow_accuracy"] = 0
        elif mode == "sumo":
            try:
                stats["sumo_duel_sword_accuracy"] = round(float(stats["sumo_duel_melee_hits"])/float(stats["sumo_duel_melee_swings"]), 2)
            except:
                stats["sumo_duel_sword_accuracy"] = 0
            
            try:
                stats["sumo_duel_kdr"] = round(float(stats["sumo_duel_kills"])/float(stats["sumo_duel_deaths"]), 2)
            except ZeroDivisionError:
                stats["sumo_duel_kdr"] = stats["sumo_duel_kills"]

            try:
                stats["sumo_duel_win_rate"] = round(float(stats["sumo_duel_wins"])/float(stats["sumo_duel_losses"]))
            except ZeroDivisionError:
                stats["sumo_duel_win_rate"] = stats["sumo_duel_wins"]

        return stats
    def getBasicStats(self):
        try:
            basic = self.basic
        except:
            raise Exception("Couldn't load basic stats (this is a really bad sign)")
        retrieve = ["firstLogin", "lastLogin", "lastLogout", "networkExp", "karma", "channel", "totalRewards", "totalDailyRewards", "currentPet", "particlePack", "mostRecentGameType"]
        stats = {}
        for item in retrieve:
            try:
                stats[item] = basic[item]
            except KeyError:
                stats[item] = None

        try:
            stats["mostRecentGameType"] = stats["mostRecentGameType"].lower().capitalize()
            stats["mostRecentGameType"] = stats["mostRecentGameType"].replace("_", " ") #has to be seperate in the event that there isn't an _ in the most recent game, so that way it just skips this step but still capitalizes the game name
        except Exception as e:
            print(e)
            stats["mostRecentGameType"] = "Hasn't played any games recently."
        try:
            stats["currentPet"] = stats["currentPet"].lower().capitalize().replace("_", " ")
        except:
            pass
        try:
            stats["particlePack"] = stats["particlePack"].lower().capitalize()
            stats["particlePack"] = stats["particlePack"].replace("_", " ")
        except:
            pass

        return stats
        