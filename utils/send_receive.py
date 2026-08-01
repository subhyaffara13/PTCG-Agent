
def send_receive(wfile, rfile, payload: str):
    import json
    wfile.write(payload)
    wfile.flush()
    response_line = rfile.readline()
    if not response_line:
        return None
    return json.loads(response_line)

