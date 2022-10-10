"""

create and update/append players info/list


open website
opt: ensure is loaded
g


"""

import os
import json
import warnings
import requests
import threading
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
user_agent = "user-agent=[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36]"


class Player:
    def __init__(self, name, url, rarity, quality):
        self.name = name
        self.url = url
        self.rarity = rarity
        self.quality = quality
        self.market_price = None

    def set_market_price(self, market_price): self.market_price = market_price


class PriceGatherer:
    def __init__(self, url):
        """
        example:
            market_price = PriceGatherer(url).get_market_price()
            print(f'{market_price = }')
        :param url:
        """
        #self.url = url
        self.url = 'https://www.futbin.com/23/player/26325/piero-hincapie'
        options = Options()
        options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(user_agent)
        self.driver = webdriver.Chrome(options=options, executable_path=r'chromedriver\chromedriver.exe')

    def get_market_price(self):
        self.driver.get(self.url)
        market_price_end_string = ' <img alt="c"'
        found = False
        for i in range(10):
            if market_price_end_string in self.driver.page_source:
                found = True
                print(f'took {i} iterations to load market price')
                break
            else:
                sleep(1)
        # print(f'{found = }')
        # agent = self.driver.execute_script("return navigator.userAgent")
        # print(agent)
        html = self.driver.page_source
        # print(html)
        html_market_price_dict = {'id': 'pc-lowest-1'}
        html_market_price = str(BeautifulSoup(html, 'html.parser').find('span', html_market_price_dict))
        market_price_start = html_market_price.index('id="pc-lowest-1">') + len('id="pc-lowest-1">')
        market_price_end = html_market_price.index(market_price_end_string)
        market_price = html_market_price[market_price_start:market_price_end]
        print(rf'Players Futbin Price = {market_price}')
        return market_price


def get_player_data(page):
    html_players, html_urls = _get_data(page)
    player_data = []
    for html_player, html_url in zip(html_players, html_urls):
        html_player, html_url = str(html_player), str(html_url)
        player_info = html_player[html_player.index('img alt="'):html_player.index('" data-original="')]
        # print(f'{player_info = }')
        name_and_rating = player_info[player_info.index('img alt="') + len('img alt="'):player_info.index('" class')]
        for i in range(2):
            if name_and_rating[-1].isdigit():
                name_and_rating = name_and_rating[:-1]
        name = name_and_rating
        player_info2 = player_info.split(' ')[-2:]
        quality = player_info2[0]
        rarity = player_info2[1]
        url = r'https://www.futbin.com' + html_url[html_url.index('href="') + len('href="'):html_url.index('">')]
        # print(f'{player.__dict__ = }')
        player_data.append(Player(name, url, rarity, quality))
    yield player_data


def _get_data(page):
    url = rf'https://www.futbin.com/players?page={page}'
    url += rf'&order=asc&pc_price=800-10000&player_rating=78-99&pos_type=all&sort=pc_price&version=all_nif'
    r = requests.get(url, headers=headers)
    html_players_dict = {'class': 'player_img'}
    html_players = list(BeautifulSoup(r.content, 'html.parser').find_all('img', html_players_dict))
    html_urls_dict = {'class': 'player_name_players_table get-tp'}
    html_urls = list(BeautifulSoup(r.content, 'html.parser').find_all('a', html_urls_dict))
    return html_players, html_urls





if __name__ == '__main__':
    os.chdir('..')
    # PriceGatherer('https://www.futbin.com/23/player/26325/piero-hincapie').get_market_price()
    # get_player_data()
    # for info in get_player_data():
    #     print(info)

