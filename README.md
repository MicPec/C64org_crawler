# C64G.com Game Scraper

This Python script scrapes game files from the C64G.com website, downloading and organizing them into a local directory structure.

## Features

- Scrapes game listings from C64G.com
- Downloads game files for each listed game
- Organizes downloaded files into subdirectories by game title
- Handles network errors and file saving exceptions

## Requirements

- Python 3.11+
- BeautifulSoup4
- Requests

## Installation

1. Clone this repository
2. Install required packages:
   ```
   uv sync
   ```

## Usage

Run the script using `uv` and Python:

```
uv run c64gcom_scrapper.py
```

Downloaded games will be saved in the `games` subdirectory.

## Disclaimer

This script is for educational purposes only. Ensure you have permission to download content from C64G.com before using this script.

## License

[MIT License](https://opensource.org/licenses/MIT)
