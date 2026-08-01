
def restore_singleton_bitgen():
    """Ensures that the singleton bitgen is restored after a test"""
    orig_bitgen = np.random.get_bit_generator()
    yield
    np.random.set_bit_generator(orig_bitgen)

