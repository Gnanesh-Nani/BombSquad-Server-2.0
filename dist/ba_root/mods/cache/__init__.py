from .stats_cache import stats_cache
from .profile_cache import profile_cache
from .bank_cache import bank_cache
import logger

def bootstrap_cache():
    logger.log_success("Cache system initialized successfully.")