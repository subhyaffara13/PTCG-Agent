
def create_mock_pg(prefix_store, rank, world_size, timeout):
    return MockProcessGroup(rank, world_size)

