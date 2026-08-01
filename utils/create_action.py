
def create_action(serialized):
    return ACTION_REGISTRY[serialized["action_type"]](**serialized.get("kwargs", {}))

