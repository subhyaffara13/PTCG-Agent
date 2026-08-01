
def good_repr(obj: object) -> str:
    if isinstance(obj, str):
        if obj.count("\n") > 1:
            bits = ["'''\\"]
            for line in obj.split("\n"):
                # force repr to use ' not ", then cut it off
                bits.append(repr('"' + line)[2:-1])
            bits[-1] += "'''"
            return "\n".join(bits)
    return repr(obj)

