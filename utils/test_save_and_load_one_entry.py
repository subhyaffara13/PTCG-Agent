
def test_save_and_load_one_entry():
    dense_matrix = np.zeros((4,6))
    dense_matrix[1,2] = 1
    _check_save_and_load(dense_matrix)

