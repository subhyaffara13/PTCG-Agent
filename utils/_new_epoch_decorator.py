import functools

def _new_epoch_decorator(thefunc):
    @functools.wraps(thefunc)
    def wrapper():
        mdates._reset_epoch_test_example()
        mdates.set_epoch('2000-01-01')
        thefunc()
        mdates._reset_epoch_test_example()
    return wrapper

