# PyTorch Forum Scraper

This Python script is designed to scrape data from the PyTorch discussion forum (https://discuss.pytorch.org). It navigates through the forum, collects information about various posts, and saves the data in a CSV file. The script is built using `asyncio` and `playwright`, which allows for asynchronous web scraping.

## Features

- Navigates to the PyTorch discussion forum's latest posts page.
- Collects data from each post, including the title, URL, category, tags, timestamp, username, and post text.
- Saves the collected data into a CSV file with a timestamp in its filename.
- Handles pagination by scrolling through the page.
- Uses asynchronous programming for efficient data scraping.

## Requirements

To run this script, you need to have Python installed along with the following packages:

- `asyncio`
- `playwright`
- `pandas`

You can install these packages using pip:

```bash
pip install playwright pandas

Additionally, you need to install the Playwright browser binaries:
```bash
playwright install

## Usage

To run the script, simply execute it with Python:

```bash
python path_to_script.py


## Output

The script outputs a CSV file named `posts_info_YYYYMMDD_HHMMSS.csv`, where `YYYYMMDD_HHMMSS` is the current timestamp. The CSV file contains the following columns:

- `post_title`: The title of the post.
- `post_URL`: The URL of the post.
- `category_name`: The category of the post.
- `tags`: The tags associated with the post.
- `timestamp`: The timestamp of the post.
- `username`: The username of the post's author.
- `post_text`: The text content of the post.

## Important Notes

- The script is designed to scrape data from a public forum. Always ensure you comply with the website's terms of service and use web scraping responsibly.
- The performance and efficiency of the script can vary based on network conditions and the structure of the website.
- The script may require updates if there are changes to the website's layout or elements.

## Disclaimer

This script is provided for educational purposes only. The author is not responsible for any potential misuse or issues arising from its use.

## License

This project is open-sourced and available under the MIT License.

