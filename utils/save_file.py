
def save_file(pickler, obj):
    logger.trace(pickler, "Fi: %s", obj)
    f = _save_file(pickler, obj, open)
    logger.trace(pickler, "# Fi")
    return f


def save_file(
    tensors: Dict[str, Array],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, Array]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.flax import save_file
    from jax import numpy as jnp

    tensors = {"embedding": jnp.zeros((512, 1024)), "attention": jnp.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    np_tensors = _jnp2np(tensors)
    return numpy.save_file(np_tensors, filename, metadata=metadata)


def save_file(
    tensors: Dict[str, mx.array],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, mx.array]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.mlx import save_file
    import mlx.core as mx

    tensors = {"embedding": mx.zeros((512, 1024)), "attention": mx.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    np_tensors = _mx2np(tensors)
    return numpy.save_file(np_tensors, filename, metadata=metadata)


def save_file(
    tensor_dict: Dict[str, np.ndarray],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensor_dict (`Dict[str, np.ndarray]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.numpy import save_file
    import numpy as np

    tensors = {"embedding": np.zeros((512, 1024)), "attention": np.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    keep_alive_buffer = []  # to keep byteswapped tensors alive
    serialize_file(
        _flatten(tensor_dict, keep_alive_buffer), filename, metadata=metadata
    )


def save_file(
    tensors: Dict[str, paddle.Tensor],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, paddle.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.paddle import save_file
    import paddle

    tensors = {"embedding": paddle.zeros((512, 1024)), "attention": paddle.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    keep_references_alive = []
    serialize_file(
        _flatten(tensors, keep_references_alive), filename, metadata=metadata
    )


def save_file(
    tensors: Dict[str, tf.Tensor],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, tf.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.tensorflow import save_file
    import tensorflow as tf

    tensors = {"embedding": tf.zeros((512, 1024)), "attention": tf.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    np_tensors = _tf2np(tensors)
    return numpy.save_file(np_tensors, filename, metadata=metadata)


def save_file(
    tensors: Dict[str, torch.Tensor],
    filename: Union[str, os.PathLike],
    metadata: Optional[Dict[str, str]] = None,
):
    """
    Saves a dictionary of tensors into `filename` in safetensors format.
    There is no mechanism in place to prevent the caller from modifying the data while a file save occurs,
    please be wary when calling `save_file` and modifying tensors referenced in the `tensors` dict concurrently;
    it may lead to corrupted files.

    Args:
        tensors (`Dict[str, torch.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        filename (`str`, or `os.PathLike`)):
            The filename we're saving into.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `None`

    Example:

    ```python
    from safetensors.torch import save_file
    import torch

    tensors = {"embedding": torch.zeros((512, 1024)), "attention": torch.zeros((256, 256))}
    save_file(tensors, "model.safetensors")
    ```
    """
    keep_references_alive = []  # to avoid garbage collection of temporary numpy arrays while we write to disk
    serialize_file(
        _flatten_as_ptr(tensors, keep_references_alive), filename, metadata=metadata
    )

