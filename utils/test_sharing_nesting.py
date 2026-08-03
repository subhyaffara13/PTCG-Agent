from typing import Any

def test_sharing_nesting(backend: BackendType) -> None:
    eqs = ["ab,bc,cd->a", "ab,bc,cd->b", "ab,bc,cd->c", "ab,bc,cd->c"]
    views = build_views(eqs[0])
    shapes = [v.shape for v in views]
    refs: Any = weakref.WeakValueDictionary()

    def method1(views):
        with shared_intermediates():
            w = contract_expression(eqs[0], *shapes)(*views, backend=backend)
            x = contract_expression(eqs[2], *shapes)(*views, backend=backend)
            result = contract_expression("a,b->", w.shape, x.shape)(w, x, backend=backend)
            refs["w"] = w
            refs["x"] = x
            del w, x
            assert "w" in refs
            assert "x" in refs
        assert "w" not in refs, "cache leakage"
        assert "x" not in refs, "cache leakage"
        return result

    def method2(views):
        with shared_intermediates():
            y = contract_expression(eqs[2], *shapes)(*views, backend=backend)
            z = contract_expression(eqs[3], *shapes)(*views, backend=backend)
            refs["y"] = y
            refs["z"] = z
            result = contract_expression("c,d->", y.shape, z.shape)(y, z, backend=backend)
            result = result + method1(views)  # nest method1 in method2
            del y, z
            assert "y" in refs
            assert "z" in refs
        assert "y" not in refs
        assert "z" not in refs

    method1(views)
    method2(views)

