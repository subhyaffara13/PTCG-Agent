
def skip_if_odd_worldsize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (os.environ["BACKEND"] != "mpi") and int(os.environ["WORLD_SIZE"]) % 2 == 1:
            sys.exit(TEST_SKIPS["odd_worldsize"].exit_code)

        return func(*args, **kwargs)

    return wrapper

