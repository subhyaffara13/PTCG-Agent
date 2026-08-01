
def test_sort_float16():
    arr = np.arange(65536, dtype=np.int16)
    temp = np.frombuffer(arr.tobytes(), dtype=np.float16)
    data = np.copy(temp)
    np.random.shuffle(data)
    data_backup = data
    assert_equal(np.sort(data, kind='quick'),
            np.sort(data_backup, kind='heap'))

