import requests
import config


def list_activities():
    response = requests.get("https://www.strava.com/api/v3/athlete",
                            headers={'Authorization': 'Bearer '.join(config.strava_config["token"])})
    print(response.json())


