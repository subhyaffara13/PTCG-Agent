import random

def test_identity_hashtable_get_set_concurrent_collisions(key_length, length):
    ht = create_identity_hash(key_length)
    base_key = tuple(object() for _ in range(key_length - 1))
    keys_vals = defaultdict(list)
    for i in range(length):
        keys = base_key + (random.choice(base_key), )
        keys_vals[keys].append(object())

    set_item_results = defaultdict(set)

    def set_item(kv):
        key, values = kv
        value = random.choice(values)
        got = identity_hash_set_item_default(ht, key, value)
        set_item_results[key].add(got)

    get_item_results = defaultdict(set)

    def get_item(kv):
        key, values = kv
        got = identity_hash_get_item(ht, key)
        get_item_results[key].add(got)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for keys, values in keys_vals.items():
            futures.append(executor.submit(set_item, (keys, values)))
            futures.append(executor.submit(get_item, (keys, values)))
        for future in futures:
            future.result()

    for key in keys_vals.keys():
        assert len(set_item_results[key]) == 1
        set_item_value = set_item_results[key].pop()
        for r in get_item_results[key]:
            assert r is None or r is set_item_value

