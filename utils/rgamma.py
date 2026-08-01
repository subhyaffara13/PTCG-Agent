
def rgamma(x):
    try:
        return 1./gamma(x)
    except ZeroDivisionError:
        return x*0.0

