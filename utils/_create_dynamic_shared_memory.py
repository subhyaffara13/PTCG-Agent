
def _create_dynamic_shared_memory(space: Graph | Sequence, n: int = 1, ctx=mp):
    raise TypeError(
        f"As {space} has a dynamic shape so its not possible to make a static shared memory. For `AsyncVectorEnv`, disable `shared_memory`."
    )

