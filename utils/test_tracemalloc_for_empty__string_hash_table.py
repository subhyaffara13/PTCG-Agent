
def test_tracemalloc_for_empty_StringHashTable():
    with activated_tracemalloc():
        table = ht.StringHashTable()
        used = get_allocated_khash_memory()
        my_size = table.sizeof()
        assert used == my_size
        del table
        assert get_allocated_khash_memory() == 0

