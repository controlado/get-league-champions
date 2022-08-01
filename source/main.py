# https://github.com/balasclava

import requests
import json


class Riot:

    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"

    def __init__(self):
        self.latest_version = self.get_versions()[0]
        self.champions_data = self.get_champions_data()

    def get_champions_names(self) -> list:
        return [self.champions_data[champion]["name"] for champion in self.champions_data]

    def get_champions_data(self) -> dict:
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.latest_version}/data/pt_BR/champion.json"
        response = requests.get(url)
        return response.json()["data"]

    def get_versions(self) -> list:
        response = requests.get(self.versions_url)
        return response.json()


if __name__ == "__main__":
    riot = Riot()
    champions_names = riot.get_champions_names()

    with open("database/response.json", "w", encoding="UTF-8") as f:
        json.dump(champions_names, f, indent=4, ensure_ascii=False)
