#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import datetime
from logging import basicConfig, getLogger, INFO
from six import PY2
from six.moves.configparser import RawConfigParser
from socket import gethostname

from pytools.twitter import tweet

logger = getLogger(__name__)

def get_args():
    parser = ArgumentParser(description='No Nonsense Tweet Publisher')
    parser.add_argument('message', help='Message to tweet')
    parser.add_argument('--no_stamp', default=False, action='store_true')
    parser.add_argument('-c', '--configuration', help='Twitter configuration', default='twitter.cfg')

    return parser.parse_args()


if __name__=="__main__":
    logging_config=dict(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    if PY2:
        logging_config['disable_existing_loggers'] = True

    basicConfig(**logging_config)

    args = get_args()
    config = RawConfigParser()
    config.read(args.configuration)

    timestamp = datetime.now().strftime("%H:%M:%S")
    machine = gethostname()

    message = "CNC/{machine} [{timestamp}]: {content}".format(machine=machine, timestamp=timestamp, content=args.message)

    logger.info("Sending message to twitter: %s", message)
    tweet(config.get("TWITTER", "CONSUMER_KEY"),
          config.get("TWITTER", "CONSUMER_SECRET"),
          config.get("TWITTER", "ACCESS_KEY"),
          config.get("TWITTER", "ACCESS_SECRET"),
          message)

    logger.info("Done")
