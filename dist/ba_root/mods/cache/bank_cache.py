import json
from pathlib import Path

BANK_FILE = Path(__file__).parent / "json_data" / "bank.json"

class _BankCache:
    def __init__(self, cache_file=BANK_FILE):
        self.cache_file = Path(cache_file)
        self.bank_data = self.load_bank_data()

    def load_bank_data(self):
        """Load bank data from disk"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_bank_data(self):
        """Save bank data to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.bank_data, f, indent=2)

    def update_bank_data(self, account_id, data):
        """Update bank data for a specific account ID"""
        self.bank_data[account_id] = data
        self.save_bank_data()

    def get_bank_data(self, account_id,default=None):
        """Get bank data for a specific account ID"""
        return self.bank_data.get(account_id, default)
    
bank_cache = _BankCache()