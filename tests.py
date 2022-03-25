import requests
from PIL import Image

r = requests.get("https://card.godsunchained.com/?id=71&q=4", stream=True)
i = Image.open(r.raw)
# i.thumbnail(400, 400)

print(r.raw)
print("done")
