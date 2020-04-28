from linkpreview import link_preview
from webpreview import web_preview
from hackernews import get_top_stories, get_story_from_id


data = get_top_stories()

for (i, id) in enumerate(data):

    print('\n')
    print('########################################"')
    
    if i == 5: break

    story = get_story_from_id(id)
    print("Title: {} - by: {} - score: {} - URL: {}".format(story['title'], story['by'], story['score'], story['url']))

    preview = link_preview(story['url'])
    print("title: {} - description: {} - image: {}".format(preview.title, preview.description, preview.image))

    title, description, image = web_preview(story['url'], parser='lxml')
    print("title: {} - description: {} - image: {}".format(title, description, image))


