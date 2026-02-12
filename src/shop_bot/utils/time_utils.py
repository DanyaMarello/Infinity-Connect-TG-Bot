import os
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

TZ_NAME = os.getenv('SERVER_TIMEZONE', 'UTC')
if ZoneInfo:
    try:
        TZ = ZoneInfo(TZ_NAME)
    except Exception:
        TZ = timezone.utc
else:
    TZ = timezone.utc


def now() -> datetime:
    """Return current server-local time as timezone-aware datetime."""
    try:
        return datetime.now(TZ)
    except Exception:
        return datetime.utcnow().replace(tzinfo=timezone.utc)


def now_utc() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def iso_now() -> str:
    return now().isoformat()


def to_utc_ms(dt: datetime) -> int:
    """Convert datetime to milliseconds since epoch (UTC)."""
    if dt is None:
        return 0
    try:
        return int(dt.astimezone(timezone.utc).timestamp() * 1000)
    except Exception:
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000)


def from_utc_ms(ms: int) -> datetime:
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    except Exception:
        return datetime.utcnow().replace(tzinfo=timezone.utc)
