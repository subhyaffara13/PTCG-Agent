
def create_uid(obs):
    uid = f"{obs.step}-{obs.nextUid}"
    obs.nextUid = obs.nextUid + 1
    return uid

