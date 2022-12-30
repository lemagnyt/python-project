import modules.app as app
import modules.TennisScraping as ts
import modules.world_data as world_data

test = False
mode_scraping = False
if __name__ == '__main__':
    if not test : 
        if mode_scraping :
            app.create_dashboard(mode_scraping=True) 
        else :
            app.create_dashboard(mode_scraping=False)
    else : 
    #Exemple de test des fonction de scraping
        players = ts.Players(20,20)
        ts.all_data_scraping(players,False,test=True)
        ts.matchesData(players.List[0].Name,players.JSONDict,False,nbMatches=15,test=True)