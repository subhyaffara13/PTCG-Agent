
def test_indexer_quantile_sum(end_value, values, func, args):
    # GH 37153
    class CustomIndexer(BaseIndexer):
        def get_window_bounds(self, num_values, min_periods, center, closed, step):
            start = np.empty(num_values, dtype=np.int64)
            end = np.empty(num_values, dtype=np.int64)
            for i in range(num_values):
                if self.use_expanding[i]:
                    start[i] = 0
                    end[i] = max(i + end_value, 1)
                else:
                    start[i] = i
                    end[i] = i + self.window_size
            return start, end

    use_expanding = [True, False, True, False, True]
    df = DataFrame({"values": range(5)})

    indexer = CustomIndexer(window_size=1, use_expanding=use_expanding)
    result = getattr(df.rolling(indexer), func)(*args)
    expected = DataFrame({"values": values})
    tm.assert_frame_equal(result, expected)

