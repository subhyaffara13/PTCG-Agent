
def list_to_robot(uid, lst):
    return {
        "uid": uid,
        "type": lst[0],
        "col": lst[1],
        "row": lst[2],
        "energy": lst[3],
        "owner": lst[4],
        "move_cooldown": lst[5],
        "jump_cooldown": lst[6],
        "build_cooldown": lst[7] if len(lst) > 7 else 0,
    }

