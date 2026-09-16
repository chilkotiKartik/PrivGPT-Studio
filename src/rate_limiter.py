\"\"\"
Authentication validation and in-memory rate limiting engine for PrivGPT-Studio API gateways.
\"\"\"
import time
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_history: Dict[str, list] = {}

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        now = time.time()
        timestamps = self.request_history.get(client_id, [])
        valid_timestamps = [t for t in timestamps if now - t < self.window_seconds]
        
        if len(valid_timestamps) >= self.max_requests:
            remaining = 0
            self.request_history[client_id] = valid_timestamps
            return False, remaining
        
        valid_timestamps.append(now)
        self.request_history[client_id] = valid_timestamps
        remaining = self.max_requests - len(valid_timestamps)
        return True, remaining