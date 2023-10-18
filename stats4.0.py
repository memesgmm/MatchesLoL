import requests

# Define headers with the API key for V5 requests
def get_headers(api_key):
    return {
        "X-Riot-Token": api_key
    }

# Define the API base URL based on the region for V4
def get_api_base_url_v4(region):
    base_urls_v4 = {
        "BR": "br1.api.riotgames.com",
        "EUNE": "eun1.api.riotgames.com",
        "EUW": "euw1.api.riotgames.com",
        "JP": "jp1.api.riotgames.com",
        "KR": "kr.api.riotgames.com",
        "LAN": "la1.api.riotgames.com",
        "LAS": "la2.api.riotgames.com",
        "NA": "na1.api.riotgames.com",
        "OCE": "oc1.api.riotgames.com",
        "TR": "tr1.api.riotgames.com",
        "RU": "ru.api.riotgames.com",
    }
    return base_urls_v4.get(region, None)

# Define the API base URL based on the region for V5
def get_api_base_url_v5(region):
    base_urls_v5 = {
        "BR": "americas.api.riotgames.com",
        "LAN": "americas.api.riotgames.com",
        "LAS": "americas.api.riotgames.com",
        "NA": "americas.api.riotgames.com",
        "JP": "asia.api.riotgames.com",
        "KR": "asia.api.riotgames.com",
        "EUNE": "europe.api.riotgames.com",
        "EUW": "europe.api.riotgames.com",
        "RU": "europe.api.riotgames.com",
        "TR": "europe.api.riotgames.com",
        "OCE": "sea.api.riotgames.com",
    }
    return base_urls_v5.get(region, None)

def get_summoner_puuid(summoner_name, region, api_key):
    api_base_url = get_api_base_url_v4(region)
    
    if api_base_url:
        summoner_url = f"https://{api_base_url}/lol/summoner/v4/summoners/by-name/{summoner_name}"
        response = requests.get(summoner_url, headers=get_headers(api_key))

        if response.status_code == 200:
            summoner_data = response.json()
            summoner_puuid = summoner_data["puuid"]
            return summoner_puuid
        else:
            print(f"Failed to retrieve summoner data using V4. Status Code: {response.status_code}")
            return None

def get_matchlist(summoner_puuid, region, count, api_key):
    api_base_url = get_api_base_url_v5(region)
    matchlist_url = f"https://{api_base_url}/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids"
    params = {"start": 0, "count": count}
    response = requests.get(matchlist_url, params=params, headers=get_headers(api_key))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve matchlist. Status Code: {response.status_code}")
        return None

def get_match_details(match_id, region, api_key):
    api_base_url = get_api_base_url_v5(region)
    match_url = f"https://{api_base_url}/lol/match/v5/matches/{match_id}"
    response = requests.get(match_url, headers=get_headers(api_key))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve match details. Status Code: {response.status_code}")
        return None

def get_champion_names():
    champion_names = {}
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/10.25.1/data/en_US/champion.json")

    if response.status_code == 200:
        data = response.json()
        for champion in data["data"]:
            champ_data = data["data"][champion]
            champion_names[int(champ_data["key"])] = champ_data["name"]
    return champion_names

def main():
    api_key = input("Enter your Riot Games API key: ")
    summoner_name = input("Enter the summoner's name: ")
    region = input("Enter the region (e.g., NA, EUW, KR): ").upper()
    count = 5  # Number of matches to retrieve

    champion_names = get_champion_names()  # Retrieve champion names

    summoner_puuid = get_summoner_puuid(summoner_name, region, api_key)

    if summoner_puuid:
        matches = get_matchlist(summoner_puuid, region, count, api_key)

        if matches:
            match_details = []

            for match in matches:
                match_data = get_match_details(match, region, api_key)

                if match_data:
                    participants = match_data["info"]["participants"]
                    for participant in participants:
                        if participant["puuid"] == summoner_puuid:
                            result = "Victory" if participant["win"] else "Defeat"
                            champion_id = participant["championId"]
                            champion_name = champion_names.get(champion_id, f"Champion {champion_id}")
                            kda = f"{participant['kills']}/{participant['deaths']}/{participant['assists']}"
                            print(f"Match Result: {result}, Champion: {champion_name}, KDA: {kda}")

if __name__ == "__main__":
    main()
