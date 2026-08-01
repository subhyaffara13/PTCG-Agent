
def test_aligned_mem_float():
    """Check linalg works with non-aligned memory (float32)"""
    # Allocate 402 bytes of memory (allocated on boundary)
    a = arange(402, dtype=np.uint8)

    # Create an array with boundary offset 4
    z = np.frombuffer(a.data, offset=2, count=100, dtype=float32)
    z = z.reshape((10, 10))

    eig(z, overwrite_a=True)
    eig(z.T, overwrite_a=True)

