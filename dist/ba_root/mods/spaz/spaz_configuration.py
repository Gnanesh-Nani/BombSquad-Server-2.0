# dist/ba_root/mods/bomb/spaz_configuration.py
import bascenev1lib.actor.spaz as spaz
import utils
import logger
spaz_settings = utils.get_module_setting("spaz")

def default_spaz_configuarion():
    try:
        spaz.Spaz.default_shields = spaz_settings["shield"]["has_default_shields"]
        spaz.Spaz.default_shield_decay_rate = spaz_settings["shield"]["default_shield_decay_rate"]
        spaz.Spaz.default_shield_hitpoints = spaz_settings["shield"]["default_shield_hitpoints"]

        spaz.Spaz.default_boxing_gloves = spaz_settings["has_default_boxing_gloves"]
        spaz.Spaz.default_hitpoints = spaz_settings["default_hitpoints"]
    except Exception as e:
        logger.log_error(f"Failed to apply spaz configuration: {e} - using defaults.")
        spaz.Spaz.default_shield = False
        spaz.Spaz.default_boxing_gloves = False
        spaz.Spaz.default_hitpoints = 1000
        spaz.Spaz.default_shield_decay_rate = 10.0