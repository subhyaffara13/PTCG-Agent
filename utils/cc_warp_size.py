
def cc_warp_size(cc: str | int) -> int:
    if torch.version.hip:
        if "gfx9" in str(cc):
            return 64
        else:
            return 32
    else:
        return 32

