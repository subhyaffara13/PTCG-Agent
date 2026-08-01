
def escapeattr(data):
    data = escape(data)
    data = data.replace('"', "&quot;")
    return data

