
def test_identity_hashtable_get_set(key_length, length):
    # no collisions expected
    keys_vals = []
    for i in range(length):
        keys = tuple(object() for _ in range(key_length))
        keys_vals.append((keys, object()))

    ht = create_identity_hash(key_length)

    for i in range(length):
        key, value = keys_vals[i]
        assert identity_hash_set_item_default(ht, key, value) is value

    for key, value in keys_vals:
        got = identity_hash_get_item(ht, key)
        assert got is value

