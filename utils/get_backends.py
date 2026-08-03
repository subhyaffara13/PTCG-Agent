import os
import sys

def get_backends():
    possible_backends = []

    if sys.platform == "win32":
        version_code = platform.win32_ver()[0].split(".")[0]
        if "Server" in version_code:
            version_code = ''.join(filter(str.isdigit, version_code))[:4]
            minimum_satisfied = int(version_code) >= 2012
        else:
            minimum_satisfied = int(version_code) >= 8

        if minimum_satisfied:
            try:
                # If cv2 is installed, prefer that on windows.
                import cv2

                possible_backends.append("OpenCV")
            except ImportError:
                possible_backends.append("_camera (MSMF)")

    if "linux" in sys.platform:
        possible_backends.append("_camera (V4L2)")

    if "darwin" in sys.platform:
        possible_backends.append("OpenCV-Mac")

    if "OpenCV" not in possible_backends:
        possible_backends.append("OpenCV")

    if sys.platform == "win32":
        possible_backends.append("VideoCapture")

    # see if we have any user specified defaults in environments.
    camera_env = os.environ.get("PYGAME_CAMERA", "").lower()
    if camera_env == "opencv":  # prioritize opencv
        if "OpenCV" in possible_backends:
            possible_backends.remove("OpenCV")
        possible_backends = ["OpenCV"] + possible_backends

    if camera_env in ("vidcapture", "videocapture"):  # prioritize vidcapture
        if "VideoCapture" in possible_backends:
            possible_backends.remove("VideoCapture")
        possible_backends = ["VideoCapture"] + possible_backends

    return possible_backends

