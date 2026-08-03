import uuid

def generate_state_key(string="__composable_api_state_key"):
    return f"{string}_{str(uuid.uuid4())}"

