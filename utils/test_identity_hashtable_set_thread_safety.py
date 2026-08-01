
def test_identity_hashtable_set_thread_safety(key_length):
    ht = create_identity_hash(key_length)

    key = tuple(object() for _ in range(key_length))
    val1 = object()

    def thread_func(val):
        return identity_hash_set_item_default(ht, key, val)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(thread_func, val1) for _ in range(100)]
        results = [f.result() for f in futures]

    assert all(r is val1 for r in results)

