# /dist/ba_root/mods/utils.py
import json
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone

# Simple module-level cache
_SETTINGS_CACHE = {}

def load_settings(settings_file: str = "settings.json") -> Dict[str, Any]:
    """Load settings from JSON file with simple caching"""
    if settings_file in _SETTINGS_CACHE:
        return _SETTINGS_CACHE[settings_file]
    
    mods_dir = Path(__file__).parent
    settings_path = mods_dir / settings_file
    
    try:
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                _SETTINGS_CACHE[settings_file] = settings
                return settings
        else:
            logging.debug(f"Settings file not found: {settings_path}")
            return {}
    except Exception as e:
        logging.error(f"Error loading settings: {e}")
        return {}

def get_module_setting(key: str, default: Any = None, settings_file: str = "settings.json") -> Any:
    """Get a specific setting from cached settings"""
    settings = load_settings(settings_file)
    return settings.get(key, default)

def get_all_settings(settings_file: str = "settings.json") -> Dict[str, Any]:
    """Get all settings from cache"""
    return load_settings(settings_file)

def clear_cache(settings_file: str = None) -> None:
    """Clear cache for specific file or all files"""
    if settings_file is None:
        _SETTINGS_CACHE.clear()
    else:
        _SETTINGS_CACHE.pop(settings_file, None)

def get_current_time_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")