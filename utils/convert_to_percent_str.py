
def convert_to_percent_str(num, denom) -> str:
    if denom == 0:
        return "0%"
    return f"{num / denom:.2%}"

