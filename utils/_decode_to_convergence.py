
def _decode_to_convergence(value: str) -> str:
    previous = value
    while True:
        decoded = unquote(previous)
        if decoded == previous:
            return decoded
        previous = decoded

