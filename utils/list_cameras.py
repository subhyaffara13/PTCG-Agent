
def list_cameras():
    """ """
    index = 0
    device_idx = []
    failed = 0

    # Sometimes there are gaps between the device index.
    # We keep trying max_gaps times.
    max_gaps = 3

    while failed < max_gaps:
        vcap = cv2.VideoCapture(index)
        if not vcap.read()[0]:
            failed += 1
        else:
            device_idx.append(index)
        vcap.release()
        index += 1
    return device_idx


def list_cameras():
    """Always only lists one camera.

    Functionality not supported in videocapture module.
    """
    return [0]

