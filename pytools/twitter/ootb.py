from logging import getLogger

from . import create_api

def tweet(consumer_key, consumer_secret, access_key, access_secret, message):
    logger = getLogger(__name__)
    logger.info("Creating twitter api")
    api = create_api(consumer_key, consumer_secret, access_key, access_secret)
    logger.info("Twitter API created")
    api.update_status(status=message)
    logger.info("Message tweeted")
