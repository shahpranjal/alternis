import os

def IS_HEROKU():
    return 'RUNNING_ON_HEROKU' in os.environ
