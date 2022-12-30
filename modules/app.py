from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
import modules.TennisScraping as ts
import json

def create_dashboard(mode_scraping=False,mode_sleep=False):
    #Si on est en mode scraping on va aller scraper toutes nos données
    if mode_scraping :
        players = ts.Players(400,600)
        ts.all_data_scraping(players,mode_sleep)
        with(open('data/tennis-data.json'))as f:
            playersDict = json.load(f)
        for name in ['Roger Federer','Novak Djokovic','Rafael Nadal']:
            ts.matchesData(name,playersDict,mode_sleep)
    else :
        #Sinon on crée juste les csv à partir des datas déjà présentes
        with(open('data/tennis-data.json'))as f:
            playersDict = json.load(f)
        ts.create_goat_table(playersDict)
        ts.create_ranking_table(playersDict)
        ts.create_stats_csv(playersDict)
    
    app = dash.Dash(__name__,use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

    app.layout = html.Div([
        html.H1('Tennis Data Master'),
        html.H3('Change page by clicking on a link below',style={"font-size": "20px"}),

        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"],style={"font-size": "25px"}
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),

        dash.page_container
    ])

    app.run_server(debug=False)
    
