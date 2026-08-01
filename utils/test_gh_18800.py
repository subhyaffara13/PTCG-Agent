
def test_gh_18800(incantation):
    # our prohibition on non-finite values
    # in kd-tree workflows means we need
    # coercion to NumPy arrays enforced

    class ArrLike(np.ndarray):
        def __new__(cls, input_array):
            obj = np.asarray(input_array).view(cls)
            # we override all() to mimic the problem
            # pandas DataFrames encountered in gh-18800
            obj.all = None
            return obj

        def __array_finalize__(self, obj):
            if obj is None:
                return
            self.all = getattr(obj, 'all', None)

    points = [
        [66.22, 32.54],
        [22.52, 22.39],
        [31.01, 81.21],
        ]
    arr = np.array(points)
    arr_like = ArrLike(arr)
    tree = incantation(points, 10)
    tree.query(arr_like, 1)
    tree.query_ball_point(arr_like, 200)

