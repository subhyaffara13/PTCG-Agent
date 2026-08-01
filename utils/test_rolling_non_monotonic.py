
def test_rolling_non_monotonic(method, expected):
    """
    Make sure the (rare) branch of non-monotonic indices is covered by a test.

    output from 1.1.3 is assumed to be the expected output. Output of sum/mean has
    manually been verified.

    GH 36933.
    """
    # Based on an example found in computation.rst
    use_expanding = [True, False, True, False, True, True, True, True]
    df = DataFrame({"values": np.arange(len(use_expanding)) ** 2})

    class CustomIndexer(BaseIndexer):
        def get_window_bounds(self, num_values, min_periods, center, closed, step):
            start = np.empty(num_values, dtype=np.int64)
            end = np.empty(num_values, dtype=np.int64)
            for i in range(num_values):
                if self.use_expanding[i]:
                    start[i] = 0
                    end[i] = i + 1
                else:
                    start[i] = i
                    end[i] = i + self.window_size
            return start, end

    indexer = CustomIndexer(window_size=4, use_expanding=use_expanding)

    result = getattr(df.rolling(indexer), method)()
    expected = DataFrame({"values": expected})
    tm.assert_frame_equal(result, expected)

