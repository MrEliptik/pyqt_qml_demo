import requests

topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
newstories_url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
beststories_url = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"
askstories_url = "https://hacker-news.firebaseio.com/v0/askstories.json?print=pretty"
showstories_url = "https://hacker-news.firebaseio.com/v0/showstories.json?print=pretty"
jobstories_url = "https://hacker-news.firebaseio.com/v0/jobstories.json?print=pretty"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"

def get_top_stories_ids():
    r = requests.get(topstories_url)
    data = r.json()
    return data

def get_story_from_id(id):
    url = item_url.format(id)
    r = requests.get(url)
    return r.json()

def get_top_stories():
    data = []
    stories_id = get_top_stories_ids()
    for _id in stories_id:
        data.append(get_story_from_id(_id))

    return data


if __name__ == "__main__":
    data = get_top_stories_ids()
    print("{} stories".format(len(data)))

    for (i, id) in enumerate(data):
        url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(id)
        r = requests.get(url)
        data = r.json()
        print("Title: {} - by: {} - score: {} - URL: {}".format(data['title'], data['by'], data['score'], data['url']))