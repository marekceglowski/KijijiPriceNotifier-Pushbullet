# Kijiji Price Notifier (PushBullet)

Small application to receive notifications on low prices from Kijiji.

When running it you must specify a search term for Kijiji and a maximum price. The application will then watch for new listings that are less than the price specfied.

You will receive notifications on Pushbullet.

## How to use

### Parameters

- **--url/SEARCH_URL**: The search of Kijiji to scrape.
- **--token/PUSHBULLET_TOKEN**: Telegram bot token.
- **--max/MAX_PRICE**: Maximum price to look at.

(Note: --url is a script argument, and SEARCH_URL is an environment variable).

### Docker 

The fastest way to get up and running is to use Docker.

Run the following command, replacing the search term, Telegram token, Telegram chat ID, and maximum price with your own values.

```shell
docker run -d --name kijijinotifier -e SEARCH_URL='https://www.kijiji.ca/b-phone-tablet/ontario/phone/k0c132l9004?ad=offering' -e PUSHBULLET_TOKEN='AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw' -e MAX_PRICE='100' marekceglowski/KijijiPriceNotifier-Pushbullet:latest
```

### Run Directly

Make sure you have Python 3 installed on your system and all the PIP packages that are required (pip install -r requirements.txt).

```shell
./main.py --url https://www.kijiji.ca/b-phone-tablet/ontario/phone/k0c132l9004?ad=offering --token AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw --max 100
```

You can also run in the background using nohup on linux:

```shell
nohup ./main.py --url https://www.kijiji.ca/b-phone-tablet/ontario/phone/k0c132l9004?ad=offering --token AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw --max 100 &
```

### Get Pushbullet Token

1. Login to your pushbullet account.
2. Go to Settings to get your Access Token: https://www.pushbullet.com/#settings
3. If there is no Access Token visible, click on Create Access Token.
