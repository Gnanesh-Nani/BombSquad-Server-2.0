# dist/ba_root/mods/bomb/custom_bomb_count.py
import bascenev1lib.actor.spaz as spaz
import utils
bomb_settings = utils.get_module_setting("bomb")

def apply_custom_bomb_count():
    new_count = bomb_settings.get("default_bomb_count")
    spaz.Spaz.default_bomb_count = new_count
