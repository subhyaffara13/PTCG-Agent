import sys

def test_jumped(config):
    # Each config contains the initial seed, a number of raw steps
    # the sha256 hashes of the initial and the final states' keys and
    # the position of the initial and the final state.
    # These were produced using the original C implementation.
    seed = config["seed"]
    steps = config["steps"]

    mt19937 = MT19937(seed)
    # Burn step
    mt19937.random_raw(steps)
    key = mt19937.state["state"]["key"]
    if sys.byteorder == 'big':
        key = key.byteswap()
    sha256 = hashlib.sha256(key)
    assert mt19937.state["state"]["pos"] == config["initial"]["pos"]
    assert sha256.hexdigest() == config["initial"]["key_sha256"]

    jumped = mt19937.jumped()
    key = jumped.state["state"]["key"]
    if sys.byteorder == 'big':
        key = key.byteswap()
    sha256 = hashlib.sha256(key)
    assert jumped.state["state"]["pos"] == config["jumped"]["pos"]
    assert sha256.hexdigest() == config["jumped"]["key_sha256"]

