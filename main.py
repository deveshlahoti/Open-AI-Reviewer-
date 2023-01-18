import openai
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from newspaper import Article

openai.api_key = "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"


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
URL = "https://www.amazon.com/Apple-Watch-Smart-Silver-Aluminum/dp/B0BDHTRVPP/ref=sr_1_3?crid=2DZ8OP5V4U7HC&keywords=apple+watch&qid=1673644935&sprefix=dildo%2Caps%2C3562&sr=8-3"

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "lxml")
title = soup.find("span", attrs={"id":'productTitle'})
title = title.string

print(title)

query = "review of " + title
links = []
for i in search(query, tld="com", num=5, stop=5, pause=2):
    links.append(i)

print(links)


final = []
for n in range(3):
    url = links[n]
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    c = 14000
    res = [text[i:i + c] for i in range(0, len(text), c)]
    for a in res:
        prompt = "write a summary about the product described in the following article: " + a
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)
        response = response["choices"][0]["text"]
        final.append(response)


s_responses = "".join(final)
prompt = "write a pros and cons list of the product described in the following: " + s_responses
final_response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
listed = final_response["choices"][0]["text"]
print(listed)
