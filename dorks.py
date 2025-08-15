from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os

# Scrap exploitdb puis retourne les données : dork, description, date
def scrapper_exploitdb(nb):
    URL = "https://www.exploit-db.com/ghdb/"+str(nb)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try :
        page = requests.get(URL, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(e)

    time.sleep(10)
    soup = BeautifulSoup(page.content, "html.parser")

    # Récupère le dork 
    try:
        dork = soup.find("h1", class_="card-title text-secondary text-center").get_text()
    except:
        dork = "Pas de dork"

    # Récupère la description du dork
    try:
        description = soup.find("code", class_="language-text").get_text()    
    except:
        description = "Pas de description"

    # Récupère la date du dork 
    try:
        date = soup.find("div", class_="stats text-center").get_text().replace('Published: ','')
    except:
        date = "Pas de date"

    return dork,description,date


if __name__ == '__main__':

    # Scrap "exploitDb" pour récuperer les dorks avec scrapper_exploitdb 

    min = 1000 # Valeur à laquelle le scraping commence
    max = 7000 # Valeur à laquelle le scraping fini

    #Création du tableur avec les dorks

    tableur_name = 'Data_scraping.xlsx'


    if(os.path.exists(tableur_name)):
        df = pd.read_excel(tableur_name)
        min = df['Dork'].count()
    else:
        df = pd.DataFrame(columns= ['Dork','Description','date'])

    for i in range(min, max):
        
        dork, description, date = scrapper_exploitdb(i)
    
        # Creer une nouvelle ligne avec les données récupérées
        new_ligne = pd.DataFrame([{
            'Dork': dork.strip(),
            'Description': description,
            'date': date
        }])
    
        df = pd.concat([df, new_ligne], ignore_index=True)
    
        # Print les valeur pour chaque dork
        print(dork)


    df.to_excel(tableur_name,index=False)
    




