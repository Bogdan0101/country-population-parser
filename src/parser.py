import httpx
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self, url: str, headers: dict) -> None:
        self.url = url
        self.headers = headers

    @abstractmethod
    def parse(self, html: str):
        pass

    async def scrap(self) -> list[dict]:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
            response = await client.get(self.url, headers=self.headers)
            print(response)
            return self.parse(html=response.text)


class WikipediaParser(BaseParser):
    def __init__(self):
        super().__init__(
            url="https://en.wikipedia.org/w/index.php"
            "?title=List_of_countries_by_population_(United_Nations)"
            "&oldid=1215058959",
            headers={
                "User-Agent": "CountryPopulationParser/1.0 (kononovb71@gmail.com)"
            },
        )

    def parse(self, html: str) -> list[dict]:
        data = []
        soup = BeautifulSoup(html, "lxml")
        body = soup.select_one("#mwLw")
        if not body:
            return []
        for row in body.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 6:
                continue

            location_tag = cells[0].select_one('a[rel="mw:WikiLink"]')
            if location_tag is None:
                continue
            location = location_tag["title"]
            if location == "World population":
                continue

            population = cells[2].get_text().replace(",", "")
            if population == "N/A":
                continue

            region_tag = cells[4].select_one('a[rel="mw:WikiLink"]')
            if region_tag is None:
                continue
            region = region_tag["title"]

            data.append(
                {
                    "location": location,
                    "population": int(population),
                    "region": region,
                }
            )

        return data


class Parsers:
    @staticmethod
    def get_parser(name: str) -> BaseParser:
        parsers_dict = {
            "wikipedia": WikipediaParser,
        }
        parser = parsers_dict.get(name.lower())
        if not parser:
            raise ValueError(f"Parser {name} does not exist.")

        return parser()
