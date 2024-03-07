import requests
from bs4 import BeautifulSoup
import pandas as pd
url = input("Input the link : ")
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        hotel = soup.h1.get_text()
        p = soup.find('span', class_='MW1oTb')
        price = p.text.strip()

        check_in_div = soup.find('input', {'placeholder': 'Check-in'}).parent.parent
        check_out_div = soup.find('input', {'placeholder': 'Check-out'}).parent.parent

        check_in_data_value = check_in_div['data-value']
        check_out_data_value = check_out_div['data-value']

        official_site_link = soup.find('span', string='Official Site')
        if official_site_link:
            div_containing_link = official_site_link.find_parent('div', class_='ADs2Tc')
            data_id = div_containing_link['data-id']
            offcal = True
        else:
            offcal = False
            data_id = None

        data = [[hotel, check_in_data_value, check_out_data_value, price, data_id,offcal]]
        df = pd.DataFrame(data, columns=['Hotel Name', 'Check-in', 'Check-out', 'Price', 'data-id', 'Official site'])
        print(df)
        df.to_csv('Hotel_data.csv', index=False)
    
    except Exception as e:
        print("An error occurred:", e)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
