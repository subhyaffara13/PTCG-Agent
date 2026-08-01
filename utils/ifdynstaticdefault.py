
def ifdynstaticdefault(count1: Any, count2: Any) -> Any:
    if torch._dynamo.config.assume_static_by_default:
        return count1
    else:
        return count2

