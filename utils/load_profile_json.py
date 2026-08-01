
def load_profile_json(profile_file):
    print(f"loading profile output {profile_file} ...")

    with open(profile_file) as opened_file:
        sess_time = json.load(opened_file)

    assert isinstance(sess_time, list)
    return sess_time

