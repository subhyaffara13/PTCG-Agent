
def test_identity_hashtable_default_thread_safety(key_length):
    ht = create_identity_hash(key_length)

    key = tuple(object() for _ in range(key_length))
    val1 = object()
    val2 = object()

    got1 = identity_hash_set_item_default(ht, key, val1)
    assert got1 is val1

    def thread_func(val):
        return identity_hash_set_item_default(ht, key, val)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(thread_func, val2) for _ in range(8)]
        results = [f.result() for f in futures]

    assert all(r is val1 for r in results)

