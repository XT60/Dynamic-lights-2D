import Config

def is_zero(x):
    return -Config.ZERO_TOLERANCE <= x <= Config.ZERO_TOLERANCE  


def is_between(value, start, end):
    return start - Config.ZERO_TOLERANCE < value < end + Config.ZERO_TOLERANCE


def is_bigger(value, min_val):
    return min_val - Config.ZERO_TOLERANCE < value


def is_equal(val1, val2):
    return abs(val1 - val2) < Config.ZERO_TOLERANCE