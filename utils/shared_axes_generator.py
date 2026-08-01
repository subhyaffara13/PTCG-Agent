
def shared_axes_generator(request):
    # test all of the ways to get fig/ax sets
    if request.param == 'gca':
        fig = plt.figure()
        ax = fig.gca()
    elif request.param == 'subplots':
        fig, ax = plt.subplots()
    elif request.param == 'subplots_shared':
        fig, ax_lst = plt.subplots(2, 2, sharex='all', sharey='all')
        ax = ax_lst[0][0]
    elif request.param == 'add_axes':
        fig = plt.figure()
        ax = fig.add_axes((.1, .1, .8, .8))
    return fig, ax

