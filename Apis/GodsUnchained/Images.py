import io
import requests
from PIL import Image

from Configs.Gui_Configs import defaultImgUrl, cardImgSize
from Model.GodsUnchained.Card import Quality


def swapQualityToNumber(q):
    return {Quality.Meteorite: 4, Quality.Shadow: 3, Quality.Gold: 2, Quality.Diamond: 1}[q]


def getImageFromURL(url, size=(50, 50)):
    r = requests.get(url, stream=True)
    defaultImg = Image.open(r.raw)
    defaultImg = defaultImg.resize(size)
    return defaultImg


def convertImgToBytes(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def fetchCardImageForProto(proto, quality=Quality.Meteorite):
    url = f"https://card.godsunchained.com/?id={proto.id}&q={swapQualityToNumber(quality)}"
    img = getImageFromURL(url, cardImgSize)
    return convertImgToBytes(img)


def loadDefaultImage():
    r = requests.get(defaultImgUrl, stream=True)
    defaultImg = Image.open(r.raw)
    defaultImg = defaultImg.resize(cardImgSize)
    img_byte_arr = io.BytesIO()
    defaultImg.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
