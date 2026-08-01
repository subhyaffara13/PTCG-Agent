
def use_ck_conv_template(layout: Layout) -> bool:
    return _use_conv_autotune_backend("CK") and use_ck_template(layout)

