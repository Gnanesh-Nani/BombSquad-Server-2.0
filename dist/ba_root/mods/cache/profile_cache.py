import json
from pathlib import Path
import utils
import logger

PROFILE_FILE = Path(__file__).parent / "json_data" / "profiles.json"

class _ProfileCache:
    def __init__(self, cache_file=PROFILE_FILE):
        self.cache_file = Path(cache_file)
        self.profiles = self.load_profiles()

    def load_profiles(self):
        """Load profiles from disk"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_profiles(self):
        """Save profiles to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)

    def update_player_profile(self, account_id, profile_data):
        """Update a profile in memory (call save_profiles to persist)"""
        self.profiles[account_id] = profile_data

    def get_player_profile(self, account_id,default=None):
        """Get a profile by account ID"""
        return self.profiles.get(account_id, default)
    

profile_cache = _ProfileCache()