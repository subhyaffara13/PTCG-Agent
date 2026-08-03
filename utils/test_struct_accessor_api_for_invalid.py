import re

def test_struct_accessor_api_for_invalid(invalid):
    with pytest.raises(
        AttributeError,
        match=re.escape(
            "Can only use the '.struct' accessor with 'struct[pyarrow]' dtype, "
            f"not {invalid.dtype}."
        ),
    ):
        invalid.struct

