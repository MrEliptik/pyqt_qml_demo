import requests

url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"

r = requests.get(url)

data = r.json()

print("{} stories".format(len(data)))

for (i, id) in enumerate(data):
    url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(id)
    r = requests.get(url)
    data = r.json()
    print("Title: {} - by: {} - score: {} - URL: {}".format(data['title'], data['by'], data['score'], data['url']))