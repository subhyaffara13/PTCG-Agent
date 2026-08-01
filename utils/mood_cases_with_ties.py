
def mood_cases_with_ties():
    # Generate random `x` and `y` arrays with ties both between and within the
    # samples. Expected results are (statistic, pvalue) from SAS.
    expected_results = [(-1.76658511464992, .0386488678399305),
                        (-.694031428192304, .2438312498647250),
                        (-1.15093525352151, .1248794365836150)]
    seeds = [23453254, 1298352315, 987234597]
    for si, seed in enumerate(seeds):
        rng = np.random.default_rng(seed)
        xy = rng.random(100)
        # Generate random indices to make ties
        tie_ind = rng.integers(low=0, high=99, size=5)
        # Generate a random number of ties for each index.
        num_ties_per_ind = rng.integers(low=1, high=5, size=5)
        # At each `tie_ind`, mark the next `n` indices equal to that value.
        for i, n in zip(tie_ind, num_ties_per_ind):
            for j in range(i + 1, i + n):
                xy[j] = xy[i]
        # scramble order of xy before splitting into `x, y`
        rng.shuffle(xy)
        x, y = np.split(xy, 2)
        yield x, y, 'less', *expected_results[si]

