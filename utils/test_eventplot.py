
def test_eventplot():
    np.random.seed(0)

    data1 = np.random.random([32, 20]).tolist()
    data2 = np.random.random([6, 20]).tolist()
    data = data1 + data2
    num_datasets = len(data)

    colors1 = [[0, 1, .7]] * len(data1)
    colors2 = [[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1],
               [1, .75, 0],
               [1, 0, 1],
               [0, 1, 1]]
    colors = colors1 + colors2

    lineoffsets1 = 12 + np.arange(0, len(data1)) * .33
    lineoffsets2 = [-15, -3, 1, 1.5, 6, 10]
    lineoffsets = lineoffsets1.tolist() + lineoffsets2

    linelengths1 = [.33] * len(data1)
    linelengths2 = [5, 2, 1, 1, 3, 1.5]
    linelengths = linelengths1 + linelengths2

    fig = plt.figure()
    axobj = fig.add_subplot()
    colls = axobj.eventplot(data, colors=colors, lineoffsets=lineoffsets,
                            linelengths=linelengths)

    num_collections = len(colls)
    assert num_collections == num_datasets

    # Reuse testcase from above for a labeled data test
    data = {"pos": data, "c": colors, "lo": lineoffsets, "ll": linelengths}
    fig = plt.figure()
    axobj = fig.add_subplot()
    colls = axobj.eventplot("pos", colors="c", lineoffsets="lo",
                            linelengths="ll", data=data)
    num_collections = len(colls)
    assert num_collections == num_datasets

