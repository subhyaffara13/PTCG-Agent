
def predicate(obj: object) -> bool:
    # This will cause the rest of dynamo to handle the if statement correctly, so we don't have to rewrite it here.
    # We can't just use bool() here since we can't trace into that in general.
    if obj:
        return True
    return False

