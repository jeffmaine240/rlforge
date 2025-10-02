import datetime

def utcnow():
    """
    Returns the current UTC time.
    """
    return datetime.datetime.now(datetime.timezone.utc)


def to_naive_utc(dt: datetime.datetime):
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt
