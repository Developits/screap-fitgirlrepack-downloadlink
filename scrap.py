import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class FitGirlScraper:
    """A compact scraper for FitGirl Repacks download links"""
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.link_pattern = re.compile(r'window\.open\(["\']([^"\']+)')
        self.output_file = 'download_links.txt'

    def fetch(self, url):
        try:
            return requests.get(url, headers=self.headers, timeout=10).text
        except Exception:
            return None

    def is_valid(self, url):
        try:
            return all([p for p in urlparse(url)[:2]])
        except ValueError:
            return False

    def extract_game_links(self, url):
        content = self.fetch(url)
        if not content:
            return []
        soup = BeautifulSoup(content, 'html.parser')
        spoiler_divs = soup.select('div.su-spoiler-content')
        if len(spoiler_divs) < 2:
            return []
        return [a['href'].split('#')[0] for a in spoiler_divs[1].select('a[href*="fuckingfast.co"]') if self.is_valid(a['href'])]

    def extract_download_url(self, url):
        content = self.fetch(url)
        if not content:
            return None
        for script in BeautifulSoup(content, 'html.parser').select('script'):
            if 'window.open' in script.text and 'fuckingfast.co/dl/' in script.text:
                match = self.link_pattern.search(script.text)
                if match and self.is_valid(match.group(1)):
                    return match.group(1)
        return None

    def run(self, game_url):
        with open(self.output_file, 'w') as f:
            f.write('')  # Clear existing file
        for redirect_url in self.extract_game_links(game_url):
            download_url = self.extract_download_url(redirect_url)
            if download_url:
                with open(self.output_file, 'a') as f:
                    f.write(f'{download_url}\n')

if __name__ == "__main__":
    FitGirlScraper().run(input("Enter the URL of the game page: "))
    print("Scraping complete. Links saved to download_links.txt")    