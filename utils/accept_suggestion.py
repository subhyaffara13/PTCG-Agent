
def accept_suggestion(input_text: str, auto_accept: bool) -> bool:
    sys.stdout.write(input_text)
    if auto_accept:
        sys.stdout.write("Y\n")
        return True
    return input().lower() != "n"

