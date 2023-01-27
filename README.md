[![Docker Image CI](https://github.com/jonasgovaerts/discord-webhook/actions/workflows/docker-image.yml/badge.svg)](https://github.com/jonasgovaerts/discord-webhook/actions/workflows/docker-image.yml)

# Discord-Webhook
This python webapp is used to receive webhooks from Sonarr, Radarr and Emby and post them to discord.
It uses the user-agent header to identify which applicaiton is sending the request.
Sonarr and Radarr send their webhooks as json, Emby sends it as multipart/form.

# Docker
The application has been build as a container image and can be run with following parameters

```bash
docker run -d --name discord-webhook \
	-p 5000:5000 \
	-e DISCORD_URL="" \ #Discord URLs to push webhook to. Create seperate ones with names Radarr, Sonarr, Emby. comma-seperated
	-e SONARR_URL="" \ #URL of your Sonarr instance, used to create hyperlinks in your discord message 
	-e RADARR_URL="" \ #URL of your Radarr instance, used to create hyperlinks in your discord message
	-e EMBY_URL="" #URL of your Emby instance, used to create hyperlinks in your discord message
	docker.io/govaertsjonas/discord-webhook
```
