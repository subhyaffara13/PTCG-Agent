
def _binary_op(f_real, f_complex):
    def g_complex(ctx, sval, tval):
        return ctx.make_mpc(f_complex(sval, tval, ctx.prec))
    def g_real(ctx, sval, tval):
        try:
            return ctx.make_mpf(f_real(sval, tval, ctx.prec))
        except ComplexResult:
            sval = (sval, mpi_zero)
            tval = (tval, mpi_zero)
            return g_complex(ctx, sval, tval)
    def lop_real(s, t):
        if isinstance(t, _matrix): return NotImplemented
        ctx = s.ctx
        if not isinstance(t, ctx._types): t = ctx.convert(t)
        if hasattr(t, "_mpi_"): return g_real(ctx, s._mpi_, t._mpi_)
        if hasattr(t, "_mpci_"): return g_complex(ctx, (s._mpi_, mpi_zero), t._mpci_)
        return NotImplemented
    def rop_real(s, t):
        ctx = s.ctx
        if not isinstance(t, ctx._types): t = ctx.convert(t)
        if hasattr(t, "_mpi_"): return g_real(ctx, t._mpi_, s._mpi_)
        if hasattr(t, "_mpci_"): return g_complex(ctx, t._mpci_, (s._mpi_, mpi_zero))
        return NotImplemented
    def lop_complex(s, t):
        if isinstance(t, _matrix): return NotImplemented
        ctx = s.ctx
        if not isinstance(t, s.ctx._types):
            try:
                t = s.ctx.convert(t)
            except (ValueError, TypeError):
                return NotImplemented
        return g_complex(ctx, s._mpci_, t._mpci_)
    def rop_complex(s, t):
        ctx = s.ctx
        if not isinstance(t, s.ctx._types):
            t = s.ctx.convert(t)
        return g_complex(ctx, t._mpci_, s._mpci_)
    return lop_real, rop_real, lop_complex, rop_complex

