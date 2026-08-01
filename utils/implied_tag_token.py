
def impliedTagToken(name, type="EndTag", attributes=None,
                    selfClosing=False):
    if attributes is None:
        attributes = {}
    return {"type": tokenTypes[type], "name": name, "data": attributes,
            "selfClosing": selfClosing}

