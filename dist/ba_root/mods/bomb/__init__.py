# dist/ba_root/mods/bomb/__init__.py
from . import bomb_configuration
import logger

def apply_bomb_mods():
    bomb_configuration.apply_custom_bomb_count()
    logger.log_success("Applied Bomb mods...")

    
