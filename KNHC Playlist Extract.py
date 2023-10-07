import requests
from bs4 import BeautifulSoup

urls = [
    'https://onlineradiobox.com/us/knhc/playlist/?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/1?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/2?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/3?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/4?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/5?cs=us.knhc',
    'https://onlineradiobox.com/us/knhc/playlist/6?cs=us.knhc'
]

playlist_rows = []

for index, url in enumerate(urls):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.find_all('tr')

    for i, row in enumerate(rows):
        text = row.get_text(strip=True)
        if ' - ' in text:
            if index == 0 and text.startswith('Live'):
                playlist_rows.append(text[4:])  # Trim off 4 characters for the first result starting with "Live"
            else:
                playlist_rows.append(text[5:])  # Trim off 5 characters for other results

duplicate_count = 0

with open('KNHC_playlist.txt', 'a+') as file:
    file.seek(0)  # Move the file pointer to the beginning
    existing_rows = file.read().splitlines()

    for row in playlist_rows:
        if row not in existing_rows:
            file.write(row + '\n')
        else:
            duplicate_count += 1

        existing_rows.append(row)  # Add row to existing rows to avoid duplicates within current session

print(f"KNHC playlist saved to playlist.txt file. Skipped {duplicate_count} duplicates.")
