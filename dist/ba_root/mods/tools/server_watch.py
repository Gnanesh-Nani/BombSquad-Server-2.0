import bascenev1 as bs
import babase
from cache import stats_cache, profile_cache
from typing import Dict, List, Set
import utils

class _ServerWatch:
    def __init__(self):
        self._timer: babase.AppTimer | None = None
        self._current_players: Set[str] = set()  # Tracks account_ids of current players
        self._previous_players: Set[str] = set()  # Previous check's players
        self._player_data: Dict[str, dict] = {}  # Stores full player info

    def check_for_player_changes(self):
        """Check for player joins/leaves and handle them."""
        current_roster = bs.get_game_roster()
        current_account_ids = {str(p['account_id']) for p in current_roster if p.get('account_id')}

        for player in current_roster:
            if 'account_id' in player:
                self._player_data[str(player['account_id'])] = player

        # Detect joins (in current but not previous)
        new_players = current_account_ids - self._previous_players
        for account_id in new_players:
            self._on_player_join(self._player_data[account_id])

        # Detect leaves (in previous but not current)
        left_players = self._previous_players - current_account_ids
        for account_id in left_players:
            self._on_player_leave(self._player_data.get(account_id, {}))

        self._previous_players = current_account_ids

    def _on_player_join(self, player_data: dict):
        """Handle new player joining."""
        name = player_data.get('display_string', 'Unknown')
        client_id = player_data.get('client_id', None)
        if(profile_cache.get_player_profile(player_data.get('account_id')) is None):
            profile_cache.update_player_profile(
                player_data['account_id'],
                {
                    'characters_used': {},
                    'last_seen': utils.get_current_time_iso(),
                    'name': name,
                    'last_display_name': None
                }
            )
            bs.broadcastmessage(f"Welcome to Our Server {name}!,we saving ur Profile data, You Got Welcome Bonus as 200 \ue01f", color=(1.0, 1.0, 1.0), transient=True, clients=[client_id])
        else:
            bs.broadcastmessage(f"Welcome {name}!",color=(1.0, 1.0, 1.0),transient = True,clients = [client_id])
        

    def _on_player_leave(self, player_data: dict):
        """Handle player leaving."""
        # name = player_data.get('display_string', 'Unknown')
        # client_id = player_data.get('client_id', None)
        # bs.broadcastmessage(f"Welcome {name}!",color=(0.5, 1.0, 0.5),transient = True,clients = [client_id])
        #print(f"PLAYER LEFT: {json.dumps(player_data, indent=2)}")

    def start(self):
        """Start monitoring."""
        if not self._timer:
            self._timer = babase.AppTimer(1, self.check_for_player_changes, repeat=True)
            
            self._previous_players = {
                str(p['account_id']) 
                for p in bs.get_game_roster() 
                if p.get('account_id')
            }

    def stop(self):
        """Stop monitoring."""
        if self._timer:
            self._timer = None


server_watch = _ServerWatch()
