
def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two versions.

    :return: -1 if version1 > version2
             0 if both versions are equal
             1 if version1 < version2
    """

    num_versions1 = list(map(int, version1.split(".")))
    num_versions2 = list(map(int, version2.split(".")))

    if len(num_versions1) > len(num_versions2):
        diff = len(num_versions1) - len(num_versions2)
        for _ in range(diff):
            num_versions2.append(0)
    elif len(num_versions1) < len(num_versions2):
        diff = len(num_versions2) - len(num_versions1)
        for _ in range(diff):
            num_versions1.append(0)

    for i, ver in enumerate(num_versions1):
        if num_versions1[i] > num_versions2[i]:
            return -1
        elif num_versions1[i] < num_versions2[i]:
            return 1

    return 0

