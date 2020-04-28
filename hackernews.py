import requests

url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"


def get_top_stories():
    r = requests.get(url)
    data = r.json()
    return data

def get_story_from_id(id):
    url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(id)
    r = requests.get(url)
    return r.json()


if __name__ == "__main__":
    data = get_top_stories()
    print("{} stories".format(len(data)))

    for (i, id) in enumerate(data):
        url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(id)
        r = requests.get(url)
        data = r.json()
        print("Title: {} - by: {} - score: {} - URL: {}".format(data['title'], data['by'], data['score'], data['url']))