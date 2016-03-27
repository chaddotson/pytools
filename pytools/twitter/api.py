from logging import getLogger
from tweepy import API, OAuthHandler



def create_api(consumer_key, consumer_secret, access_key, access_secret):
    logger = getLogger(__name__)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    logger.info("Authenticating to twitter...")
    api = API(auth)
    logger.info("Authenticated")
    return api
