import dash
from dash import html, dcc,callback
import dash_bootstrap_components as dbc
import json
import pandas as pd
from dash import dash_table
from dash.dependencies import Output,Input,State
import plotly_express as px
import modules.world_data as world_data

names  = ['Roger Federer','Novak Djokovic','Rafael Nadal']
with open('data/tennis-data.json','r') as f:
    players =json.load(f)

matches = {}
for name in names :
    with open('data/matches_'+name.replace(' ','_')+'.json','r') as f:
        matches[name]=json.load(f)
        
def filtre_data(dataframe):
    '''
    Returns the min and max of the data when its filtred.

            Parameters:
                    dataframe (pd.DataFrame): the data
            Returns:
                    list[filtre] (int or float): the minimum of the data filtred
                    list[length-filtre] (int or float): the maximum of the data filtred
                    
    '''
    list = sorted(dataframe)
    length = len(dataframe)
    filtre = int(length/33) #On enlève les 3% du début et de la fin de la data
    return [list[filtre],list[length-filtre]]
#------------------------------------------------ Profiles ------------------------------------------------------#
# On va récupérer les profiles de nos trois joueurs et les stocjé dans un dictionnaire afin de le convertir ensuite en dataFrame

#Ici on sélectionne toutes les données voulues
infos = [i for i in players['Novak Djokovic']['profile']]+['Retired','Olympics']

#Ici on enlève celles que l'on ne veut pas dans celles choisies
for info in ['Facebook','Peak Elo Rating','Website','Current Elo Rank','Twitter']:
    if info in infos :
        infos.remove(info)

#Puis on passe au remplissage du dictionnaire
profilesdict = {'Infos':[i for i in infos]}
for name in names:
    profilesdict[name]=[]
    for info in profilesdict['Infos']:
        if info not in players[name]['profile']:
            profilesdict[name].append('')
        else:
            profilesdict[name].append(players[name]['profile'][info])
profilesData = pd.DataFrame(profilesdict)

#------------------------------------------------- Stats ---------------------------------------------------------#

#On va récupérer les stats pour chaque joueur
stats = {}

#On prend toujours en référence Djokovic car il possède toutes les stats possibles dans notre data
for title in players['Novak Djokovic']['stats']:
    stats[title]={'Stat':[stat for stat in players['Novak Djokovic']['stats'][title]]}
    for name in names:
        stats[title][name]=[]
        if title in players[name]['stats']:
            for stat in players['Novak Djokovic']['stats'][title]:
                if stat in players[name]['stats'][title]:
                    stats[title][name].append(players[name]['stats'][title][stat])
                else:
                    stats[title][name].append('')
        else :
            for stat in players['Novak Djokovic']['stats'][title]:
                stats[title][name].append('')
                
#---------------------------------------- Grand Slams and Titles Race --------------------------------------------#

#On va stocker dans un tableau tous les résultats de grand chelem et le nombre de titre au fil des années
# en allant regarder tous les matchs pour chaque joueur dans la data
GS = {}
raceTitles={}
raceGS={}
raceATPFinals = {}
GSData = {}
raceM1000= {}

#le nom des différents grand chelems
for gs in ['Wimbledon','US Open','Australian Open','Roland Garros']:
    GS[gs]={}
    GSData[gs]={'Year':[str(y) for y in range(1999,2023)]}
    for y in range(1999,2023):
        GS[gs][str(y)]={}

#Pour chaque joueur du big three
for name in names :
    raceTitles[name]={str(y):0 for y in range(1999,2023)}
    raceGS[name]={str(y):0 for y in range(1999,2023)}
    raceM1000[name]={str(y):0 for y in range(1999,2023)}
    raceATPFinals[name]={str(y):0 for y in range(1999,2023)}
    id = -1
    #chacun de leur match
    for match in matches[name]:
        #On stocke l'année du match
        year = match['date'][:4]
        #Pour savoir si le tournoi est gagné on regarde si le match est une finale et si il a été gagné,
        # on stock ensuite en fonction du level pour connaître le type de tournoi
        if match['round']=='F' and match['result']=='Win':
            raceTitles[name][year]+=1
            if match['level']=='M':
                raceM1000[name][year]+=1
            if match['level']=='F':
                raceATPFinals[name][year]+=1
        if match['level']=='G' and (match['tournamentEventId']!=id):
            tournament = match['tournament']
            id = match['tournamentEventId']
            roundGS = match['round']
            if roundGS == 'F' and match['result']=='Win':
                roundGS = 'Win'
                raceGS[name][year]+=1
            GS[tournament][year][name]=roundGS
    #On additionne chaque année les titres gagnés car on veut l'évolution du nombre de titre au fil des années
    for y in range(2000,2023):
        raceGS[name][str(y)]+=raceGS[name][str(y-1)]
        raceM1000[name][str(y)]+=raceM1000[name][str(y-1)]
        raceTitles[name][str(y)]+=raceTitles[name][str(y-1)]
        raceATPFinals[name][str(y)]+=raceATPFinals[name][str(y-1)]

#---------------------------------------- Histograms Matches Stats --------------------------------------------#

#On va stocker les données qu 'on veut pour les histos dans le bon format de dictionnaire afin de pouvoir le convertir en dataFrame encore une fois
histoStats = {}
for name in names :
    #On choisit nos stats
    histoStats[name]={'Aces per Set':[],'DFs per Set':[],'Total Points Won %':[],'1st Serve %':[],'1st Serve Won %':[],'2nd Serve Won %':[],
                      'Return Points Won %':[],'Break Points Won %':[],'Match Time':[]}
    #A chaque match on ajoute la stat obtenue
    for match in matches[name] :
        if match['hasStats']:
            histoStats[name]['Aces per Set'].append(float(match['stats'][name]['Aces']['Aces per Set']['pct']))
            histoStats[name]['DFs per Set'].append(float(match['stats'][name]['Double Faults']['DFs per Set']['pct']))
            histoStats[name]['Total Points Won %'].append(float(match['stats'][name]['Points & Games']['Total Points Won %']['pct'][:-1]))
            histoStats[name]['1st Serve %'].append(float(match['stats'][name]['Serve']['1st Serve %']['pct'][:-1]))
            histoStats[name]['1st Serve Won %'].append(float(match['stats'][name]['Serve']['1st Serve Won %']['pct'][:-1]))
            histoStats[name]['2nd Serve Won %'].append(float(match['stats'][name]['Serve']['2nd Serve Won %']['pct'][:-1]))
            histoStats[name]['Return Points Won %'].append(float(match['stats'][name]['Points']['Return Points Won %']['pct'][:-1]))
            try :
                histoStats[name]['Break Points Won %'].append(float(match['stats'][name]['Points']['Break Points Won %']['pct'][:-1]))
            except :
                histoStats[name]['Break Points Won %'].append(None)
            #Pour le temps on va convertir une stats du format H:min en heures
            time = match['stats']['Time']['Match Time']
            if ':' in time:
                time = float(time.split(':')[0])*60+float(time.split(':')[1])
            else :
                time = float(time)
            histoStats[name]['Match Time'].append(time)
            
def histograms_list(stat):
    '''
    Returns the list of histograms for a stat.

            Parameters:
                    stat (str): the stat

            Returns:
                    histograms (list): the list of histograms
    '''
    histograms = []
    for name in names :    
        histoData = pd.DataFrame(histoStats[name])
        filtre = filtre_data(histoData[stat])
        graphData= histoData[(histoData[stat]<=filtre[1]) & (histoData[stat]>=filtre[0])]
        fig = px.histogram(graphData,x=stat,nbins=20,title='Histogram of \''+stat+'\' for '+name)
        fig.update_layout(height=650,title_x=0.5)
        histograms.append(dcc.Graph(figure=fig))
    return histograms

#----------------------------------------------------- Oponnent's Countries Map --------------------------------------------------#

#Ici on va créer nos différentes map des joueurs affrontés en fonction du pays

#On obtient la data pour nos maps
world = [world_data.world_data2(matches[name]) for name in names]
 
def maps_list(stat) :
    '''
    Returns the list of maps for a stat.

            Parameters:
                    stat (str): the stat

            Returns:
                    maps (list): the list of maps
    '''
    maps=[]
    i=0
    for w in world:
        map = px.choropleth(w,locations="iso_a3",color=stat,color_continuous_scale=px.colors.sequential.Plasma,title = "Matches "+stat+ " per Country for "+names[i])
        i+=1
        map.update_layout(margin=dict(l=20, r=20, b=20, t=40),
                  width=1200, 
                  height=600,title_x=0.5)
        hovertemplate = ['Country : %{customdata[0]}']
        if stat=='Win %':
            hovertemplate.append(stat+' : %{customdata[1]:.2f}')
            hovertemplate.append('Win : %{customdata[2]:.0f}')
            hovertemplate.append('Lost : %{customdata[3]:.0f}')
            map.update_traces(customdata=w[['name',stat,'Win','Played']],hovertemplate="<br>".join(hovertemplate))
            
        else :
            hovertemplate.append(stat+' : %{customdata[1]:.0f}')
            map.update_traces(customdata=w[['name',stat]],hovertemplate="<br>".join(hovertemplate))
        maps.append(dcc.Graph(figure=map))
    return maps
#--------------------------------------------------------------- H2H --------------------------------------------------------------#
#Ici on va créer nos tableaux de Head to head entre 2 des 3 joueurs, c'est-à-dire leurs stats par affrontements
H2H = {name:{} for name in names}

other_names=names.copy()
SurfaceRatio = {name : {} for name in names}
for name in names :
    names1 = names.copy()
    names1.remove(name)
    for player in names1 :
        #On choisit les stats qu'on veut
        H2H[name][player]={'withStats':0,'Matches':0,'Total Points Played':0,'Total Games Played':0,'Total Sets Played':0,'Total Tie-Breaks Played':0,'Match Time':0,'Win':0,'Lost':0,'Win %':None,'Grass Ratio':'','Hard Ratio':'',
                       'Clay Ratio':'','Stats':{}}
        H2H[name][player]['Stats'] = {'Aces per Set':0,'DFs per Set':0,'Total Points Won %':0,'1st Serve %':0,'1st Serve Won %':0,'2nd Serve Won %':0,
                'Return Points Won %':0,'Break Points Won %':0}
        SurfaceRatio[name][player]={'G':[0,0],'C':[0,0],'H':[0,0]}
for name in other_names:
    statH2H = {name:{'Aces per Set':0,'DFs per Set':0,'Total Points Won %':0,'1st Serve %':0,'1st Serve Won %':0,'2nd Serve Won %':0,
                'Return Points Won %':0,'Break Points Won %':0}for name in other_names}
    #Cette liste correspond aun noms des joueurs dont on va étudier le Head to head face à notre joueur 'name'.
    other_names.remove(name)
    for match in matches[name]:
        #On va regarder tous les matchs de notre joueurs et chercher le nom de l'adversaire
        if match['result']=='Win':
            oponnent = match['loser']['name']
        else :
            oponnent = match['winner']['name']
        #Si ce nom est dans la liste défini tout à l'heure on va stocker ses stats
        if oponnent in other_names and oponnent!=name:
            if match['result']=='Win':
                H2H[name][oponnent]['Win']+=1
                SurfaceRatio[name][oponnent][match['surface']][0]+=1
                H2H[oponnent][name]['Lost']+=1
            else:
                H2H[name][oponnent]['Lost']+=1
                H2H[oponnent][name]['Win']+=1
                SurfaceRatio[oponnent][name][match['surface']][0]+=1
            players = [name,oponnent]
            for i in range (0,2):
                H2Hplayer = H2H[players[i]][players[(i+1)%2]]
                SurfaceRatio[players[i]][players[(i+1)%2]][match['surface']][1]+=1
                H2Hplayer['Matches']+=1
                for set in match['score'].split(' '):
                    H2Hplayer['Total Sets Played']+=1
                    if '7-6' in set:
                        H2Hplayer['Total Tie-Breaks Played']+=1
                #On vérifie que le match a des stats, si oui on additionne toutes ses stats et on augmente le nombre de match étudié par 1 pour pouvoir faire une moyenne plus tard
                if match['hasStats']:
                    H2Hplayer['withStats']+=1
                    H2Hplayer['Stats']['Aces per Set']+=float(match['stats'][players[i]]['Aces']['Aces per Set']['pct'])
                    H2Hplayer['Stats']['DFs per Set']+=float(match['stats'][players[i]]['Double Faults']['DFs per Set']['pct'])
                    H2Hplayer['Stats']['Total Points Won %']+=float(match['stats'][players[i]]['Points & Games']['Total Points Won %']['pct'][:-1])
                    H2Hplayer['Stats']['1st Serve %']+=float(match['stats'][players[i]]['Serve']['1st Serve %']['pct'][:-1])
                    H2Hplayer['Stats']['1st Serve Won %']+=float(match['stats'][players[i]]['Serve']['1st Serve Won %']['pct'][:-1])
                    H2Hplayer['Stats']['2nd Serve Won %']+=float(match['stats'][players[i]]['Serve']['2nd Serve Won %']['pct'][:-1])
                    H2Hplayer['Stats']['Return Points Won %']+=float(match['stats'][players[i]]['Points']['Return Points Won %']['pct'][:-1])
                    if match['stats'][players[i]]['Points']['Break Points Won %']['pct']!='' :
                        H2Hplayer['Stats']['Break Points Won %']+=float(match['stats'][players[i]]['Points']['Break Points Won %']['pct'][:-1])
                    time = match['stats']['Time']['Match Time']
                    if ':' in time:
                        time = float(time.split(':')[0])*60+float(time.split(':')[1])
                    else :
                        time = float(time)
                    H2Hplayer['Match Time']+=time
                    H2Hplayer['Total Points Played']+=int(match['stats'][players[i]]['Points & Games']['Total Points Played'])
                    H2Hplayer['Total Games Played']+=int(match['stats'][players[i]]['Points & Games']['Total Games Played'])
    for oponnent in other_names :
        players = [oponnent,name]
        for i in range(0,2):
            H2Hplayer = H2H[players[i]][players[(i+1)%2]]
            #On va ici faire la moyenne pour chaque stat car pour le moment on avait la somme de chacune d'entre elles
            H2Hplayer['Stats']={stat:round(H2Hplayer['Stats'][stat]/(H2Hplayer['withStats']),2) for stat in statH2H[name]}
            stringTime = str(round(H2Hplayer['Match Time']/H2Hplayer['withStats'],2))+' min per match (Total : '+ str(H2Hplayer['Match Time'])+' min for '+str(H2Hplayer['withStats'])+'/'+str(H2Hplayer['Matches'])+' matches)'
            H2Hplayer['Match Time']=stringTime 
            H2Hplayer ['Total Points Played']=str(H2Hplayer ['Total Points Played'])+ ' (for '+str(H2Hplayer['withStats'])+'/'+str(H2Hplayer['Matches'])+' matches)'
            H2Hplayer ['Total Games Played']=str(H2Hplayer ['Total Games Played'])+ ' (for '+str(H2Hplayer['withStats'])+'/'+str(H2Hplayer['Matches'])+' matches)'            
            if H2Hplayer['Matches']>0:
                H2Hplayer['Win %']=round(float(H2Hplayer['Win'])/H2Hplayer['Matches'],2)
            ratioG = SurfaceRatio[players[i]][players[(i+1)%2]]['G']
            ratioC = SurfaceRatio[players[i]][players[(i+1)%2]]['C']
            ratioH = SurfaceRatio[players[i]][players[(i+1)%2]]['H']
            H2Hplayer['Grass Ratio']=str(round(float(ratioG[0])*100/float(ratioG[1]),1))+' % ('+str(ratioG[0])+'/'+str(ratioG[1])+')'
            H2Hplayer['Clay Ratio']=str(round(float(ratioC[0])*100/float(ratioC[1]),1))+' % ('+str(ratioC[0])+'/'+str(ratioC[1])+')'
            H2Hplayer['Hard Ratio']=str(round(float(ratioH[0])*100/float(ratioH[1]),1))+' % ('+str(ratioH[0])+'/'+str(ratioH[1])+')'
#--------------------------------------------------------------- Data --------------------------------------------------------------#

#Ici on va créer nos différents tableaux à parti de la data obtenue

#On crée notre data pour le tableau des Grand chelem à partir de l'année
for gs in GS:
    for y in GS[gs]:
        for name in names:
            if name not in GS[gs][y]:
                GS[gs][y][name]='Not Played'

GScolumns=[{"name": ["", "Year"], "id": "year"}]
GScolumns_id=['year']
GSdata = []
for name in names :
    for gs in [('AO','Australian Open'),('RG','Roland Garros'),('W','Wimbledon'),('UO','US Open')]:
        id = name.replace(' ','_')+'_'+gs[0]
        GScolumns_id.append(id)
        GScolumns.append({"name": [name, gs[0]], "id": id})
for y in range(1999,2023):
    GSdict = {'year':y}
    for name in names:
        for gs in [('AO','Australian Open'),('RG','Roland Garros'),('W','Wimbledon'),('UO','US Open')]:
            id = name.replace(' ','_')+'_'+gs[0]
            GSdict[id]=GS[gs[1]][str(y)][name]
    GSdata.append(GSdict)



#On crée le tableau à partir de la data en mettant des couleurs en fonction du résultat, et de la surface pour les noms de tournoi
tableGS = dash_table.DataTable(
    columns=GScolumns,
    data = GSdata,
    merge_duplicate_headers=True,style_header={'textAlign': 'center'},style_cell={'textAlign': 'center'},
    style_data_conditional=[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= Win'
            },
            'backgroundColor': 'green'
        }for column_id in GScolumns_id

    ] +[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "Not Played"'
            },
            'backgroundColor': 'grey'
        }for column_id in GScolumns_id

    ]+[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "F"'
            },
            'backgroundColor': 'blue'
        }for column_id in GScolumns_id

    ]+[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "SF" || {'+column_id+'}= "QF"'
            },
            'backgroundColor': 'cyan'
        }for column_id in GScolumns_id
    ]+[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "R32" || {'+column_id+'}= "R16"'
            },
            'backgroundColor': 'yellow'
        }for column_id in GScolumns_id
    ]+[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "R64"'
            },
            'backgroundColor': 'orange'
        }for column_id in GScolumns_id
    ]+[
        {
            'if': {
                'column_id':column_id,
                'filter_query': '{'+column_id+'}= "R128"'
            },
            'backgroundColor': 'red'
        }for column_id in GScolumns_id
    ],
    style_header_conditional=[
        {
            'if': {
                'column_id': name.replace(' ','_')+'_AO',
                'header_index': 1
            },
            'backgroundColor': 'blue'
        }
        for name in names
    ]+[
        {
            'if': {
                'column_id': name.replace(' ','_')+'_UO',
                'header_index': 1
            },
            'backgroundColor': 'blue'
        }
        for name in names
    ]+[
        {
            'if': {
                'column_id': name.replace(' ','_')+'_RG',
                'header_index': 1
            },
            'backgroundColor': 'orange'
        }
        for name in names
    ]+[
        {
            'if': {
                'column_id': name.replace(' ','_')+'_W',
                'header_index': 1
            },
            'backgroundColor': 'lime'
        }
        for name in names
    ]
)

#On crée toutes les data pour les graphiques pour chaque joueurs
raceGSData = {'Year': [y for y in range(1999,2023)]}
raceM1000Data = {'Year': [y for y in range(1999,2023)]}
raceTitlesData = {'Year': [y for y in range(1999,2023)]}
raceATPFinalsData = {'Year': [y for y in range(1999,2023)]}
for name in names:
    raceGSData[name]=[nb for nb in list(raceGS[name].values())]
    raceTitlesData[name]=[nb for nb in list(raceTitles[name].values())]
    raceM1000Data[name]=[nb for nb in list(raceM1000[name].values())]
    raceATPFinalsData[name]=[nb for nb in list(raceATPFinals[name].values())]

#On crée ensuite la data pour nos tableaux H2H. Au total on fait 3 tableaux, 2 avec des infos et 1 avec les stats
H2HData = {}
for name in names:
    other_names = names.copy()
    other_names.remove(name)
    for oponnent in other_names:
        H2Hdict = H2H[name][oponnent]
        H2Hdict1 = H2H[oponnent][name]
        H2HInfo1 = {'Infos':[key for key in H2Hdict][1:7],'Value':[value for value in H2Hdict.values()][1:7]}
        H2HInfo2 = {name:[value for value in H2Hdict.values()][7:-1],'Stats':[key for key in H2Hdict][7:-1],
                oponnent:[value for value in H2Hdict1.values()][7:-1]}
        H2HStats = {name:[stat for stat in H2Hdict['Stats'].values()],'Stats':[stat for stat in H2Hdict['Stats']],
                    oponnent:[stat for stat in H2Hdict1['Stats'].values()]}
        H2HData[name+' - '+oponnent] = {'Info1':H2HInfo1,'Info2':H2HInfo2,'Stats':H2HStats}


def table_H2H(player1,player2):
    '''
    Returns the H2H tables.

            Parameters:
                    player1 (str): first player of the H2H
                    player2(str): second player of the H2H

            Returns:
                    (list) : the 3 different tables
    '''
    tableName = player1+' - '+player2
    tableH2HInfo1 = dash_table.DataTable(pd.DataFrame(H2HData[tableName]['Info1']).to_dict('records'),
                    style_header={'display': 'none'},
                    style_cell={'textAlign': 'center','height': 'auto','minWidth': '100px', 'width': '100px', 'maxWidth': '100px','whiteSpace': 'normal'},
                    cell_selectable=False,id = 'dbt-tableH2H1')

    tableH2HInfo2 = dash_table.DataTable(pd.DataFrame(H2HData[tableName]['Info2']).to_dict('records'),
                    style_header={'textAlign' : 'center'},
                    style_cell={'textAlign': 'center','height': 'auto','minWidth': '100px', 'width': '100px', 'maxWidth': '100px','whiteSpace': 'normal'},
                    cell_selectable=False)

    tableH2HStats = dash_table.DataTable(pd.DataFrame(H2HData[tableName]['Stats']).to_dict('records'),
                    style_header={'display': 'none'},
                    style_cell={'textAlign': 'center','height': 'auto','minWidth': '100px', 'width': '100px', 'maxWidth': '100px','whiteSpace': 'normal'},
                    cell_selectable=False)
    return [tableH2HInfo1,html.Br(),tableH2HInfo2,tableH2HStats]


#On initialise notre graphique de course aux titres avec la course au grand chelems
df = pd.DataFrame(raceGSData)
fig = px.line(df, x='Year', y=df.columns[1:],title="Grand Slams' Race")


#On crée notre tableau de profiles à partir de la data
table = dash_table.DataTable(profilesData.to_dict('records'),
                style_header={'textAlign': 'center'},
                style_cell={'textAlign': 'center','height': 'auto','minWidth': '180px', 'width': '180px', 'maxWidth': '180px','whiteSpace': 'normal'},
                cell_selectable=False,page_size=16)

def create_table_stats(statTitle):
    tableStats = dash_table.DataTable(pd.DataFrame(stats[statTitle]).to_dict('records'),
                    style_header={'textAlign':'center'},
                    style_cell={'textAlign': 'center','height': 'auto','minWidth': '180px', 'width': '180px', 'maxWidth': '180px','whiteSpace': 'normal'},
                    cell_selectable=False)
    return tableStats

dash.register_page(
    __name__,
    path='/big-three',
    title='The Big Three',
    name='The Big Three'
)

layout = dbc.Container(children=[
    html.H3('THE BIG THREE',style={"font-size": "80px",'textAlign':'center'}),html.Br(),html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Profiles',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            table,html.Br(),
            
            dcc.Dropdown(list(stats.keys()),value='AcesDFs',id='dbt-DdTableStats'),
            html.H3('Stats',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            html.Div(create_table_stats('AcesDFs'),id='dbt-tableStats'),html.Br(),html.Br(),html.Br(),
            
            html.H3('Head to Head',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=names,value=names[0],id='dbt-playerH2H1'),html.Br(),
                    html.Center(html.Img(src=dash.get_asset_url('nadal.jpg'),id='dbt-imageH2H1'))],align=True,width={'offset':0, 'order':'first'}),
                dbc.Col([
                    dcc.Dropdown(options=names,value=names[1],id='dbt-playerH2H2'),html.Br(),
                    html.Center(html.Img(src=dash.get_asset_url('federer.jpg'),id='dbt-imageH2H2'))],align=True,width={'offset':0, 'order':'last'}),
            ],justify='center'),
            html.Div(table_H2H('Roger Federer','Rafael Nadal'),id='dbt-tableH2H')               
            ,html.Br(),html.Br(),html.Br(),
            
            html.H3('Grand Slams Results',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            tableGS,html.Br(),html.Br(),html.Br(),
            
            html.H3('Titles Race',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            dcc.Dropdown(['Grand Slams','Masters 1000','ATP Finals','Titles'],value='Grand Slams',id='dbt-DdRace')
            ,dcc.Graph(figure=fig,id='dbt-figRace')
        ],width={'size':8,'order':'center'}),  
    ],justify='center'),html.Br(),html.Br(),html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.H3('Oponnents Map',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),dcc.Dropdown(world[0].columns[-4:],value='Win %',id='dbt-Ddmap')
        ]),
        dbc.Col([
                    html.Center(html.H3('Stat Histograms',style={"font-size": "50px", "text-decoration": "underline"})),html.Br(),html.Br(),dcc.Dropdown(list(histoStats[names[0]].keys()),value='Aces per Set',id='dbt-histoStats')
        ])
    ],justify='around'),html.Br(),
    html.H3('Roger Federer',style={"font-size": "30px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
    dbc.Row(id = 'dbt-histomap1',justify='around'),html.Br(),html.Br(),
    
    html.H3('Rafael Nadal',style={"font-size": "30px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
    dbc.Row(id = 'dbt-histomap2',justify='around'),html.Br(),html.Br(),
       
    html.H3('Novak Djokovic',style={"font-size": "30px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
    dbc.Row(id = 'dbt-histomap3',justify='around')        
],fluid=True)

@callback(Output('dbt-tableStats','children'),Input('dbt-DdTableStats','value'))
def updata_table_stats(statTitle):
    '''
    Updates the table stats by changing the groupe of stats title.

            Parameters:
                    statTitle(str) : the group of stat title

            Returns:
                    (dash.DataTable) : the table created
    '''
    return create_table_stats(statTitle)

@callback(Output('dbt-playerH2H2','options'),Input('dbt-playerH2H1','value'))
def H2Htables(player):
    '''
    Return the second dropdown options depending on the first dropdown value for the H2H

            Parameters:
                    player (str): first player of the H2H

            Returns:
                    other_names (list) : a list of name without the name already selected in the first dropdown
    '''
    #On renvoie une liste des noms sans le nom déjà présent dans le premier dropdown afin de ne pas pouvoir l'utiliser 2 fois
    other_names = names.copy()
    other_names.remove(player)
    return other_names

@callback(Output('dbt-playerH2H1','options'),Input('dbt-playerH2H2','value'))
def H2Htables(player):
    '''
    Return the first dropdown options depending on the second dropdown value for the H2H

            Parameters:
                    player (str): second player of the H2H

            Returns:
                    other_names (list) : a list of name without the name already selected in the second dropdown
    '''
    other_names = names.copy()
    other_names.remove(player)
    return other_names

@callback(Output('dbt-imageH2H1','src'),Input('dbt-playerH2H1','value'))
def update_image1(player) :
    '''
    Updates the image depending on the player the selected

            Parameters:
                    player (str): player selected

            Returns:
                    (dash.get_asset_url) : the url image of the player
    '''
    imageName = player.split(' ')[1].lower()+'.jpg'
    return dash.get_asset_url(imageName)

@callback(Output('dbt-imageH2H2','src'),Input('dbt-playerH2H2','value'))
def update_image2(player) :
    '''
    Updates the image depending on the player the selected

            Parameters:
                    player (str): player selected

            Returns:
                    (dash.get_asset_url) : the url image of the player
    '''
    imageName = player.split(' ')[1].lower()+'.jpg'
    return dash.get_asset_url(imageName)

@callback(Output('dbt-tableH2H','children'),Input('dbt-playerH2H1','value'),Input('dbt-playerH2H2','value'))
def H2Htables(player1,player2):
    '''
    Updates the H2H table depending on the two player selected

            Parameters:
                    player1 (str): first player selected
                    player2 (str): second player selected

            Returns:
                    (dash.dataTable) : the 3 H2H tables
    '''
    return table_H2H(player1,player2)

@callback(Output('dbt-figRace','figure'),Input('dbt-DdRace','value'))
def raceGraph(tournament):
    '''
    Updates the race tournament graphic depending on the tournament the selected

            Parameters:
                    tournament (str): tournament selected

            Returns:
                    figRace (px.line) : the graphic wanted
    '''
    if(tournament=='Grand Slams'):
        dataRace = pd.DataFrame(raceGSData)
    elif(tournament=='ATP Finals'):
        dataRace = pd.DataFrame(raceATPFinalsData)
    elif(tournament=='Masters 1000'):
        dataRace = pd.DataFrame(raceM1000Data)
    elif(tournament=='Titles'):
        dataRace = pd.DataFrame(raceTitlesData)        
    figRace = px.line(dataRace, x='Year', y=df.columns[1:],height=800,width=1600,title='Number of '+tournament+' won over the years by the Big Three')
    #Pour pouvoir comparer les 3 données sur le graphique en fonction de l'année
    figRace.update_traces(mode="markers+lines", hovertemplate=None)
    figRace.update_layout(yaxis_title='Number of '+tournament,legend=dict(title="Players"),title_x=0.5,hovermode="x unified")
    return figRace

@callback(Output('dbt-histomap1','children'),Output('dbt-histomap2','children'),Output('dbt-histomap3','children'),Input('dbt-Ddmap','value'),Input('dbt-histoStats','value'))
def maphisto_update(mapStat,histoStat): 
    '''
    Updates the maps and histograms depending on eaches stat

            Parameters:
                    mapStat (str): the stat for the maps
                    histoStat (str) : the stat for the histograms

            Returns:
                    histomap1,histomap2,histomap3  : the 3 histograms and maps
    '''
    histomaps = [html.Br()]
    histoList = histograms_list(histoStat)
    mapList =maps_list(mapStat)  
    histomap1 = dbc.Col(mapList[0]),dbc.Col(histoList[0])
    histomap2 = dbc.Col(mapList[1]),dbc.Col(histoList[1])
    histomap3 = dbc.Col(mapList[2]),dbc.Col(histoList[2])
    return histomap1,histomap2,histomap3