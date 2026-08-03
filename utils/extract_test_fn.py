from typing import Callable

def extract_test_fn() -> Callable | None:
    try:
        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            if "self" not in frame.f_locals:
                continue
            self_val = frame.f_locals["self"]
            if isinstance(self_val, unittest.TestCase):
                test_id = self_val.id()
                *_, cls_name, test_name = test_id.rsplit('.', 2)
                if cls_name == type(self_val).__name__ and test_name.startswith("test"):
                    test_fn = getattr(self_val, test_name).__func__
                    return test_fn
    except Exception:
        pass
    return None

