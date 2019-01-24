import re

import unidecode

HOUR_REGEX = re.compile(r"([0-9]*) hours?")
MINUTE_REGEX = re.compile(r"([0-9]*) minutes?")
SECOND_REGEX = re.compile(r"([0-9]*\.?[0-9]*) seconds?")
PERCENT_REGEX = re.compile(r"([0-9]{1,3})\s?%")


def int_or_string(val: str):
    """
    Loads a value from MO into either an int or string value.

    String is returned if we can't turn it into an int.
    """
    new_s = val.replace(",", "")
    try:
        return float(new_s)
    except ValueError:
        return val


def parse_time(val: str) -> float:
    """
    Parse the time out into minutes.
    """
    unit = val.split(" ")[1]
    if 'minute' in unit:
        # Calculate the hour.
        mins = int(val.split(" ")[0])
        hours = round(mins / 60, 3)
        return hours
    else:
        hours = val.split(" ")[0]
        return float(hours)


def try_extract(value):
    """
    Attempt to extract a meaningful value from the time.
    """
    if value == "--":
        return 0

    get_float = int_or_string(value)
    # If it's changed, return the new int value.
    if get_float != value:
        return get_float

    # Next, try and get a time out of it.
    matched = HOUR_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        return val

    matched = MINUTE_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val /= 60
        return val

    matched = SECOND_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val = (val / 60 / 60)

        return val

    matched = PERCENT_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val = (val / 100)

        return val

    # Check if there's an ':' in it.
    if ':' in value:
        sp = value.split(':')
        # If it's only two, it's mm:ss.
        # Formula is (minutes + (seconds / 60)) / 60
        if len(sp) == 2:
            mins, seconds = map(int, sp)
            mins += seconds / 60
            hours = mins / 60
            return hours

        # If it's three, it's hh:mm:ss.
        # Formula is hours + ((minutes + (seconds / 60)) / 60).
        elif len(sp) == 3:
            hours, mins, seconds = map(int, sp)
            mins += (seconds / 60)
            hours += (mins / 60)
            return hours
    else:
        # Just return the value.
        return value


def sanitize_string(string):
    """
    Convert an arbitrary string into the format used for our json keys
    """
    space_converted = re.sub(r'[-\s]', '_', unidecode.unidecode(string).lower())
    removed_nonalphanumeric = re.sub(r'\W', '', space_converted)
    underscore_normalized = re.sub(r'_{2,}', '_', removed_nonalphanumeric)
    return underscore_normalized.replace("soldier_76", "soldier76")  # backwards compatability
