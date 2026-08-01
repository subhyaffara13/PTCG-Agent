
def moderatex(x):
    '''
    This function moderates a decision variable. It replaces NaN by 0 and Inf/-Inf by
    REALMAX/-REALMAX.
    '''
    x[np.isnan(x)] = 0
    x = np.clip(x, -REALMAX, REALMAX)
    return x

