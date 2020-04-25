from datetime import datetime


def prepare_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S") if date else None
    except ValueError:  # invalid dateformat
        return None
