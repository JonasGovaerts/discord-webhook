#!/usr/bin/python

'''
Application which can receive Emby webhook and transform it to
a webhook for Discord
'''

import os
from datetime import datetime
import json
import requests
from flask import Flask, request

app = Flask(__name__)
discord_url = os.environ["DISCORD_URL"].split(",")
emby_url = os.environ["EMBY_URL"]
sonarr_url = os.environ["SONARR_URL"]
radarr_url = os.environ["RADARR_URL"]

@app.route("/api/webhooks/discord", methods=['POST','GET'])
def receive():
    '''
    Module to receive webhook from Emby, Sonarr and Radarr  and forward it to discord
    '''
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if request.is_json:
        user_agent = request.headers.get('User-Agent')
        if "Sonarr" in user_agent:
            avatar_url = "https://sonarr.tv/img/logo.png"
            for url in discord_url:
                response = json.loads(requests.get(url).text)
                if response['name'] == "Sonarr":
                    sonarr_discord_url = url
            data = request.get_json()
            series_name = data['series']['title']
            season_number = str(data['episodes'][0]['seasonNumber'])
            episode_name = data['episodes'][0]['title']
            event_type = data['eventType']
            discord_body = {
                    "username": "Sonarr",
                    "content": event_type+" on Sonarr",
                    "avatar_url": avatar_url, 
                    "embeds": [{
                        "title": event_type+" on Sonarr",
                        "url": sonarr_url,
                        "thumbnail": {
                              "url": avatar_url
                        },
                        "fields": [
                            {
                                "name": "Series",
                                "value": series_name
                            },
                            {
                                "name": "Season",
                                "value": "Season "+season_number
                            },
                            {
                                "name": "Episode",
                                "value": episode_name
                            },
                            {
                                "name": "Date",
                                "value": date
                            }
                        ]
                    }]
            }

            code = requests.post(sonarr_discord_url, json=discord_body).status_code
            return [code]

        if "Radarr" in user_agent:
            avatar_url = "https://radarr.video/img/logo.png"
            for url in discord_url:
                response = json.loads(requests.get(url).text)
                if response['name'] == "Radarr":
                    radarr_discord_url = url

            data = request.get_json()
            movie_name = data['movie']['title']
            event_type = data['eventType']
            discord_body = {
                    "username": "Radarr",
                    "content": event_type+" on Radarr",
                    "avatar_url": avatar_url,
                    "embeds": [{
                        "title": event_type+" on Radarr",
                        "url": radarr_url,
                        "thumbnail": {
                              "url": avatar_url
                        },
                        "fields": [
                            {
                                "name": "Movie",
                                "value": movie_name
                            },
                            {
                                "name": "Date",
                                "value": date
                            }
                        ]
                    }]
            }

            code = requests.post(radarr_discord_url, json=discord_body).status_code
            return [code]

    if request.form:
        user_agent = request.headers.get('User-Agent')
        if "Emby" in user_agent:
            avatar_url = "https://emby.media/resources/logowhite_1881.png"
            for url in discord_url:
                response = json.loads(requests.get(url).text)
                if response['name'] == "Emby":
                    emby_discord_url = url

            data = json.loads(request.form.get('data'))
            date = data["Date"]
            content_type = data['Item']['Type']

            if content_type == "Episode":
                series_name = data['Item']['SeriesName']
                season_name = data['Item']['SeasonName']
                episode_name = data['Item']['Name']
                discord_body = {
                        "username": "Emby",
                        "content": "New episode available on Emby",
                        "avatar_url": avatar_url,
                        "embeds": [{
                            "title": "Watch it here",
                            "url": emby_url,
                            "thumbnail": {
                                "url": avatar_url
                            },
                            "fields": [
                                {
                                    "name": "Series",
                                    "value": series_name
                                },
                                {
                                    "name": "Season",
                                    "value": season_name
                                },
                                {
                                    "name": "Episode",
                                    "value": episode_name
                                },
                                {
                                    "name": "Date",
                                    "value": date
                                }
                            ]
                        }]
                }

            code = requests.post(emby_discord_url, json=discord_body).status_code
            return [code]
