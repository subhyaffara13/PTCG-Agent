
def test_aligned_mem():
    """Check linalg works with non-aligned memory (float64)"""
    # Allocate 804 bytes of memory (allocated on boundary)
    a = arange(804, dtype=np.uint8)

    # Create an array with boundary offset 4
    z = np.frombuffer(a.data, offset=4, count=100, dtype=float)
    z = z.reshape((10, 10))

    eig(z, overwrite_a=True)
    eig(z.T, overwrite_a=True)

