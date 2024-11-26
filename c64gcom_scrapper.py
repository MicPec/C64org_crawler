#!/usr/bin/env python3
import os
from typing import Dict, Generator, List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as BS
from bs4.element import Tag

# Configuration constants
BASE_URL = 'https://c64g.com/'
GAMES_SUBDIR = 'games'

# HTTP request headers
HTTP_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'Origin': 'https://c64g.com',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def get_parsed_html(url: str) -> BS:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for bad status codes
    return BS(response.content, 'html.parser')


def find_games(container: Tag) -> Generator[Tuple[str, str], None, None]:
    for link in container.find_all('a'):
        yield link.text, link['href']


def get_form_details(form: Tag) -> Dict:
    details = {
        "action": form.attrs.get("action", "").lower(),
        "method": form.attrs.get("method", "post").lower(),
        "inputs": []
    }

    for input_tag in form.find_all("input"):
        input_details = {
            "type": input_tag.attrs.get("type", "text"),
            "name": input_tag.attrs.get("name"),
            "value": input_tag.attrs.get("value", "")
        }
        details["inputs"].append(input_details)

    return details


def save_file(filepath: str, data: bytes) -> None:
    try:
        with open(filepath, 'wb') as f:
            f.write(data)
        print(f'Successfully saved: {filepath}')
    except IOError as e:
        print(f'Error saving {filepath}: {str(e)}')


def get_form_data(form_details: Dict) -> Dict:
    return {tag["name"]: tag["value"] for tag in form_details['inputs']}


def download_game_file(download_url: str, game_dir: str, button_text: str) -> None:
    download_page = get_parsed_html(download_url)
    form = get_form_details(download_page.find('form'))
    form_data = get_form_data(form)

    post_url = urljoin(download_url, form['action'])
    response = requests.post(post_url, data=form_data, headers=HTTP_HEADERS, timeout=5)
    response.raise_for_status()

    filename = os.path.join(game_dir, button_text)
    if not os.path.exists(filename):
        save_file(filename, response.content)
    else:
        print(f'File already exists: {filename}')


def process_game(game_title: str, game_url: str) -> None:
    game_dir = os.path.join(GAMES_SUBDIR, game_title)
    os.makedirs(game_dir, exist_ok=True)

    game_page = get_parsed_html(urljoin(BASE_URL, game_url))
    download_buttons = game_page.find_all('a', class_='btn btn-primary btn-block')

    for button in download_buttons:
        download_url = urljoin(BASE_URL, button['href'])
        try:
            download_game_file(download_url, game_dir, button.contents[0])
        except requests.RequestException as e:
            print(f"Error downloading {button.contents[0]}: {str(e)}")


def process_games(game_list: Generator[Tuple[str, str], None, None]) -> None:
    for game_title, game_url in game_list:
        try:
            process_game(game_title, game_url)
        except Exception as e:
            print(f"Error processing game {game_title}: {str(e)}")
            continue


def main() -> None:
    try:
        games_page = get_parsed_html(urljoin(BASE_URL, GAMES_SUBDIR))
        games_container = games_page.find('div', class_='container c64border')
        if not games_container:
            raise ValueError("Could not find games container on the page")
            
        game_list = find_games(games_container)
        process_games(game_list)
    except requests.RequestException as e:
        print(f"Network error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
