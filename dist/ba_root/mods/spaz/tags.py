import bascenev1 as bs
from bascenev1lib.actor import playerspaz
from stats.record_stats import get_rank
import logger

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing import Dict, Any, Sequence

import utils

stats_settings = utils.get_module_setting("stats")

rank_settings = stats_settings["rank"]

class RankTag:
    def __init__(self,player_spaz):
        
        session_player = player_spaz._player._sessionplayer
        self.account_id = session_player.get_v1_account_id()
        if( not self.account_id):
            logger.log_error("RankTag: No account_id found for player_spaz.")
            return
        self.rank = get_rank(self.account_id)
        self.set_rank(player_spaz, color=(1.0, 1.0, 1.0))
    
    def set_rank(self,player_spaz,color: Sequence[float] = (1.0,1.0,1.0) ) -> None:
        if not player_spaz.node:
            return 
        
        color_fin = bs.safecolor(color)[:3]

        mnode = bs.newnode(
            'math',
            owner=player_spaz.node,
            attrs={'input1': (0, 1.5, 0), 'operation': 'add'} 
        )

        player_spaz.node.connectattr('torso_position', mnode, 'input2')

        self._rank_text = bs.newnode(
            'text',
            owner=player_spaz.node,
            attrs={
                'text': rank_settings["unranked_text"] if self.rank == 0 else f"{rank_settings["rank_prefix"]}{self.rank}{rank_settings["rank_suffix"]}",
                'in_world': True,
                'shadow': 1.0,
                'flatness': 1.0,
                'color': color_fin,
                'scale': 0.01,
                'h_align': 'center',
            },
        )

        mnode.connectattr('output', self._rank_text, 'position')
 
def wrap_player_spaz_class(player_spaz_class):
    class wrapper_player_spaz(player_spaz_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if rank_settings["show_rank_on_spaz"]:
                RankTag(self)
    return wrapper_player_spaz

def apply_tags():
    logger.log_debug("Wrapping PlayerSpaz class with RankTag functionality.")
    playerspaz.PlayerSpaz = wrap_player_spaz_class(playerspaz.PlayerSpaz)
        

