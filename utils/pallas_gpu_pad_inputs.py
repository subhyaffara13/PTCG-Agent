from typing import Any

def pallas_gpu_pad_inputs(inputs: list[Any], alignment: int = 128) -> list[Any]:
    """Flatten and pad each input JAX array to a multiple of alignment."""
    import jax.numpy as jnp  # pyrefly: ignore [import-error, missing-import]

    padded = []
    for inp in inputs:
        flat = inp.flatten()
        orig_size = flat.size
        aligned_size = ((orig_size + alignment - 1) // alignment) * alignment
        if orig_size != aligned_size:
            padded.append(jnp.pad(flat, (0, aligned_size - orig_size)))
        else:
            padded.append(flat)
    return padded

