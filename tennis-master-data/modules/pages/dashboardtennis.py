import dash
from dash import dcc,html,dash_table,callback
import dash_bootstrap_components as dbc
import plotly_express as px
from dash.dependencies import Output,Input
import pandas as pd
import json
import modules.world_data as world_data

rankingList = pd.read_csv('data/rankingTable.csv')
goatList = pd.read_csv('data/goatTable.csv')
AcesDFs = pd.read_csv('data/Stats/AcesDFs.csv',sep='|')
ServeSpeed = pd.read_csv('data/Stats/ServeSpeed.csv',sep='|')
Serve = pd.read_csv('data/Stats/Serve.csv',sep='|')
SetsMatches = pd.read_csv('data/Stats/SetsMatches.csv',sep='|')
Games = pd.read_csv('data/Stats/Games.csv',sep='|')
OpponentTime = pd.read_csv('data/Stats/OpponentTime.csv',sep='|')
Points = pd.read_csv('data/Stats/Points.csv',sep='|')
Return = pd.read_csv('data/Stats/Return.csv',sep='|')

histoStats=['Ace %','Aces per Match','Aces per Set','Double Fault %','DFs per Match','DFs per Set','Ace Against %','Double Fault Against %',
            'Games Won %','Games per Set','Games per Match','Tie-Breaks Won %','Tie-Breaks per Match','Tie-Breaks per Set %',
            'Match Time','Set Time (minutes)','Game Time (minutes)','Point Time (seconds)',
            'Total Points Won %','Total Break Points Won %','Net Points Won %','Unforced Error %','Forced Error %','Points per Game','Points per Set','Points per Match',
            'Return Points Won %','1st Srv. Return Won %','2nd Srv. Return Won %','Pts. Won per Rtn. Game','Rtn. In-play Pts. Won %',
            '1st Serve Won %','2nd Serve Won %','Service Points Won %','Points per Service Game','Break Points Saved %','Service Games Won %','Svc. In-play Pts. Won %',
            'Serve Max Speed','1st Serve Average Speed','2nd Serve Average Speed',
            'Sets Won %','Sets per Match','Matches Won %']
histoStatsTitles = ['Aces & Double Faults','Games','Time','Points','Return','Serve','Serve Speed','Sets & Matches']

with open('data/tennis-data.json','r') as f:
    players =json.load(f)
 
def find_data(statTitle): 
    '''
    Returns the data and the list of stats that we want to study in function of the stat title.

            Parameters:
                    statTitle (str): the stat title to find data

            Returns:
                    (list): list of the stats that we want to study
                    (pd.DataFrame) : data for these stats
    ''' 
    if statTitle == histoStatsTitles[0] :
        return histoStats[0:8],AcesDFs
    elif statTitle == histoStatsTitles[1]:
        return histoStats[8:14],Games
    elif statTitle == histoStatsTitles[2] :
        return histoStats[14:18],OpponentTime
    elif statTitle == histoStatsTitles[3]:
        return histoStats[18:26],Points
    elif statTitle == histoStatsTitles[4]:
        return histoStats[26:31],Return
    elif statTitle==histoStatsTitles[5]:
        return histoStats[31:38],Serve
    elif statTitle == histoStatsTitles[6]:
        return histoStats[38:41],ServeSpeed
    elif statTitle == histoStatsTitles[7]:
        return histoStats[41:44],SetsMatches
    return [],None
                
def fusion_data(data1,data2):
    '''
    Returns the fusion of two dataFrames.

            Parameters:
                    data1 (pd.DataFrame): first data
                    data2 (pd.DataFrame): second data

            Returns:
                     pd.DataFrame(data)(pd.DataFrame): The fusion of the two datas
    '''
    data = {'name':[name for name in data1['name']]}
    for stat in list(data1.columns)+list(data2.columns):
        data[stat]=[]
    for name in data2['name']:
        if name not in data['name']:
            data['name'].append(name)
    for name in data['name']:
        if name in list(data1['name']):
            dataValue = data1[data1['name']==name]
            for column in data1.columns[1:]:
                data[column].append(list(dataValue[column])[0])
        else :
            for column in data1.columns[1:]:
                data[column].append(None)
        if name in list(data2['name']):
            dataValue = data2[data2['name']==name]
            for column in data2.columns[1:]:
                data[column].append(list(dataValue[column])[0])
        else :
            for column in data2.columns[1:]:
                data[column].append(None)
    return pd.DataFrame(data)
  

    
                
    
    
def list_without_element(list,element):
    '''
    Returns a list without one element.

            Parameters:
                    list (list): The list
                    element (str): The element that we don't want on the list

            Returns:
                    list1 (list): The list without the element
    '''
    list1 = list.copy()
    list1.remove(element)
    return list1


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
    filtre = int(length/33) #3%
    return [list[filtre],list[length-filtre]]
    

    
world_ranking = world_data.world_data1('RANKING')
world_goat = world_data.world_data1('GOAT')

histo = px.histogram(AcesDFs,x='Ace %',range_x=[-5,30],nbins=300)
histo2 = px.histogram(AcesDFs,x='Ace Against %',range_x=[-5,30],nbins=300)
fig2 = dcc.Graph(figure=histo2,id='figure2')
map = px.choropleth(world_ranking, locations="iso_a3",color="Total Players",color_continuous_scale=px.colors.sequential.Plasma)



dash.register_page(
    __name__,
    path='/',
    title='Tennis Players Data',
    name='Tennis Players Data'
)
layout = dbc.Container(children=[
    html.H3('TENNIS PLAYERS DATA',style={"font-size": "80px",'textAlign':'center'}),html.Br(),html.Br(),
    html.H3('Table (mode Ranking or Goat)',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),
    html.Br(),
    html.Br(),
    dcc.Dropdown(
            id="mode-dropdown",
            options=[
            {'label': 'Ranking Table', 'value': 'Ranking Table'},
            {'label': 'Goat Table', 'value': 'Goat Table'}
                ],
            value='Ranking Table',optionHeight=30,
            style={'width': '100%','textAlign':'center','font-size':25}
            ),html.Br(),html.Br(),
    dbc.Row(
        [dbc.Col([
            html.H1('Players Table (Mode Ranking)',id='dap-tableTitle',style={'textAlign':'center'}),
            html.Br(),
            html.Br(),
            html.Div(children=[dash_table.DataTable(id='tbl',active_cell=None),html.Center(dcc.Checklist(id='checklist',value=[]))],id='mode')
        ],align=True,
            width={'size':5, 'offset':0, 'order':1},
        ),
        dbc.Col([html.Br(),html.Center(html.H1(id='playerSelected')),html.Br(),html.Br(),html.Br(),html.Div(id='tbl_out',children=[])],
            width={'size':5, 'offset':1, 'order':2},
        )],
        justify='center'
    ),
    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Histogram',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            dcc.Dropdown(id="dap-DdHisto1",options=histoStatsTitles,value=histoStatsTitles[0]),
            dcc.Dropdown(id="dap-DdHisto2",options=[],value=None),
            dcc.Graph(id='dap-figHisto'),
        ]),
        dbc.Col([
            dcc.Store(data=AcesDFs.to_dict(),id='dap-dataFusion'),
            html.H3('Graphic (y=histo stat)',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
            dcc.Dropdown(id="dap-DdGraph1",options=histoStatsTitles,value=histoStatsTitles[0]),
            dcc.Dropdown(id="dap-DdGraph2",options=[]),
            dcc.Graph(id='dap-figGraph')
        ])
    ]),html.Br(),html.Br(),html.Br(),
    html.H3('Players Map',style={"font-size": "50px", "text-decoration": "underline",'textAlign':'center'}),html.Br(),html.Br(),
    dbc.Row([
        dbc.Col([
        html.Br(),
                        dcc.Dropdown(
            id="graph-dropdown3",
            options=[
            {'label': 'RANKING', 'value': 'RANKING'},
            {'label': 'GOAT', 'value': 'GOAT'}
            ],
            value='RANKING'
            ),
        ]),
        dbc.Col([
        html.Br(),
                        dcc.Dropdown(
            id="graph-dropdown4",
            options=[
            {'label': 'Total Players', 'value': 'Total Players'},
            ],
            value='Total Players'
            ),
        ])
    ]),
    html.Br(),html.Br(),
    dbc.Row([
        html.Center(dcc.Graph(figure = map,id='map'))
    ])
], fluid=True) 
    
@callback(Output('mode','children'),Output('dap-tableTitle','children'),Input('mode-dropdown','value'))

def update_mode(value) :
    print(value)
    if  value == 'Goat Table':
        elements_checkList = ['Age','Country','Win Rate','Titles','GS','Retired']
        tableData = goatList  
        tableTitle = 'Players Table (mode GOAT)'
    else :
        elements_checkList=['Age','Country','Win Rate','Titles','GS']
        tableData = rankingList
        tableTitle = 'Players Table (mode Ranking)'
    
    table = dash_table.DataTable(tableData.to_dict('records'),page_size=20,id='tbl',page_current=0,style_header={
        'border': '1px solid pink',
        'textAlign': 'center'},
    style_cell={
        'textAlign': 'center'
    })
    checklist = dcc.Checklist(options=[{'label':i,'value':i}for i in elements_checkList],value=[],inline=True,id='checklist')
    return [table,html.Center(checklist)],tableTitle 

@callback(Output('tbl','data'),Input('checklist','value'),Input('mode-dropdown','value'))
def update_table(value,mode):
    columns=['Rank','Name','Points']+value 
    if mode == 'Goat Table':
        tableData=goatList[columns]
    else :
        tableData=rankingList[columns]

    return tableData.to_dict('records')

@callback(Output('tbl_out', 'children'),Output('playerSelected','children'), Input('tbl', 'active_cell'),Input('tbl','page_current'),Input('mode-dropdown','value'))
def update_graphs(active_cell,page_current,mode):
    if active_cell :
        if active_cell['column']==1:

            if mode == 'Goat Table':
                name = goatList['Name'][active_cell['row']+20*page_current]
            else :
                name = rankingList['Name'][active_cell['row']+20*page_current]
            data = players[name]['profile']
            table = dash_table.DataTable(pd.DataFrame({'Info':data.keys(),'Value':data.values()}).to_dict('records'),
                style_header={'display': 'none'},
                style_cell={'textAlign': 'center'},style_as_list_view=True,cell_selectable=False,page_size=20)
            return table,name   
    return [html.Br(),html.Br(),html.Br(),html.Center(html.Img(src=dash.get_asset_url('noPlayerSelected.jpg')))],'Click on a player name in the Table'

@callback(Output('dap-DdHisto2','options'),Output('dap-DdHisto2','value'),Input('dap-DdHisto1','value'))
def update_histo1(value):
    data = find_data(value)
    return data[0],data[0][0]

@callback(Output('dap-figHisto','figure'),Input('dap-DdHisto1','value'),Input('dap-DdHisto2','value'))
def update_histo2(value1,value):
    graphData = pd.DataFrame(find_data(value1)[1].to_dict())
    filtre = filtre_data(graphData[value])
    graphData= graphData[(graphData[value]<=filtre[1]) & (graphData[value]>=filtre[0])]
    alpha=int((max(graphData[value])-min(graphData[value]))/10)
    histo = px.histogram(graphData,x=value,range_x=[min(graphData[value])-alpha,max(graphData[value])+alpha],title='Histogram of \''+value+"\' for all players")
    histo.update_layout(title_x=0.5,height=700)
    return histo

@callback(Output('dap-dataFusion','data'),Output('dap-DdGraph2','options'),Output('dap-DdGraph2','value'),Input('dap-DdGraph1','value'),Input('dap-DdHisto1','value'),Input('dap-DdHisto2','value'))
def update_graph1(valueG,valueH1,valueH2):
    data1 = find_data(valueG)
    if valueG==valueH1:
        listData = list_without_element(data1[0],valueH2)
        return data1[1].to_dict(),listData,listData[0]
    data2 = find_data(valueH1)
    data = fusion_data(data1[1],data2[1])
    return data.to_dict(),data1[0],data1[0][0]

@callback(Output('dap-figGraph','figure'),Input('dap-DdGraph2','value'),Input('dap-DdHisto2','value'),Input('dap-dataFusion','data'))
def update_graph2(valueG2,valueH2,data):
    graphData = pd.DataFrame(data)
    filtre = filtre_data(graphData[valueH2])
    filtre1 = filtre_data(graphData[valueG2])

    graphData = graphData.sort_values(by=valueH2)
    graph = px.scatter(graphData,x=valueH2,y=valueG2,range_x=filtre,range_y=filtre1,title='\''+valueG2+'\' in function of \''+valueH2+'\' for all players')
    graph.update_layout(title_x=0.5,height=700)
    return graph
        
        
    
@callback(Output("graph-dropdown4",'options'),Output("graph-dropdown4",'value'),Input("graph-dropdown3",'value'))

def update_mode_map(mode_map):
    if mode_map == 'RANKING':
        map_options = [{'label':i,'value':i} for i in world_data.ranking_stats]
    else :
        map_options = [{'label':i,'value':i} for i in world_data.goat_stats]
    return map_options,'Total Players'

@callback(Output("map","figure"),Input("graph-dropdown4",'value'),Input("graph-dropdown3",'value'))      
def update_map(stat,mode):
    hovertemplate = ['Country : %{customdata[1]}']
    if 'Top' not in stat:
        hovertemplate.append('Players : %{customdata[0]}')
        if 'Ratio' in stat :
            nb = stat+'_Nb'
            hovertemplate.append(stat+' : %{customdata[2]:.2f} %')
            hovertemplate.append('Matches played per player : %{customdata[3]:.2f}')
            hovertemplate.append('Total matches played : %{customdata[4]:.0f}')
        elif stat in ['Height','Age'] or 'per player' in stat :
            nb = stat+'_Nb'
            hovertemplate.append(stat+' : %{customdata[2]:.2f}')
        else :
            nb = 'Total Players'
            if stat != 'Total Players':
                hovertemplate.append(stat+' : %{customdata[2]:.0f}')
    else:
        if 'Top' in stat :
            nb = stat
            hovertemplate.append('Players in '+stat+' : %{customdata[2]}')
        
    if mode == "RANKING" :
        data = world_ranking       
    else :
        data = world_goat
    hover_data = ['name','Total Players']
    if stat in ['Height'] or 'Ratio' in stat :
        hover_data.append(stat+'_Nb')
    map = px.choropleth(data, locations="iso_a3",color=stat,color_continuous_scale=px.colors.sequential.Plasma,title='\''+stat+'\' per country for '+mode+' players')
    map.update_layout(margin=dict(l=0, r=0, t=50, b=0),width=1900,height=1200,title_x=0.5,title_font_size=30)
    map.update_traces(customdata=data[[nb,'name',stat,'Matches per player','Total Matches']],
    hovertemplate="<br>".join(hovertemplate))
    return map




