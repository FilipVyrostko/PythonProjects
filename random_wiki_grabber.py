import time
import requests
from random_word import RandomWords
from bs4 import BeautifulSoup

HOST = "https://wikipedia.org"
PORT = 80


def wait():
    time.sleep(1)


def generate_link(rwg):
    print("\n\tGenerating article...\n")
    random_word = rwg.get_random_word()

    req = requests.get(url=HOST + "/wiki/" + random_word)

    # If random word does not have a link, try new
    while not req.ok:
        random_word = rwg.get_random_word()
        req = requests.get(url=HOST + "/wiki/" + random_word)

    return req, random_word


def main():
    print("Welcome to RandomWikiGrabber!"
          "\nThis tool is used to randomly search and return a Wikipedia article.\n")
    wait()

    # Generate random word
    rwg = RandomWords()

    req, random_word = generate_link(rwg)

    while input(f"Are you happy with article about '{random_word}' [y/n]? ") != "y":
        req, random_word = generate_link(rwg)

    content_div = BeautifulSoup(req.content, features="lxml"). \
        body.find('div', attrs={'id': 'mw-content-text'})

    unwanted_tags = ["img", "table",
                     ("div", {"class": "printfooter"}),
                     ("a", {"class": "external text"}),
                     ("div", {"class": "reflist"}),
                     ]

    for tag in unwanted_tags:

        if isinstance(tag, tuple):
            unwanted = content_div.find(tag[0], attrs=tag[1])
            unwanted.extract()

        else:
            unwanted = content_div.find(tag)
            unwanted.extract()

    print(content_div.text.strip())


if __name__ == "__main__":
    main()
