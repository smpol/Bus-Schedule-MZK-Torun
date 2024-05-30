import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_table_data(number_of_stop):

    url = f'http://sip.um.torun.pl:8080/panels/0/default.aspx?stop={number_of_stop}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'tablePanel'})
        
        if table:
            table_data = []
            rows = table.find_all('tr')
            #Skips first row (headers) and empty rows
            for row in rows[1:]:
                cells = row.find_all(['td'])
                row_data = [cell.text.strip() for cell in cells]
                
                # Check if row contains data
                if any(row_data):
                    forrmatted_row_data = {
                        'line': row_data[0],
                        'destination': row_data[1],
                        'time': row_data[2]
                    }
                    table_data.append(forrmatted_row_data)
            
            datenow ={
                'line': 'Ostatnia aktualizacja:',
                'destination': '',
                'time': datetime.now().strftime("%H:%M:%S")
            }
            table_data.append(datenow)

            return table_data
        else:
            print("Nie znaleziono tabeli na stronie.")
    else:
        print(f"Błąd pobierania strony. Kod statusu: {response.status_code}")