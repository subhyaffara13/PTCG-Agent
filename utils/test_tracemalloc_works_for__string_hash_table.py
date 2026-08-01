
def test_tracemalloc_works_for_StringHashTable():
    N = 1000
    keys = np.arange(N).astype(np.str_).astype(np.object_)
    with activated_tracemalloc():
        table = ht.StringHashTable()
        table.map_locations(keys)
        used = get_allocated_khash_memory()
        my_size = table.sizeof()
        assert used == my_size
        del table
        assert get_allocated_khash_memory() == 0

