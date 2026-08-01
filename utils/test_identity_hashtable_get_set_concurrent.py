
def test_identity_hashtable_get_set_concurrent(key_length, length):
    ht = create_identity_hash(key_length)
    keys_vals = []
    for i in range(length):
        keys = tuple(object() for _ in range(key_length))
        keys_vals.append((keys, object()))

    def set_item(kv):
        key, value = kv
        got = identity_hash_set_item_default(ht, key, value)
        assert got is value

    def get_item(kv):
        key, value = kv
        got = identity_hash_get_item(ht, key)
        assert got is None or got is value

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for kv in keys_vals:
            futures.append(executor.submit(set_item, kv))
            futures.append(executor.submit(get_item, kv))
        for future in futures:
            future.result()

