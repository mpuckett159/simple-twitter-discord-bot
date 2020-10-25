import os
from typing import Any

import tweepy
from discord_webhook import DiscordWebhook


def _env(
    key: str,
    fail: bool = True,
    default: Any = None,
) -> Any:
    """
    Function used to read container/OS environmnet variables in and return the
    values to be stored in global Python variables.
    """
    value = os.environ.get(key)
    if value is None:
        if fail and default is None:
            raise KeyError(f"Key '{key}' is not present in environment!")
        value = default
    return value


DISCORD_WEBHOOK_URL = _env(key="DISCORD_WEBHOOK_URL")


def send_discord_message(url: str, message: str) -> None:
    print("sending update message to Discord channel")
    webhook = DiscordWebhook(url=url, content=message)
    webhook.execute()


class Listener(tweepy.StreamListener):
    """
    Listener implementation for when a status matching the track is received.
    """

    def on_status(self, status: tweepy.Status):
        print("Got a new message, sending on to Discord.")
        send_discord_message(DISCORD_WEBHOOK_URL, status)

    def on_error(self, status_code):
        print(f"There was an error: {status_code}")
        print("Continuing...")
        return True


def get_api():
    """
    Function to create and authenticate session with the Twitter API
    """
    twitter_api_key = _env(key="TWITTER_API_KEY")
    twitter_api_secret = _env(key="TWITTER_API_SECRET")
    twitter_access_token = _env(key="TWITTER_ACCESS_TOKEN")
    twitter_token_secret = _env(key="TWITTER_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_access_token, twitter_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()
    return api


def main():
    """
    Top level function for running the twitter-to-signal loop.
    """
    print("Loading API")
    api = get_api()
    print("Creating Stream")
    stream = tweepy.Stream(auth=api.auth, listener=Listener())
    account_to_follow = [_env(key="ACCOUNT_TO_FOLLOW")]
    print(f"Account to follow {','.join(account_to_follow)}")
    print("Beginning stream follow")
    stream.filter(follow=account_to_follow, stall_warnings=True)


if __name__ == "__main__":
    main()
