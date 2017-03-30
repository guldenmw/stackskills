from pprint import pprint
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import simplejson as json

search = input("Search For:")
params = {"q": search, "t": "hd", "iax": 1, "ia": "images"}
r = requests.get("http://www.duckduckgo.com", params=params)
temp = json.load(r.text)
pprint(temp)
# print(r.content)
# print(r.url)

# soup = BeautifulSoup(r.text, "html.parser")
# print(soup.type)
# print(soup.prettify())
# links = soup.findAll("a", {"class": "thumb"})
# print("Links:", links)
#
# for item in links:
#     # print("Item:", item)
#     img_obj = requests.get(item.attrs["href"])
#     print("Getting", item.attrs["href"])
#     title = item.attrs["href"].split("/")[-1]
#     img = Image.open(BytesIO(img_obj.content))
#     img.save("C:/Users/Wilhelm/PycharmProjects/stackskills/webscrapery/scraped_images/" + title, img.format)
