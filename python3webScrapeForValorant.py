import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import re

def download_webpage(url, filename):
    response = requests.get(url)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

def parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        rank_div = soup.find('div', class_='valorant-rank-bg')

        score_text_div = soup.find('div', class_='score__text')

        if rank_div is not None:
            valorant_rank = rank_div.text.strip()
        else:
            valorant_rank = "UNKNOWN"

        if score_text_div is not None:
            score_text = score_text_div.text.strip()
            score_numeric = re.search(r'\d+', score_text).group()
        else:
            score_text = "UNKNOWN"
            score_numeric = "UNKNOWN"

        return valorant_rank, score_numeric

user_info_list = []

filenames_list = []

while True:
    username = input("Type username (or type 'ENTER' to finish): ")


    if username.upper() == 'ENTER':
        break


    url = f"https://tracker.gg/valorant/profile/riot/{urllib.parse.quote(username)}/overview"


    filename = urllib.parse.quote(username, safe='') + ".html"


    download_webpage(url, filename)


    user_info_list.append((username, filename))
    filenames_list.append(filename)

for (username, filename) in user_info_list:

    valorant_rank, score_numeric = parse_file(filename)


    print(f"Username: {username}")
    print(f"Rank: {valorant_rank}")
    print(f"Tracker score: {score_numeric}")
    print()


    os.remove(filename)
