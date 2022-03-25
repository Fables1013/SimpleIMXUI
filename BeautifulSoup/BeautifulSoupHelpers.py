from bs4 import BeautifulSoup
import requests


def loadWebpage(url):
    return requests.get(url)


def loadSoup(html):
    return BeautifulSoup(html.content, 'html.parser')


def loadSoupFromURL(url):
    return loadSoup(loadWebpage(url))


def printWebpage(url):
    soup = loadSoupFromURL(url)
    print(soup.prettify)


def loadTagsOnWebpage(url, tag):
    soup = loadSoupFromURL(url)
    return soup.find_all(tag)


def fetchClass(url, c):
    soup = loadSoupFromURL(url)
    return soup.find("div", class_=c)


def fetchClassValue(url, c):
    soup = loadSoupFromURL(url)
    return soup.find("div", class_=c).text
