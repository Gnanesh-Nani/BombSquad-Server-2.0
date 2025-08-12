# /dist/ba_root/mods/cache/stats_cache.py
import json
from pathlib import Path
import utils
import logger

stats_settings = utils.get_module_setting("stats")
# STATS_FILE = Path(__file__).parent.parent / "stats" / stats_settings["stats_file"]
STATS_FILE = Path(__file__).parent / "json_data" / stats_settings["stats_file"]

class _StatsCache:
    def __init__(self, cache_file=STATS_FILE):
        self.cache_file = Path(cache_file)
        self.stats = self.load_stats()

    def load_stats(self):
        """Load stats from disk"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_stats(self):
        """Save stats to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def update_player_stats(self, key, value):
        """Update a stat in memory (call save_stats to persist)"""
        self.stats[key] = value

    def get_player_stats(self, key, default=None):
        """Get a stat value"""
        return self.stats.get(key, default)
    
    def get_player_rank(self, account_id):
        """Get the rank of a player by account ID"""
        return self.stats.get(account_id, {}).get('rank', 0)

    def get_player_kd(self,account_id):
        return self.stats.get(account_id,{}).get('kd',0)
    
    def calculate_ranks(self):
        """Recalculate all player ranks based on current scores"""
        # Get all players with their scores
        players = []
        for account_id, data in self.stats.items():
            players.append({
                'account_id': account_id,
                'score': data.get('score', 0),
                'name': data.get('last_display_name', 'Unknown')
            })
        
        # Sort by score (descending)
        players.sort(key=lambda x: x['score'], reverse=True)
        
        # Update ranks
        for rank, player in enumerate(players, start=1):
            self.stats[player['account_id']]['rank'] = rank

stats_cache = _StatsCache()