from typing import Any

def get_is_contig_ops() -> list[AHOperation]:
    def mat1_is_contig_fn(data: Any) -> bool:
        stride_0 = data["mat1_stride_0"]
        stride_1 = data["mat1_stride_1"]
        k = data["k"]
        return stride_0 == k and stride_1 == 1

    mat1_is_contig_op = AHOperation(
        "mat1_iscontig", mat1_is_contig_fn, is_categorical=True
    )

    def mat2_is_contig_fn(data: Any) -> bool:
        stride_0 = data["mat2_stride_0"]
        stride_1 = data["mat2_stride_1"]
        n = data["n"]
        return stride_0 == n and stride_1 == 1

    mat2_is_contig_op = AHOperation(
        "mat2_iscontig", mat2_is_contig_fn, is_categorical=True
    )

    return [mat1_is_contig_op, mat2_is_contig_op]

