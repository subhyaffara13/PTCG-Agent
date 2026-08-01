
def test_fill_between_interpolate_decreasing():
    p = np.array([724.3, 700, 655])
    t = np.array([9.4, 7, 2.2])
    prof = np.array([7.9, 6.6, 3.8])

    fig, ax = plt.subplots(figsize=(9, 9))

    ax.plot(t, p, 'tab:red')
    ax.plot(prof, p, 'k')

    ax.fill_betweenx(p, t, prof, where=prof < t,
                     facecolor='blue', interpolate=True, alpha=0.4)
    ax.fill_betweenx(p, t, prof, where=prof > t,
                     facecolor='red', interpolate=True, alpha=0.4)

    ax.set_xlim(0, 30)
    ax.set_ylim(800, 600)

