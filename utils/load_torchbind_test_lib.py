
def load_torchbind_test_lib():
    import unittest

    from torch.testing._internal.common_utils import (  # type: ignore[attr-defined]
        find_library_location,
        IS_FBCODE,
        IS_MACOS,
        IS_SANDCASTLE,
        IS_WINDOWS,
    )

    if IS_MACOS:
        raise unittest.SkipTest("non-portable load_library call used in test")
    elif IS_SANDCASTLE or IS_FBCODE:
        lib_file_path = Path("//caffe2/test/cpp/jit:test_custom_class_registrations")
    elif IS_WINDOWS:
        lib_file_path = find_library_location("torchbind_test.dll")
    else:
        lib_file_path = find_library_location("libtorchbind_test.so")
    torch.ops.load_library(str(lib_file_path))

