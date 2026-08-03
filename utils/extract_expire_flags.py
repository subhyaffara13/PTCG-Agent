from typing import List, Optional

def extract_expire_flags(
    ex: Optional[ExpiryT] = None,
    px: Optional[ExpiryT] = None,
    exat: Optional[AbsExpiryT] = None,
    pxat: Optional[AbsExpiryT] = None,
) -> List[EncodableT]:
    exp_options: list[EncodableT] = []
    if ex is not None:
        exp_options.append("EX")
        if isinstance(ex, datetime.timedelta):
            exp_options.append(int(ex.total_seconds()))
        elif isinstance(ex, int):
            exp_options.append(ex)
        elif isinstance(ex, str) and ex.isdigit():
            exp_options.append(int(ex))
        else:
            raise DataError("ex must be datetime.timedelta or int")
    elif px is not None:
        exp_options.append("PX")
        if isinstance(px, datetime.timedelta):
            exp_options.append(int(px.total_seconds() * 1000))
        elif isinstance(px, int):
            exp_options.append(px)
        else:
            raise DataError("px must be datetime.timedelta or int")
    elif exat is not None:
        if isinstance(exat, datetime.datetime):
            exat = int(exat.timestamp())
        exp_options.extend(["EXAT", exat])
    elif pxat is not None:
        if isinstance(pxat, datetime.datetime):
            pxat = int(pxat.timestamp() * 1000)
        exp_options.extend(["PXAT", pxat])

    return exp_options

