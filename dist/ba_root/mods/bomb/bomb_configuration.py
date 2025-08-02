# dist/ba_root/mods/bomb/bomb_configuration.py
import bascenev1lib.actor.spaz as spaz
import utils
import logger
bomb_settings = utils.get_module_setting("bomb")

def apply_bomb_configuration():
    try:
        spaz.Spaz.default_bomb_count = bomb_settings["default_bomb_count"]
        spaz.Spaz.default_bomb_type = bomb_settings["default_bomb_type"]
    except Exception as e:
        logger.log_error(f"Failed to apply bomb configuration: {e} - using defaults.")
        spaz.Spaz.default_bomb_count = 1
        spaz.Spaz.default_bomb_type = 'normal'
