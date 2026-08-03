import math


def _pair_uniform_to_normal(u1, u2):
    """Box-Muller transform"""
    u1 = hl.max(hl.f32(1.0e-7), u1)
    th = hl.f32(math.tau) * u2
    r = hl.sqrt(hl.f32(-2.0) * hl.log(u1))
    return r * hl.cos(th), r * hl.sin(th)

