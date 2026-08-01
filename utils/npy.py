
def npy(data, lim=350.0):
    return data/((data/lim)**8+1)**(1/8.)

