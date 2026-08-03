import os
from typing import Any, Callable

def try_import_ck_lib() -> tuple[
    str | None, Callable[[], list[Any]], Callable[[], list[Any]], type[Any]
]:
    try:
        import ck4inductor  # type: ignore[import]
        from ck4inductor.universal_gemm.gen_instances import (  # type: ignore[import]
            gen_ops_library,
            gen_ops_preselected,
        )
        from ck4inductor.universal_gemm.op import (  # type: ignore[import]
            CKGemmOperation,
        )

        package_dirname = os.path.dirname(ck4inductor.__file__)
    except ImportError:

        def gen_ops_library() -> list[Any]:
            return []

        def gen_ops_preselected() -> list[Any]:
            return []

        class CKGemmOperation:  # type: ignore[no-redef]
            pass

        package_dirname = None
    return package_dirname, gen_ops_library, gen_ops_preselected, CKGemmOperation

