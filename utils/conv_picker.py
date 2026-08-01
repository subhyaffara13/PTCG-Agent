
def conv_picker(func, conv1dOpt, conv2dOpt, conv3dOpt):
    if func is F.conv1d:
        return conv1dOpt
    if func is F.conv2d:
        return conv2dOpt
    else:
        if func is not F.conv3d:
            raise AssertionError(
                f"Expected func to be F.conv1d, F.conv2d, or F.conv3d, got {func}"
            )
        return conv3dOpt

