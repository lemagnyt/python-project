import requests as rq
from bs4 import BeautifulSoup
from tqdm import tqdm
from random import randint
from time import sleep
import json




class Players:
    """
    A class to represent a list of Players.

    ...

    Attributes
    ----------
    List : list
        list of players
    TotalR : int
        number of ranking players
    TotalG : int
        number of goat players
    JSONDict : dict
        dict with data of all players in the list

    Methods
    -------
    hasPlayer(name):
        Indicates if the player with this name is present in the list
        
    getPlayer(name):
        Returns the player with this name in the list
    """
    def __init__(self,totalR,totalG):
        """
        Constructs all the necessary attributes for the players object.

        Parameters
        ----------
            totalR : int
                number of ranking players
            totalG : int
                number of goat players
        """
        self.List=[]
        self.TotalR=totalR
        self.TotalG=totalG
        self.JSONDict = dict()

    def hasPlayer(self,name):
        '''
        Returns if a player has this name in the list of players.

                Parameters:
                        name (str): the name searched
                Returns:
                        (bool): true if there is the name, false if not
        '''
        for i in self.List:
            if name == i.Name :
                return True
        return False
    
    def getPlayer(self,name):
        '''
        Returns the player with this name.

                Parameters:
                        name (str): the name searched

                Returns:
                        (Player): the player with the name
        '''
        for p in self.List:
            if p.Name == name :
                return p
        return None
        
class Player :
    """
    A class to represent a list of Players.

    ...

    Attributes
    ----------
    Name : str
        name of the player
    Id : int
        id of the player
    Country : str
        country code of the player
    Profile : dict
        dict with data profile of the player
    Stats : dict
        dict with data Stats of the player
    isGOAT : bool
        Indicates if the player is in goat players
    isRanking : bool
        Indicates if the player is in ranking players

    """
    
    def __init__(self, name,id,country) :
        """
        Constructs all the necessary attributes for the Player object.

        Parameters
        ----------
            name : str
                name of the player
            id : int
                id of the player
            country :
                the country code of the player
        """
        self.Name = name
        self.Id = id
        self.Country = country
        self.Profile=dict()
        self.Stats=dict()
        self.isGOAT=False
        self.isRanking = False
            
        
def ranking_scraping(players,mode_sleep):
    '''
    Scraps ranking players and at them in the list of players.

            Parameters:
                    players (str): the list of players (with the number of ranking players wanted)
                    mode_sleep (bool): the mode sleep to avoid ban request in the website
            Returns:
                    None
    '''
    j = 1   
    mode_sleep = False
    if mode_sleep:
        sleep(randint(4,7))
    content = rq.get("https://www.ultimatetennisstatistics.com/rankingsTableTable?current=1&rowCount=-1&sort%5Brank%5D=asc&searchPhrase=&rankType=RANK&season=&date=&_=1668603348547").json()
    for i in content['rows'][:players.TotalR]:
        player = Player(i['name'],i['playerId'],i['country']['code'])
        player.isRanking = True
        players.List.append(player)
        j+=1
        
def GOAT_scraping(players,mode_sleep):
    '''
    Scraps goat players and at them in the list of players.

            Parameters:
                    players (str): the list of players (with the number of goat players wanted)
                    mode_sleep (bool): the mode sleep to avoid ban request in the website
            Returns:
                    None
    '''
    j = 1 
    if mode_sleep:
        sleep(randint(4,7))       
    content = rq.get("https://www.ultimatetennisstatistics.com/goatListTable?current=1&rowCount=-1&sort%5BtotalPoints%5D=desc&searchPhrase=&oldLegends=true&_=1668604193476").json()
    for i in content['rows'][:players.TotalG]:
        player = Player(i['name'],i['playerId'],i['country']['code'])
        player.isGOAT = True
        if(not players.hasPlayer(player.Name)):
            players.List.append(player)
        else:
            players.getPlayer(player.Name).isGOAT = True
        j+=1



def all_data_scraping(players,mode_sleep):
    '''
    Scraps ranking and goat players, then scrap the stats and profile for each and stock them in the JSONDict of players and in a real json.

            Parameters:
                    players (str): the list of players (with the number of ranking and goat players wanted)
                    mode_sleep (bool): the mode sleep to avoid ban request in the website
            Returns:
                    None
    '''
    ranking_scraping(players,mode_sleep)
    GOAT_scraping(players,mode_sleep)    
    #All players Data stats and profile
    print('########################################### Collecting players data ###########################################')
    #On cherche pour tous les joueurs
    for p in tqdm(players.List) :
        if mode_sleep :
            sleep(randint(4,7))
        #On va d'abord stocker les infos du profil
        website = rq.get("https://www.ultimatetennisstatistics.com/playerProfileTab?playerId="+str(p.Id)).text
        soup = BeautifulSoup(website, "html.parser")
        table = soup.find_all('table',{'class':'table table-condensed text-nowrap'})
        #On va dans les différents tableaux de profils
        for t in table :
            tr = t.find_all('tr')
            for a in tr :
                #On prend le nom de l'info et l'info
                td= a.find('td')
                th = a.find('th')
                if(td!=None and th!=None and th.text!='Wikipedia' and not (th.text=='H2H %' and td.text=='0.0%')):
                    #Si c'est un continent on ne prend que le premier text
                    if(th.text == 'Country'):
                        p.Profile[th.text]=td.text[1:]
                    else :
                        p.Profile[th.text]=td.text
        if mode_sleep:   
            sleep(randint(4,7))   
        #puis  on va chercher les stats
        website = rq.get("https://www.ultimatetennisstatistics.com/playerStatsTab?playerId="+str(p.Id)) .text
        soup = BeautifulSoup(website, "html.parser")
        div = soup.find_all('div',{'class':'tab-pane fade'})
        #On cherche tous les groupes de stats
        for d in div :
            #On stock le titre du group de stat en tant que clé au dictionnaire et sa valeur sera un dictionnaire où l'on stocker les stats
            statTableName = d['id'].replace('statistics','')
            p.Stats[statTableName]=dict()
            table = d.find_all('table',{'class':'table table-condensed table-hover table-striped'})
            #On vérifie chacun de ces tableaux et on les ajoutes en valeurs à notre nouveau dictionnaire
            for t in table :
                tr = t.find_all('tr')
                for a in tr :
                    td= a.find('td')
                    th = a.find('th')
                    if(td!=None and th!=None):
                        p.Stats[statTableName][td.text]=th.text.replace('\n','')
        #Une fois qu'on a tout récupérer on peut ajouter notre data en tant que valeur du dictionnaire json avec pour clé le nom du joueur
        players.JSONDict[p.Name] = {"id":p.Id,"isGOAT":p.isGOAT, "isRanking":p.isRanking,"Country":p.Country,"profile":p.Profile,"stats":p.Stats}
    #Une fois le dictionnaire rempli on le stocke dans un fichier json
    with(open('data/tennis-data.json','w') as Tennis_data_JSON):
        json.dump(players.JSONDict,Tennis_data_JSON, indent=6)
    create_goat_table(players.JSONDict)
    create_ranking_table(players.JSONDict)
    create_stats_csv(players.JSONDict)

# take second element for sort
def takeSecond(elem):
    return elem[1]

def create_goat_table(playersDict):
    '''
    Creates a csv table for goat players in the order of their rank.

            Parameters:
                    playersDict (dict): the dict with all players data
            Returns:
                    None
    '''
    
    #On ouvre le fichier dans lequel on veut écrire notre csv
    with(open('data/goatTable.csv','w')) as f:
        #On écrit les colonnes de notre csv
        f.write('Rank,Name,Age,Country,Win Rate,Retired,Titles,GS,Points\n')
        goatList = []
        #On regarde pour tous les joueurs de notre dictionnaire
        for name in playersDict :
            #On ne garde que ceux qui sont des goats
            if playersDict[name]['isGOAT']:
                #On stock leur nom et leur rang car on veut les classer selon leur rang
                goatList.append([name,int(playersDict[name]['profile']['GOAT Rank'].split(' (')[0])])
        #On les classe dans l'ordre croissant de leur rang
        goatList.sort(key=takeSecond)
        #avec cette liste on va créer notre tableau en utilisant la data de chacun des joueurs de la liste
        #On prend les infos qui nous intéressent
        for name,rank in goatList:
            if playersDict[name]['isGOAT'] :
                Profile = playersDict[name]['profile']
                Stats = playersDict[name]['stats']
                age = 'Unknowed'       
                country = 'Unknowed'
                winRate = 'Unknowed'
                retired = 'Y'
                titles = 0
                gs = 0
                if 'Active' in Profile:
                    retired='N'
                # on stock le classement et les pointsd de classement dans 2 différentes variable
                goatRank,goatPoints = Profile['GOAT Rank'].split(' (')
                goatPoints = goatPoints.replace(')','')
                if'Age' in Profile:
                    #On isole afin d'obtenir l'âge seulement
                    age = Profile['Age'].split(' ')[0]
                if 'Titles' in Profile:
                    titles = Profile['Titles']
                if 'Grand Slams' in Profile:
                    gs = Profile['Grand Slams']
                if'Country' in Profile:
                    #On enlève les virgules présentes dans certains pays afin de ne pas gêner dans le csv
                    country = Profile['Country'].replace(',','')
                if 'SetsMatches' in Stats:
                    SetsMatches = Stats['SetsMatches']
                    #On écrit le pourcentage de victoire avec le ratio
                    winRate = str(SetsMatches['Matches Won %'])+' ('+str(SetsMatches['Matches Won']+'/'+str(SetsMatches['Matches Played'])+')')
                #On écrit toutes les infos collectées
                f.write(str(goatRank)+','+name+','+str(age)+','+country+','+winRate+','+retired+','+str(titles)+','+str(gs)+','+str(goatPoints)+'\n')

def create_ranking_table(playersDict):
    '''
    Creates a csv table for ranking players.

            Parameters:
                    playersDict (dict): the dict with all players data
            Returns:
                    None
    '''
    #Même chose que pour la fonction au dessus, 
    # mais comme on fait les joueurs ranking on n'a pas besoin de trier car c'est déjà fait dans le dictionnaire
    with(open('data/rankingTable.csv','w')) as f:
        f.write('Rank,Name,Age,Country,Win Rate,Titles,GS,Points\n')
        for name in playersDict:
            if playersDict[name]['isRanking'] :
                Profile = playersDict[name]['profile']
                Stats = playersDict[name]['stats']
                age = 'Unknowed'       
                country = 'Unknowed'
                winRate = 'Unknowed'
                titles = 0
                gs = 0
                if 'Active' in Profile:
                    retired='N'
                Rank,Points = Profile['Current Rank'].split(' (')
                Points = Points.replace(')','')
                if'Age' in Profile:
                    age = Profile['Age'].split(' ')[0]
                if 'Titles' in Profile:
                    titles = Profile['Titles']
                if 'Grand Slams' in Profile:
                    gs = Profile['Grand Slams']
                if'Country' in Profile:
                    country = Profile['Country'].replace(',','')
                if 'SetsMatches' in Stats:
                    SetsMatches = Stats['SetsMatches']
                    winRate = str(SetsMatches['Matches Won %'])+' ('+str(SetsMatches['Matches Won']+'/'+str(SetsMatches['Matches Played'])+')')
                f.write(str(Rank)+','+name+','+str(age)+','+country+','+winRate+','+str(titles)+','+str(gs)+','+str(Points)+'\n')

def create_stats_csv(playersDict):
    #On crée les csv pour les différents groupe de stats
    '''
    Creates a csv table for each group of stats for all players in the playersDict.
            Parameters:
                    playersDict (dict): the dict with all players data
            Returns:
                    None
    '''
    #On se réfère à Novak Djokovic car il possède toutes les stats possibles
    for i in playersDict['Novak Djokovic']['stats']:
        #pur chaque groupe de stats on va ouvrir un fichier différent
        with(open('data/Stats/'+i+'.csv','w')) as f:
            f.write('name')
            #On écrit le nom des autres colonnes après le nom
            for namestats in playersDict['Novak Djokovic']['stats'][i]:
                f.write('|'+namestats)
            f.write('\n')
            for name in playersDict:
                #On va filtrer les stats avec le boolean correct, si correct devient false on ne prend pas les stats pour ce joueur
                correct = True
                Stats = playersDict[name]['stats']
                if  i not in Stats or int(Stats['SetsMatches']['Matches Played'])<20: #On filtre pour avoir desj oueurs qui ont joué au moins 5 matchs
                    correct = False
                elif(Stats[i].keys()!=playersDict['Novak Djokovic']['stats'][i].keys()):
                    correct = False
                #Si le nombre d'Aces est inférieur à 20 on ne prend pas ce groupe de stat pour ce joueur
                elif (i=='AcesDFs' and int(Stats[i]['Aces'])<20):
                    correct = False
                elif (i=='ServeSpeed'):
                    #On vérifie les erreurs sur la vitesse qui sont très fréquentes
                    if float(Stats[i]['Serve Max Speed'].replace(' km/h',''))>260.3: #On vérifie qu 'il n y a pas eu d'erreur de frappe dans le serivce max dont le record est d'environ 260 km/h
                        correct = False
                    elif float(Stats[i]['Serve Max Speed'].replace(' km/h',''))<=float(Stats[i]['1st Serve Average Speed'].replace(' km/h','')):
                        correct = False
                    elif float(Stats[i]['1st Serve Average Speed'].replace(' km/h',''))<=float(Stats[i]['Serve Average Speed'].replace(' km/h','')):
                        correct = False
                #Sinon on les écrit dans le fichier    
                if correct:
                    f.write(name)
                    #On enlève les pourcent pour pouvoir obtenir des nombres pour les graphiques
                    for stats,value in playersDict[name]['stats'][i].items():
                        if '%' in value :
                            value = value.replace('%','')
                        #même chose pour les vitesses
                        elif ' km/h' in value :
                            value = value.replace(' km/h','')
                        
                        if stats=='Match Time':
                            time = value.split(':')
                            #On convertit le temps en heures au lieu de heure:minutes
                            value = str(round(float(time[0])+float(time[1])/60,2))  
                        #On écrit notre Stats                   
                        f.write('|'+value)
                    #On change de ligne quand on change de joueur    
                    f.write('\n')

#All matches data for a player
def matchesData(name,playersDict,mode_sleep,nbMatches=None):
    '''
    Scraps data for a number of matches of a player, and stock it in a json.

            Parameters:
                    name (str): the name
                    playersDict (dict) : the dict with all players Data
                    mode_sleep (bool): the mode sleep to avoid ban request in the website
                    nbMatches (int) : the number of matches wanted
            Returns:
                    None
    '''
    matches=[]
    #On regarde d'abord si le joueur est dans notre dictionnaire et donc si on peut récupérer son id. Si on ne peut pas on ne retourne rien
    if name not in playersDict:
        print('No player in te list has this name.')
        return
    #Sinon on continue et on stock la data du joueur dans player
    player = playersDict[name]
    if mode_sleep :
        sleep(randint(4,7))
    #A l'aide de son id on obtient la liste de ces matchs dont on stocké toutes les données intéressantes
    content = rq.get("https://www.ultimatetennisstatistics.com/matchesTable?playerId="+str(player['id'])+"&current=1&rowCount=-1&sort%5Bdate%5D=desc&searchPhrase=&season=&fromDate=&toDate=&level=&bestOf=&surface=&indoor=&speed=&round=&result=&opponent=&tournamentId=&tournamentEventId=&outcome=&score=&countryId=&bigWin=false&_=1668691482451").json()
    if nbMatches==None :
        nbMatches = len(content['rows'])
    print('########################################### Collection match Data for '+name+'##########################################')
    for match in tqdm(content['rows'][:nbMatches]):
        m=match
        if m['winner']['name']!=name :
            m['result']='Defeat'
        else :
            m['result']='Win'
        if(m['hasStats']):
            if mode_sleep :
                sleep(randint(4,7))
            #Si le match a des stats on va les chercher dans le html et on les stock dans la clé stat de notre match avecp our valeur un dictionnaire
            html  = rq.get("https://www.ultimatetennisstatistics.com/matchStats?matchId="+str(match['id'])).text
            soup = BeautifulSoup(html, "html.parser")
            matchStats = dict()
            #on cherche le nom du premier joueur
            player1 = soup.find('div',{'class':'col-xs-5 text-left'}).text
            matchStats[player1]=dict()
            #On cherche le nom du 2 ème joueur
            player2 = soup.find('div',{'class':'col-xs-5 text-right'}).text#pour les 2 joueurs on crée une clée par rapport au dictionnaire des stats
            
            matchStats[player2]=dict()
            table = soup.find_all('table',{'class':'table table-condensed table-hover table-striped text-nowrap'})
            #On parcour tous les tableaux et on stocke les stats des 2 joueurs du match
            for t in table[1:] :
                tr = t.find_all('tr')
                for a in tr :
                    title_test = a.find('th',{'class':'text-center'})
                    if title_test!=None:
                        title=title_test.text
                        if(title!='Time'):
                            matchStats[player1][title]=dict()
                            matchStats[player2][title]=dict()
                        else:
                            matchStats['Time']=dict() 
                    else :
                        th = a.find_all('th')
                        stat = a.find('td').text
                        if(title != 'Time'):
                            #si il y a un ratio et un pourcentage on les sépare en 2 différentes clée pour la stat
                            if(len(th)==4):
                                matchStats[player1][title][stat]=dict()
                                matchStats[player2][title][stat]=dict()                            
                                matchStats[player1][title][stat]['ratio']=th[1].text
                                matchStats[player2][title][stat]['ratio']=th[2].text
                                matchStats[player1][title][stat]['pct']=th[0].text
                                matchStats[player2][title][stat]['pct']=th[3].text                          
                            else :
                                matchStats[player1][title][stat]=th[0].text
                                matchStats[player2][title][stat]=th[1].text
                        else :
                            matchStats[title][stat]=th[1].text
            #on stock notre dictionnaire de stat en tant que valeur de stat pour ce match dans notre liste de match
            m['stats']=matchStats
        #On ajoute notre match à notre list de matchs
        matches.append(m)
    #Une fois tous les matchs ajoutés on stocke la liste dans un json
    with(open('data/matches_'+name.replace(' ','_')+'.json','w') as Tennis_data_JSON):
        json.dump(matches,Tennis_data_JSON, indent=6)           




