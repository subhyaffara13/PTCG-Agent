from . import collections, io, np, pickle

def _load_pickle_state(raw):
    """Load state_dict from old-format pickled checkpoint."""
    class _Unpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == "collections" and name == "OrderedDict":
                return collections.OrderedDict
            if module == "torch._utils":
                if name == "_rebuild_tensor_v2":
                    return self._rebuild_tensor_v2
                if name == "_rebuild_parameter":
                    return self._rebuild_parameter
            if module in ("torch", "torch.storage"):
                if name in ("FloatStorage", "_UntypedStorage"):
                    return self._UntypedStorage
            if module == "torch" and name == "Size":
                return tuple
            if module == "builtins":
                b = __builtins__
                return b[name] if isinstance(b, dict) else getattr(b, name)
            raise pickle.UnpicklingError(f"Unknown {module}.{name}")

        def _UntypedStorage(self, *args, **kwargs):
            sz = args[0] if args else 0
            return np.zeros(sz, dtype=np.uint8)

        def _rebuild_tensor_v2(self, storage, storage_offset, size,
                                stride, requires_grad, backward_hooks):
            if isinstance(storage, np.ndarray):
                raw = np.frombuffer(storage.tobytes(), dtype=np.float32)
                return raw[storage_offset:].reshape(size)
            return np.zeros(size, dtype=np.float32)

        def _rebuild_parameter(self, *args, **kwargs):
            return args[0] if args else None

    return _Unpickler(io.BytesIO(raw)).load()

def relu(x):
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def linear(x, weight, bias):
    return x @ weight.T + bias

