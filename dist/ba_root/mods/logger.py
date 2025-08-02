"""
BombSquad Mod Logger (Final Version)
- Full message coloring
- No duplicate logging
- Simplified interface
"""

import logging
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    VIOLET = '\033[95m'
    WHITE = '\033[97m'
    END = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter that colors entire messages"""
    
    def format(self, record):
        msg = super().format(record)
        
        if record.levelname == 'ERROR':
            return f"{Colors.RED}{msg}{Colors.END}"
        elif record.levelname == 'WARNING':
            return f"{Colors.YELLOW}{msg}{Colors.END}"
        elif record.levelname == 'INFO':
            return f"{Colors.WHITE}{msg}{Colors.END}"
        elif record.levelname == 'DEBUG':
            return f"{Colors.VIOLET}{msg}{Colors.END}"
        return msg

class SimpleLogger:
    """Main logger class with full message coloring"""
    
    def __init__(self, name="Mods"):
        # Configure logger to prevent duplicates
        self.logger = logging.getLogger(name)
        self.logger.propagate = False  # Prevent bubbling to root logger
        self.logger.handlers = []     # Remove existing handlers
        
        # Set up our custom handler
        console_handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
    
    def info(self, message):
        """Log info message (white)"""
        self.logger.info(message)
    
    def success(self, message):
        """Log success message (green)"""
        self.logger.info(f"{Colors.GREEN}{message}{Colors.END}")
    
    def warning(self, message):
        """Log warning message (yellow)"""
        self.logger.info(f"{Colors.YELLOW}{message}{Colors.END}")    

    def error(self, message):
        """Log error message (red)"""
        self.logger.info(f"{Colors.RED}{message}{Colors.END}")  

    def debug(self, message):
        """Log debug message (violet)"""
        self.logger.info(f"{Colors.VIOLET}{message}{Colors.END}")
            
    def banner(self, message, color=Colors.WHITE):
        """Log a banner-style message"""
        border = "=" * 50
        self.info(f"{color}{border}{Colors.END}")
        self.info(f"{color}{message.center(50)}{Colors.END}")
        self.info(f"{color}{border}{Colors.END}")

# Create default logger instance
logger = SimpleLogger()

# Quick-access functions
def log_info(msg): logger.info(msg)
def log_success(msg): logger.success(msg)
def log_warning(msg): logger.warning(msg)
def log_error(msg): logger.error(msg)
def log_debug(msg): logger.debug(msg)
def log_banner(msg): logger.banner(msg)

# Example usage
if __name__ == "__main__":
    log_banner("Logger Initialized")
    log_info("This is an info message (white)")
    log_success("Operation completed successfully (green)")
    log_warning("This is a warning (yellow)")
    log_error("Something went wrong (red)")
    log_debug("Debug information (violet)")