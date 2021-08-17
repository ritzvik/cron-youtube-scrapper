import os

class EnvironmentVars:
    def __init__(self):
        
        self.SECRET_KEY = "znu@df2u!hvqe+03psfp-u11rs8e91$)h0)zb+1i^=z_@83rm="
        self.DEBUG = True
        self.DB_CONN_AGE = 60

        self.ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PWD = os.environ.get("DB_PWD")
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")

        self.REDIS_HOST = os.environ.get("REDIS_HOST")
        self.REDIS_PORT = os.environ.get("REDIS_PORT")

        self.CACHE_PREFIX = os.environ.get("CACHE_PREFIX", f"code_{self.ENVIRONMENT}")

        self.YOUTUBE_QUERY_STRING = os.environ.get("YOUTUBE_QUERY_STRING", "INDIA")
        self.YOUTUBE_KEYS = [os.environ.get("YOUTUBE_KEY", 'AIzaSyBUk_Gutur67QaJd0DJDMTgvPSbKfjTEKo')]
