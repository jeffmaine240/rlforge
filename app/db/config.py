from app.core.config import Config

class DatabaseConfig:
    """Database configuration container"""
    
    def __init__(self):
        self.database_url = Config.database_url
        self.echo = Config.DEBUG
        self.echo_pool = False
        self.pool_size = 20
        self.max_overflow = 30
        self.pool_timeout = 30
        self.pool_recycle = 3600
        self.pool_pre_ping = True
