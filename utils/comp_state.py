
def comp_state(state1, state2):
    identical = True
    if isinstance(state1, dict):
        for key in state1:
            identical &= comp_state(state1[key], state2[key])
    elif type(state1) is not type(state2):
        identical &= type(state1) is type(state2)
    elif (isinstance(state1, (list, tuple, np.ndarray)) and isinstance(
            state2, (list, tuple, np.ndarray))):
        for s1, s2 in zip(state1, state2):
            identical &= comp_state(s1, s2)
    else:
        identical &= state1 == state2
    return identical

