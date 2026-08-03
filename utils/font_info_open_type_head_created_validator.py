from typing import Any

def fontInfoOpenTypeHeadCreatedValidator(value: Any) -> bool:
    """
    Version 2+.
    """
    # format: 0000/00/00 00:00:00
    if not isinstance(value, str):
        return False
    # basic formatting
    if not len(value) == 19:
        return False
    if value.count(" ") != 1:
        return False
    strDate, strTime = value.split(" ")
    if strDate.count("/") != 2:
        return False
    if strTime.count(":") != 2:
        return False
    # date
    strYear, strMonth, strDay = strDate.split("/")
    if len(strYear) != 4:
        return False
    if len(strMonth) != 2:
        return False
    if len(strDay) != 2:
        return False
    try:
        intYear = int(strYear)
        intMonth = int(strMonth)
        intDay = int(strDay)
    except ValueError:
        return False
    if intMonth < 1 or intMonth > 12:
        return False
    monthMaxDay = calendar.monthrange(intYear, intMonth)[1]
    if intDay < 1 or intDay > monthMaxDay:
        return False
    # time
    strHour, strMinute, strSecond = strTime.split(":")
    if len(strHour) != 2:
        return False
    if len(strMinute) != 2:
        return False
    if len(strSecond) != 2:
        return False
    try:
        intHour = int(strHour)
        intMinute = int(strMinute)
        intSecond = int(strSecond)
    except ValueError:
        return False
    if intHour < 0 or intHour > 23:
        return False
    if intMinute < 0 or intMinute > 59:
        return False
    if intSecond < 0 or intSecond > 59:
        return False
    # fallback
    return True

