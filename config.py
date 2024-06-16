import os

class Config:
    DEBUG = False
    TESTING = False
    RASA_SERVER_URL = os.getenv('RASA_SERVER_URL', 'http://localhost:5005/webhooks/rest/webhook')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
