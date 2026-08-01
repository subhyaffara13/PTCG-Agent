
def myTakeStep2(x):
    """redo RandomDisplacement in function form without the attribute stepsize
    to make sure everything still works ok
    """
    s = 0.5
    x += np.random.uniform(-s, s, np.shape(x))
    return x

