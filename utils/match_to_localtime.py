import re
import time

def match_to_localtime(match: re.Match[str]) -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    sec = int(sec_str) if sec_str else 0
    micros = int(micros_str.ljust(6, "0")) if micros_str else 0
    return time(int(hour_str), int(minute_str), sec, micros)


def match_to_localtime(match: re.Match[str]) -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    sec = int(sec_str) if sec_str else 0
    micros = int(micros_str.ljust(6, "0")) if micros_str else 0
    return time(int(hour_str), int(minute_str), sec, micros)


def match_to_localtime(match: re.Match) -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    micros = int(micros_str.ljust(6, "0")) if micros_str else 0
    return time(int(hour_str), int(minute_str), int(sec_str), micros)


def match_to_localtime(match: re.Match[str]) -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    micros = int(micros_str.ljust(6, "0")) if micros_str else 0
    return time(int(hour_str), int(minute_str), int(sec_str), micros)


def match_to_localtime(match: "re.Match") -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    micros = int(micros_str.ljust(6, "0")) if micros_str else 0
    return time(int(hour_str), int(minute_str), int(sec_str), micros)

