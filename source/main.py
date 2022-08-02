# https://github.com/balasclava

import requests
import json


class Riot:

    def __init__(self):
        self.latest_version = self.get_versions()[0]
        self.champions_data = self.get_champions_data()
        self.skins_data = self.get_skins_data()

    def get_database(self) -> list:
        return [
            {
                "championId": self.champions_data[champion]["key"],
                "championName": self.champions_data[champion]["name"],
                "championSkins": self.get_champion_skins(
                    self.champions_data[champion]["key"]
                )
            }
            for champion in self.champions_data
        ]

    def get_champion_skins(self, requested_champion_id: str) -> list:
        return [
            {
                "skinId": self.skins_data[skin]["id"],
                "skinName": self.skins_data[skin]["name"],
                "skinRarity": self.skins_data[skin]["rarity"]
            }
            for skin in self.skins_data
            if not self.skins_data[skin]["isBase"]
            and self.skins_data[skin]["tilePath"].split("/")[-2] == requested_champion_id
        ]

    def get_skins_data(self) -> dict:
        return requests.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json").json()

    def get_champions_data(self) -> dict:
        return requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.latest_version}/data/pt_BR/champion.json").json()["data"]

    def get_versions(self) -> list:
        return requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()


if __name__ == "__main__":
    riot = Riot()
    database = riot.get_database()

    with open("database/response.json", "w", encoding="UTF-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
