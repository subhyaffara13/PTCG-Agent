
def hash_storage_kernel(x):
    # The randint calls are carefully written to hit things we
    # have lowerings for in inductor.  Lack of unsigned 32-bit integer
    # is a pain.
    a = torch.randint(
        -(2**31), 2**31, x.shape, device=x.device, dtype=torch.int32
    ).abs()
    a = ((a % (2**31 - 1)) + 1).long()
    b = (
        torch.randint(-(2**31), 2**31, x.shape, device=x.device, dtype=torch.int32)
        .abs()
        .long()
    )
    # This is a standard shift-multiply universal hash family
    # plus xor sum hash, using Philox to generate random numbers.
    # Our Philox RNG is not deterministic across devices so
    # don't use this for stable hashing.
    #
    # This assumes fixed length so you're also obligated to bucket
    # by the length of tensor as well
    return prims.xor_sum((a * x + b).int(), [0])

