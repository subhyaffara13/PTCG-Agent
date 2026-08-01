
def set_fusion_group_inlining(inlining):
    old = torch._C._debug_get_fusion_group_inlining()
    torch._C._debug_set_fusion_group_inlining(inlining)
    try:
        yield
    finally:
        torch._C._debug_set_fusion_group_inlining(old)

