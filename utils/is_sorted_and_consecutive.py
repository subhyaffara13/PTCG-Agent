
def is_sorted_and_consecutive(arr: list[int]) -> bool:
    # check if the array is sorted
    if arr == sorted(arr):
        # check if the differences between adjacent elements are all 1
        return all(x[1] - x[0] == 1 for x in itertools.pairwise(arr))
    else:
        return False

