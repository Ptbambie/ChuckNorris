import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "http://www.chucknorrisfacts.fr/facts/recent"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')
    joke_blocks = soup.find_all('div', class_='card')

    if len(joke_blocks) >= 20:
        jokes_and_notes = []  # Crée une liste pour stocker les paires de blagues et de notes
        
        for i, joke_block in enumerate(joke_blocks[:20]):
            joke_text = joke_block.text
            note_pattern = r'(\d/\d)'
            notes = re.findall(note_pattern, joke_text)
            
            if notes:
                jokes_and_notes.append({"Blague": f"Blague {i+1}", "Note": notes[0]})
            else:
                jokes_and_notes.append({"Blague": f"Blague {i+1}", "Note": "Aucune note trouvée"})
        
        # Transformez la liste en un DataFrame
        df = pd.DataFrame(jokes_and_notes)
        
        # Afficher le DataFrame
        print(df)
    else:
        print("Il n'y a pas suffisamment de blagues pour afficher la 20e.")
else:
    print("La requête a échoué avec le code HTTP :", response.status_code)
