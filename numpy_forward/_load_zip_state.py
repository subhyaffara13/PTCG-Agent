from . import collections, io, np, pickle, zipfile

def _load_zip_state(path):
    """Load state_dict from zip-archive .pt file."""
    with zipfile.ZipFile(path) as z:
        namelist = z.namelist()

        # Determine archive prefix (e.g. 'm71/' or 'ppo_actor_critic/')
        prefixes = {n.split("/")[0] for n in namelist if "/" in n}
        prefix = next(iter(prefixes)) if prefixes else ""

        pkl_data = z.read(f"{prefix}/data.pkl") if prefix else z.read("data.pkl")

        class _Unpickler(pickle.Unpickler):
            def __init__(self, *a, zf=None, zprefix="", **kw):
                super().__init__(*a, **kw)
                self.zf = zf
                self.zprefix = zprefix

            def find_class(self, module, name):
                if module == "collections" and name == "OrderedDict":
                    return collections.OrderedDict
                if module == "torch._utils":
                    if name == "_rebuild_tensor_v2":
                        return self._rebuild_tensor_v2
                    if name == "_rebuild_parameter":
                        return self._rebuild_parameter
                if module == "torch.storage" and name == "_UntypedStorage":
                    return self._UntypedStorage
                if module == "torch" and name == "FloatStorage":
                    return self._FloatStorage
                if module == "torch" and name == "Size":
                    return tuple
                if module == "builtins":
                    b = __builtins__
                    return b[name] if isinstance(b, dict) else getattr(b, name)
                raise pickle.UnpicklingError(f"Unknown module/name: {module}.{name}")

            def _UntypedStorage(self, *args, **kwargs):
                sz = args[0] if args else 0
                return np.zeros(sz, dtype=np.uint8)

            def _FloatStorage(self, *args, **kwargs):
                return None

            def _rebuild_tensor_v2(self, storage, storage_offset, size,
                                    stride, requires_grad, backward_hooks):
                if isinstance(storage, np.ndarray):
                    raw = np.frombuffer(storage.tobytes(), dtype=np.float32)
                    return raw[storage_offset:].reshape(size)
                return np.zeros(size, dtype=np.float32)

            def _rebuild_parameter(self, *args, **kwargs):
                return args[0] if args else None

            def persistent_load(self, pid):
                if isinstance(pid, tuple) and len(pid) >= 4 and pid[0] == "storage":
                    _fn, _storage_type_fn, data_id, _device, numel = pid
                    if self.zf and self.zprefix:
                        inzip = f"{self.zprefix}/data/{data_id}"
                        if inzip in self.zf.namelist():
                            raw_bytes = self.zf.read(inzip)
                            return np.frombuffer(raw_bytes, dtype=np.uint8)
                return None

        u = _Unpickler(io.BytesIO(pkl_data), zf=z, zprefix=prefix)
        return u.load()

