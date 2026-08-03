import copy
import json

def jsonify_object(data: dict) -> dict:
    db_data = copy.deepcopy(data)

    for k, v in db_data.items():
        if isinstance(v, dict):
            try:
                db_data[k] = json.dumps(v)
            except Exception:
                # This avoids Prisma retrying this 5 times, and making 5 clients
                db_data[k] = "failed-to-serialize-json"
    return db_data

