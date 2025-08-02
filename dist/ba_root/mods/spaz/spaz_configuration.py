# dist/ba_root/mods/bomb/spaz_configuration.py
import bascenev1lib.actor.spaz as spaz
import utils
import logger
spaz_settings = utils.get_module_setting("spaz")

def default_spaz_configuarion():
    try:
        spaz.Spaz.default_shields = spaz_settings.get("has_default_shields")
        spaz.Spaz.default_boxing_gloves = spaz_settings.get("has_default_boxing_gloves")
        spaz.Spaz.default_hitpoints = spaz_settings.get("default_hitpoints")
    except Exception as e:
        logger.log_error(f"Failed to apply default spaz configuration: {e}")
        spaz.Spaz.default_shield = False
        spaz.Spaz.default_boxing_gloves = False
        spaz.Spaz.default_hitpoints = 1000