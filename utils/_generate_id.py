import uuid

def _generate_id():  # private helper function
    return "chatcmpl-" + str(uuid.uuid4())

