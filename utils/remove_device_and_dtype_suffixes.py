
def remove_device_and_dtype_suffixes(test_name: str) -> str:
    # import statement is localized to avoid circular dependency issues with common_device_type.py
    from torch.testing._internal.common_device_type import get_device_type_test_bases
    device_suffixes = [x.device_type for x in get_device_type_test_bases()]
    dtype_suffixes = [str(dt)[len("torch."):] for dt in get_all_dtypes()]

    test_name_chunks = test_name.split("_")
    if len(test_name_chunks) > 0 and test_name_chunks[-1] in dtype_suffixes:
        if len(test_name_chunks) > 1 and test_name_chunks[-2] in device_suffixes:
            return "_".join(test_name_chunks[0:-2])
        return "_".join(test_name_chunks[0:-1])
    return test_name

