import os

import redis

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'QNPviGKm4kUPG2wVslmQaUNNndnnpPby'
    # Configure redis for flask-session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://localhost:6379')
