from collections import namedtuple
from datetime import datetime
import requests

POSTS = dict()

Post = namedtuple('Post', ['link', 'title', 'date'])

LAST_PAGE = 5

url = 'https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs'

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'content-type': 'application/json',
    'origin': 'https://analogdevices.wd1.myworkdayjobs.com',
    'priority': 'u=1, i',
    'referer': 'https://analogdevices.wd1.myworkdayjobs.com/en-US/External/?locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

json_data = {"appliedFacets":{"locationCountry":["bc33aa3152ec42d4995f4791a106ed09"]},"limit":20,"offset":0,"searchText":""}

for page in range(LAST_PAGE):
    json_data["offset"] = 20 * page

    response = requests.post(
        url=url,
        headers=headers,
        json=json_data
    )

    jobs = dict(response.json())['jobPostings']

    for job in jobs:
        title = job['title']
        link = "https://analogdevices.wd1.myworkdayjobs.com/en-US/External"+job['externalPath']
        if not (link in POSTS.keys()):
            POSTS[link] = Post(link, title, -1 * len(POSTS))


STREAM = sorted([POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True)

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join([ r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Analog Devices Careers</title>""",
            r"""<description>Analog Devices Careers</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</pubDate>""",
            r"""<lastBuildDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</lastBuildDate>""",
            "\n".join([r"""<item><title><![CDATA["""+x.title+r"""]]></title><link>"""+x.link+r"""</link></item>""" for x in STREAM]),
            r"""</channel>""",
            r"""</rss>""",
    ])

    print(XML)
