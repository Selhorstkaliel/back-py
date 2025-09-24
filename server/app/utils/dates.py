from datetime import datetime

def quinzena(dt: datetime) -> int:
    return 1 if dt.day <= 15 else 2