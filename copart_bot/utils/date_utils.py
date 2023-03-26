import datetime
from typing import Optional


def convert_timestamp_to_datetime(timestamp_mil: int) -> Optional[datetime.datetime]:
    if timestamp_mil:
        timestamp_sec = timestamp_mil // 1000
        return datetime.datetime.fromtimestamp(timestamp_sec)
    return None

