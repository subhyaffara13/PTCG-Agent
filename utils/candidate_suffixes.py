
def candidate_suffixes(fullname: str) -> list[str]:
    components = fullname.split(".")
    result = [""]
    for i in range(len(components)):
        result.append(".".join(components[-i - 1 :]) + ".")
    return result

