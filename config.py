import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
    'emmab@thieves.com': {
        'name': 'Emma',
        'password': 'ralphiscute'
     },
    'dylank@thieves.com': {
        'name': 'Dylan',
        'password': 'ilovemydog'
     }
}