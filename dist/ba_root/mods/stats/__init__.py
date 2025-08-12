from . import record_stats
import logger
import utils


stats_settings = utils.get_module_setting("stats")

def apply_stats_mods():
    """Initialize the stats recording system."""
    try:
        record_stats.record_stats()
            
    except Exception as e:
        logger.log_error(f"Failed to initialize stats mod: {e}")
        return
    
    logger.log_success("Stats mod initialized successfully!")