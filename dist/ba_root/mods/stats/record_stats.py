import json
import os
from typing import Dict, Any, List, Tuple
from bascenev1._activitytypes import ScoreScreenActivity
import bascenev1 as bs
import utils

stats_settings = utils.get_module_setting("stats")

STATS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    stats_settings["stats_file"]
)

def _load_stats() -> Dict[str, Any]:
    """Load existing stats from JSON file."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def _save_stats(stats: Dict[str, Any]) -> None:
    """Save stats to JSON file with ranking."""
    # Calculate ranks before saving
    stats = _calculate_ranks(stats)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def _calculate_ranks(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate and assign ranks to all players based on score."""
    # Create a list of players with their scores
    players = []
    for account_id, player_data in stats.items():
        players.append({
            'account_id': account_id,
            'score': player_data.get('score', 0),
            'name': player_data.get('last_display_name', 'Unknown')
        })
    
    # Sort players by score (descending)
    players_sorted = sorted(players, key=lambda x: x['score'], reverse=True)
    
    # Assign ranks
    for rank, player in enumerate(players_sorted, start=1):
        stats[player['account_id']]['rank'] = rank
    
    return stats

def get_leaderboard(stats: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
    """Return top players sorted by score."""
    players = []
    for account_id, player_data in stats.items():
        players.append({
            'account_id': account_id,
            'name': player_data.get('last_display_name', 'Unknown'),
            'score': player_data.get('score', 0),
            'kills': player_data.get('kills', 0),
            'deaths': player_data.get('deaths', 0),
            'kd': player_data.get('kd', 0.0),
            'rank': player_data.get('rank', 0)
        })
    
    # Sort by score (descending) and return limited results
    return sorted(players, key=lambda x: x['score'], reverse=True)[:limit]

# Store original method
_original_on_begin = ScoreScreenActivity.on_begin

def _patched_show_player_scores(self, *args, **kwargs) -> None:
    """Patched version that records player stats and maintains rankings."""
    # Call original method first
    _original_on_begin(self, *args, **kwargs)
    
    stats = _load_stats()
    
    for p_entry in self.stats.get_records().values():
        # Only process entries with valid players and account IDs
        if p_entry.player is not None:
            account_id = p_entry.player.get_v1_account_id()
            if account_id is not None:
                # Initialize player entry if needed
                if account_id not in stats:
                    stats[account_id] = {
                        'last_display_name': p_entry.name,
                        'kills': 0,
                        'deaths': 0,
                        'score': 0,
                        'kd': 0.0,
                        'games_played': 0,
                        'characters_used': {}
                    }
                
                # Update stats
                stats[account_id]['last_display_name'] = p_entry.name
                stats[account_id]['kills'] += p_entry.accum_kill_count
                stats[account_id]['deaths'] += p_entry.accum_killed_count
                stats[account_id]['score'] += p_entry.accumscore
                stats[account_id]['games_played'] += 1
                stats[account_id]['kd'] = stats[account_id]['kills'] / (
                    stats[account_id]['deaths'] if stats[account_id]['deaths'] > 0 else 1
                )
                
                # Track character usage
                if p_entry.character:
                    char = p_entry.character
                    stats[account_id]['characters_used'][char] = (
                        stats[account_id]['characters_used'].get(char, 0) + 1
                    )
    
    # Save updated stats with rankings
    _save_stats(stats)

    # Optionally display leaderboard in console for debugging
    if stats_settings.get("debug_leaderboard", False):
        leaderboard = get_leaderboard(stats)
        print("\n=== CURRENT LEADERBOARD ===")
        for player in leaderboard:
            print(f"#{player['rank']}: {player['name']} - Score: {player['score']}")

# PATCHING 
def record_stats() -> None:
    """Activate the stats tracking system."""
    ScoreScreenActivity.on_begin = _patched_show_player_scores