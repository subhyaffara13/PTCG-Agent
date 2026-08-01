
def index_large():
    # large values used in TestUInt64Index where no compat needed with int64/float64
    large = [2**63, 2**63 + 10, 2**63 + 15, 2**63 + 20, 2**63 + 25]
    return Index(large, dtype=np.uint64)

