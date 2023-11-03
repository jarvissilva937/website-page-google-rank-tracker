import requests
import pandas as pd
from googleapiclient.discovery import build

api_key = ""
cse_id = ""

titles = []
urls = []
positions = []

def get_posts(page,per_page):
    url = f'https://domain.com/wp-json/wp/v2/posts?page={page}&per_page={per_page}'
    response = requests.get(url)
    return response.json()

def search_google(post_title,post_url,country):
    found = False
    position = 0
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=post_title, cx=cse_id, gl=country).execute()

    for item in res['items']:
        if item['link'] == post_url:
            found = True
            break
        else:
            position = position + 1

    titles.append(post_title)
    urls.append(post_url)

    if found:
        positions.append(position)
    else:
        positions.append(-1)

if __name__ == "__main__":
    posts = get_posts(2,98)
    for post in posts:
        search_google(post['title']['rendered'],post['link'],'in')
    df = pd.DataFrame({'Title': titles, 'Url': urls, 'Position': positions})
    df.to_excel('rankings.xlsx', index=False)
    print("Done")
