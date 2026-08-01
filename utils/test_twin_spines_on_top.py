
def test_twin_spines_on_top():
    matplotlib.rcParams['axes.linewidth'] = 48.0
    matplotlib.rcParams['lines.linewidth'] = 48.0

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    data = np.array([[1000, 1100, 1200, 1250],
                     [310, 301, 360, 400]])

    ax2 = ax1.twinx()

    ax1.plot(data[0], data[1]/1E3, color='#BEAED4')
    ax1.fill_between(data[0], data[1]/1E3, color='#BEAED4', alpha=.8)

    ax2.plot(data[0], data[1]/1E3, color='#7FC97F')
    ax2.fill_between(data[0], data[1]/1E3, color='#7FC97F', alpha=.5)

    # Reuse testcase from above for a labeled data test
    data = {"i": data[0], "j": data[1]/1E3}
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax1.plot("i", "j", color='#BEAED4', data=data)
    ax1.fill_between("i", "j", color='#BEAED4', alpha=.8, data=data)
    ax2.plot("i", "j", color='#7FC97F', data=data)
    ax2.fill_between("i", "j", color='#7FC97F', alpha=.5, data=data)

