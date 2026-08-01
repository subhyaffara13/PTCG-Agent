
def test_aligned_mem_complex():
    """Check that complex objects don't need to be completely aligned"""
    # Allocate 1608 bytes of memory (allocated on boundary)
    a = zeros(1608, dtype=np.uint8)

    # Create an array with boundary offset 8
    z = np.frombuffer(a.data, offset=8, count=100, dtype=complex)
    z = z.reshape((10, 10))

    eig(z, overwrite_a=True)
    # This does not need special handling
    eig(z.T, overwrite_a=True)

