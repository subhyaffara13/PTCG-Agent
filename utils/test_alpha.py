
def test_alpha():
    # Test data for the alpha_k. See DLMF 8.12.14.
    with mp.workdps(30):
        alpha = [mp.mpf(0), mp.mpf(1), mp.mpf(1)/3, mp.mpf(1)/36,
                 -mp.mpf(1)/270, mp.mpf(1)/4320, mp.mpf(1)/17010,
                 -mp.mpf(139)/5443200, mp.mpf(1)/204120]
        mp_assert_allclose(compute_alpha(9), alpha)


def test_alpha():
    np.random.seed(0)
    data = np.random.random(50)

    fig, ax = plt.subplots()

    # alpha=.5 markers, solid line
    ax.plot(data, '-D', color=[1, 0, 0], mfc=[1, 0, 0, .5],
            markersize=20, lw=10)

    # everything solid by kwarg
    ax.plot(data + 2, '-D', color=[1, 0, 0, .5], mfc=[1, 0, 0, .5],
            markersize=20, lw=10,
            alpha=1)

    # everything alpha=.5 by kwarg
    ax.plot(data + 4, '-D', color=[1, 0, 0], mfc=[1, 0, 0],
            markersize=20, lw=10,
            alpha=.5)

    # everything alpha=.5 by colors
    ax.plot(data + 6, '-D', color=[1, 0, 0, .5], mfc=[1, 0, 0, .5],
            markersize=20, lw=10)

    # alpha=.5 line, solid markers
    ax.plot(data + 8, '-D', color=[1, 0, 0, .5], mfc=[1, 0, 0],
            markersize=20, lw=10)


def test_alpha():
    # We want an image which has a background color and an alpha of 0.4.
    fig = plt.figure(figsize=[2, 1])
    fig.set_facecolor((0, 1, 0.4))
    fig.patch.set_alpha(0.4)
    fig.patches.append(mpl.patches.CirclePolygon(
        [20, 20], radius=15, alpha=0.6, facecolor='red'))

