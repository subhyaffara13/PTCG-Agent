
def setmesstext(block):
    global filepositiontext

    try:
        filepositiontext = f"In: {block['from']}:{block['name']}\n"
    except Exception:
        pass

