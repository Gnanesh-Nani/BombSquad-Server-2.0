# dist/ba_root/mods/spaz/__init__.py
from . import spaz_configuration
import logger

def apply_spaz_mods():
    spaz_configuration.default_spaz_configuarion()
    logger.log_success("Applied Spaz mods...")