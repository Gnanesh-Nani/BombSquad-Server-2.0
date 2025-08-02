# dist/ba_root/mods/bomb/__init__.py
from . import custom_bomb_count
import logger

def apply_bomb_mods():
    custom_bomb_count.apply_custom_bomb_count()
    logger.log_success("Applied Bomb mods...")

    
