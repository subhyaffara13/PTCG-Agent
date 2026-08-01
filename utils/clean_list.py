
def clean_list(arr, remove_all_strings=True):
    if remove_all_strings:
        # Remove all empty strings in list
        return list(filter(lambda elm: elm != "", arr))

    # Remove empty strings at end of list
    while len(arr) > 0:
        if arr[-1] == "":
            arr.pop()
        else:
            break
    return arr

