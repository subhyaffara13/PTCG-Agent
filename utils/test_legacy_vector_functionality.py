
def test_legacy_vector_functionality():
    def _padwithtens(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = 10
        vector[-pad_width[1]:] = 10

    a = np.arange(6).reshape(2, 3)
    a = np.pad(a, 2, _padwithtens)
    b = np.array(
        [[10, 10, 10, 10, 10, 10, 10],
         [10, 10, 10, 10, 10, 10, 10],

         [10, 10,  0,  1,  2, 10, 10],
         [10, 10,  3,  4,  5, 10, 10],

         [10, 10, 10, 10, 10, 10, 10],
         [10, 10, 10, 10, 10, 10, 10]]
        )
    assert_array_equal(a, b)

