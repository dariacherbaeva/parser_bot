import re
import time

from bs4 import BeautifulSoup
from selenium.common import TimeoutException


def parse_page(link, driver, delay):
    driver.get(link)
    try:
        time.sleep(2)
        button = driver.find_element('xpath', "//*[contains(text(), 'older miners')]")
        button.click()
        time.sleep(delay)
    except TimeoutException:
        print('Loading took too much time!')
    html = driver.page_source
    driver.quit()
    return html


def find_miners(html):
    soup = BeautifulSoup(html)

    lines = soup.find_all("tr", {"class": "table-pin"})
    lines += soup.find_all("tr", {"role": "row"})
    return lines


def get_miner_info(line):
    children = line.findChildren()[0].findChildren("a")
    if children:
        link = re.search("(?P<url>https?://[^\s]+)", str(line))
        if link:
            link = link.group("url")
            miner_dict = dict()
            miner_dict['Mining group'] = str(line.find("td", {"aria-colindex": "2"}).text.strip())
            miner_dict['Token'] = str(line.find("td", {"aria-colindex": "4"}).text.strip())
            miner_dict['Fees'] = str(line.find("td", {"aria-colindex": "6"}).text.strip())
            miner_dict['Age'] = str(line.find("td", {"aria-colindex": "7"}).text.strip())
            miner_dict['Daily'] = str(line.find("td", {"aria-colindex": "8"}).text.strip())
            miner_dict['TVL'] = str(line.find("td", {"aria-colindex": "9"}).text.strip())
            miner_dict['Evol TVL'] = str(line.find("td", {"aria-colindex": "10"}).text.strip())

            return link, miner_dict
