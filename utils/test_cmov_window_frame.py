
def test_cmov_window_frame(f, xp, step):
    # Gh 8238
    pytest.importorskip("scipy")
    df = DataFrame(
        np.array(
            [
                [12.18, 3.64],
                [10.18, 9.16],
                [13.24, 14.61],
                [4.51, 8.11],
                [6.15, 11.44],
                [9.14, 6.21],
                [11.31, 10.67],
                [2.94, 6.51],
                [9.42, 8.39],
                [12.44, 7.34],
            ]
        )
    )
    xp = DataFrame(np.array(xp))[::step]

    roll = df.rolling(5, win_type="boxcar", center=True, step=step)
    rs = getattr(roll, f)()

    tm.assert_frame_equal(xp, rs)

