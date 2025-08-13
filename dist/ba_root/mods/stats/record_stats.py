import os
from typing import Dict, Any, List, Tuple
from bascenev1._activitytypes import ScoreScreenActivity
import bascenev1 as bs
import utils
from cache import stats_cache , profile_cache, bank_cache

import logger
from datetime import datetime, timezone


stats_settings = utils.get_module_setting("stats")
shopSystem_settings = utils.get_module_setting("shopSystem")

# Store original method
_original_on_begin = ScoreScreenActivity.on_begin

def _patched_show_player_scores(self, *args, **kwargs) -> None:
    """Patched version that records player stats using the stats cache."""
    # Call original method first
    _original_on_begin(self, *args, **kwargs)
    
    for p_entry in self.stats.get_records().values():
        # Only process entries with valid players and account IDs
        if p_entry.player is not None:
            account_id = p_entry.player.get_v1_account_id()
            if account_id is not None:
                # Get existing stats or initialize new entry
                if(stats_settings["record_stats"]):
                    player_stats = stats_cache.get_player_stats(account_id, {
                        'kills': 0,
                        'deaths': 0,
                        'score': 0,
                        'kd': 0.0,
                        'games_played': 0
                    })

                    # Update stats
                    player_stats['kills'] += p_entry.accum_kill_count
                    player_stats['deaths'] += p_entry.accum_killed_count
                    player_stats['score'] += p_entry.accumscore
                    player_stats['games_played'] += 1
                    player_stats['kd'] = round(
                        player_stats['kills'] / (player_stats['deaths'] if player_stats['deaths'] > 0 else 1), 2
                    )
                    stats_cache.update_player_stats(account_id, player_stats)

                if shopSystem_settings["enabled"]:
                    bank_data = bank_cache.get_bank_data(account_id, {
                        'tickets': 0,
                        'tags': None,
                        'effects': None
                    })
                    bank_data['tickets'] += shopSystem_settings["tickets_per_kill"] * p_entry.accum_kill_count
                    bank_cache.update_bank_data(account_id, bank_data)

                player_profile = profile_cache.get_player_profile(account_id,{
                    'characters_used': {},
                    'last_seen': utils.get_current_time_iso(),
                })
                
                # Update player profile
                player_profile['last_display_name'] = p_entry.name
                if p_entry.character:
                    char = p_entry.character
                    player_profile['characters_used'][char] = (
                        player_profile['characters_used'].get(char, 0) + 1
                )
                player_profile['last_seen'] = utils.get_current_time_iso()
                
                # Update in cache
                profile_cache.update_player_profile(account_id, player_profile)
    
    if( stats_settings["record_stats"]):
        stats_cache.calculate_ranks()
        stats_cache.save_stats()
    if shopSystem_settings["enabled"]:
        bank_cache.save_bank_data()
    profile_cache.save_profiles()
    

def record_stats() -> None:
    """Activate the stats tracking system."""
    logger.log_debug("Wrapping ScoreScreenActivity.onbegin class for stats recording.")
    ScoreScreenActivity.on_begin = _patched_show_player_scores
    logger.log_success("Stats recording system activated!")