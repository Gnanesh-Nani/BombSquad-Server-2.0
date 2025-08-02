# /dist/ba_root/mods/utils.py
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

def load_settings(settings_file: str = "settings.json") -> Dict[str, Any]:
    mods_dir = Path(__file__).parent
    settings_path = mods_dir / settings_file
    
    try:
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Settings file not found: {settings_path}")
            return {}
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}

def get_module_setting(key: str, default: Any = None, settings_file: str = "settings.json") -> Any:
    settings = load_settings(settings_file)
    return settings.get(key, default)

def get_all_settings(settings_file: str = "settings.json") -> Dict[str, Any]:
    return load_settings(settings_file)

