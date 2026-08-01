
def test_identity_hashtable_get_thread_safety(key_length):
    ht = create_identity_hash(key_length)
    key = tuple(object() for _ in range(key_length))
    value = object()
    identity_hash_set_item_default(ht, key, value)

    def thread_func():
        return identity_hash_get_item(ht, key)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(thread_func) for _ in range(100)]
        results = [f.result() for f in futures]

    assert all(r is value for r in results)

