
def parse_list(lst: str) -> list[int]:
    lst = lst.replace("[", "").replace("]", "")
    substrings = lst.split(",")

    return [int(substring.strip()) for substring in substrings]

