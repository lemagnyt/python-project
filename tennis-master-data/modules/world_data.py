import geopandas
import json
import pycountry
import plotly_express as px

#On charge la data geopandas dans laquelle il ya tous les points pour tracer la carte du monde
world_init = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

#On charge notre propre data
with open('data/tennis-data.json','r') as f:
    players =json.load(f)

#On créé un dictionnaire dont les clés sont les codes iso_a3 des pays et les valeurs sont les codes iso_a2 à partir du module pycountry
#qui contient les 2
countries = {}
for country in pycountry.countries:
    countries[country.alpha_3] = country.alpha_2

#A partir de ce dictionnaire on ajoute une nouvelle colonne à notre data monde, celle des codes iso_a2, à partir de sa colonne iso_a3
#Cela nous permettra de faire le lien avec notre propre data où les joueurs possède un code iso_a2 pour leurs pays
world_init['iso_a2'] = [countries.get(country, 'Unknown code') for country in world_init['iso_a3']]
world_init = world_init[world_init['iso_a2']!='Unknown code']

#On stock les stats qu'on veut utiliser dans les maps des ranking et des goat
ranking_stats = ['Total Players','Top 200 Players','Top 100 Players','Height','Titles per player','Total Titles','Win Ratio','Ace Ratio','Total Matches','Matches per player','Age']
goat_stats = ['Total Players','Top 400 Players','Top 200 Players','Top 100 Players','Win Ratio','Grand Slams per player','Total Grand Slams','Titles per player','Total Titles','Total Matches','Matches per player']


def world_data1(mode_map):
    '''
    Returns the data for creating maps with players data.

            Parameters:
                    mode (str): the mode of the map (RANKING or GOAT) 
            Returns:
                    world (geopandas.DataFrame): data for the map
    '''
    
    #On choisit les stats à étudier en fonction du mode et on copie la data avec les points géométriques des pays
    world = world_init.copy()
    if mode_map == 'RANKING':
        mode = 'isRanking'
        rank_name = 'Current Rank'
        stats = ranking_stats
    else :
        mode = 'isGOAT'
        rank_name = 'GOAT Rank'
        stats = goat_stats
    statDict = {stat:{} for stat in stats}
   
   #On crée un dictionnaire qui contiendra les stats que l'on veut
    for code in world['iso_a2']:
        for stat in statDict:
            if(stat in ['Total Players'] or 'Total' in stat or 'Top' in stat):
                statDict[stat][code]=0
            else :
                statDict[stat][code] = [0,0]
    
    #On cherche pour chaque joueurs             
    for p in players: 
        if(players[p][mode]):
            #On cherche son pays et on le met en majuscule pour qu'il corresponde à notre nouveau dictionnaire de stats
            #On extrait toute les stats voulu dont les moyennes pour lesquels on divise la somme totale par le nombre de cas étudié
            country = players[p]['Country'].upper()
            statDict['Total Players'][country] += 1; 
            rank = int(players[p]['profile'][rank_name].split(' (')[0])
            if 'Top 400 Players' in statDict.keys()  and rank<= 400:
                statDict['Top 400 Players'][country]+=1
            if rank<= 200:
                statDict['Top 200 Players'][country]+=1
                if rank<= 100:
                    statDict['Top 100 Players'][country]+=1
            if('Total Titles' in statDict.keys() and 'Titles' in players[p]['profile']):
                nb_titles = int(players[p]['profile']['Titles'])
                title_ratio = statDict['Titles per player'][country] 
                statDict['Total Titles'][country] += nb_titles
                statDict['Titles per player'][country][0] = (title_ratio[1]*title_ratio[0] + nb_titles)/float(title_ratio[1]+1)
                statDict['Titles per player'][country][1] += 1
            if('Total Grand Slams' in statDict.keys() and 'Grand Slams' in players[p]['profile']):
                nb_grandslams = int(players[p]['profile']['Grand Slams'])
                gs_ratio = statDict['Grand Slams per player'][country] 
                statDict['Total Grand Slams'][country] += nb_grandslams
                statDict['Grand Slams per player'][country][0] = (gs_ratio[1]*gs_ratio[0] + nb_grandslams)/float(gs_ratio[1]+1)   
                statDict['Grand Slams per player'][country][1] += 1
            if('Total Matches' in statDict.keys() and 'SetsMatches' in players[p]['stats'] and 'Matches Played' in players[p]['stats']['SetsMatches']):
                nb_matches = int(players[p]['stats']['SetsMatches']['Matches Played'])
                matches_ratio = statDict['Matches per player'][country] 
                statDict['Total Matches'][country] += nb_matches
                statDict['Matches per player'][country][0] = (matches_ratio[1]*matches_ratio[0] + nb_matches)/float(matches_ratio[1]+1)   
                statDict['Matches per player'][country][1] += 1       
            if('Win Ratio' in statDict.keys() and 'SetsMatches' in players[p]['stats'] and 'Matches Won %' in players[p]['stats']['SetsMatches']):
                ratioplayer = float(players[p]['stats']['SetsMatches']['Matches Won %'][:-1])
                ratio = statDict['Win Ratio'][country] 
                statDict['Win Ratio'][country][0] = (ratio[1]*ratio[0] + ratioplayer)/(ratio[1]+1)
                statDict['Win Ratio'][country][1] += 1
            if('Age' in statDict.keys() and 'Age' in players[p]['profile']):
                age_ratio = statDict['Age'][country]
                age =(float)(players[p]['profile']['Age'][:2])
                statDict['Age'][country][0]=(age_ratio[1]*age_ratio[0] + age)/(age_ratio[1]+1)
                statDict['Age'][country][1]+=1
            if('Height' in statDict.keys() and 'Height' in players[p]['profile']):
                height_ratio = statDict['Height'][country]
                height =(float)(players[p]['profile']['Height'][:-3])
                statDict['Height'][country][0]=(height_ratio[1]*height_ratio[0] + height)/(height_ratio[1]+1)
                statDict['Height'][country][1]+=1
            if('Ace Ratio' in statDict.keys() and 'AcesDFs' in players[p]['stats'] and 'Ace %' in players[p]['stats']['AcesDFs']):
                aceStat =(float)( players[p]['stats']['AcesDFs']['Ace %'][:-1])
                ace_ratio = statDict['Ace Ratio'][country]
                ace_ratio[0]=(ace_ratio[1]*ace_ratio[0] + aceStat)/(ace_ratio[1]+1)
                statDict['Ace Ratio'][country][1]+=1
    #On stock les données de notre dictionnaire dans la dataframe où se trouve les points géométriques des pays
    for stat in statDict :  
        if stat in ['Height','Age'] or 'Ratio' in stat or 'per player' in stat :              
            for code in world['iso_a2']:
                if statDict[stat][code][1]==0 : 
                    statDict[stat][code][0]=None 
            world[stat+'_Nb']= [statDict[stat][country][1] for country in world['iso_a2']]
            world[stat]= [statDict[stat][country][0] for country in world['iso_a2']]      
        else :
            world[stat]= [statDict[stat][country] for country in world['iso_a2']] 
    #On retourne notre data         
    return world

def world_data2(matches):
    '''
    Returns the map world data for a list of matches.

            Parameters:
                    matches (dict): A list of matches

            Returns:
                    world (geopandas.DataFrame): data of the map
    '''
    #On copie la data avec les points géométriques
    world = world_init.copy()

    played = {country:0 for country in world['iso_a2']}
    lost = {country:0 for country in world['iso_a2']}
    win = {country:0 for country in world['iso_a2']}
    ratio = {country:None for country in world['iso_a2']}
    #On extrait pour tous les matches les stats voulu en fonction du pays de l'adversaire
    for match in matches :
        if match['result']=='Win':
            country = match['loser']['country']['code'].upper()
            if country == 'MC':  #Problem with players from monaco
                country = 'FR'
            win[country]+=1
        else :
            country = match['winner']['country']['code'].upper()
            if country == 'MC': 
                country = 'FR'
            lost[country]+=1
        played[country]+=1
    for country in world['iso_a2']:
        if played[country]>0:
            ratio[country]=(win[country]/played[country])*100

    #On stocke tout dans notre data où se trouve les points géométriques
    world['Played'] = played.values()
    world['Win'] = win.values()
    world['Lost'] = lost.values()
    world['Win %'] = ratio.values()
    
    #On retourne cette data
    return world
