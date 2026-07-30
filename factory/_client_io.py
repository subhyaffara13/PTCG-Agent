import json
def filter_state(game_state: dict) -> dict:
    return {k: v for k, v in game_state.items() if not k.startswith("_")}

def send_receive(wfile, rfile, payload: str):
    import json
    wfile.write(payload)
    wfile.flush()
    response_line = rfile.readline()
    if not response_line:
        return None
    return json.loads(response_line)
