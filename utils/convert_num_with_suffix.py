
def convert_num_with_suffix(number, suffix):
    index = suffixes.index(suffix)
    # Divide the number by 1000^index and format it to two decimal places
    value = f"{number / 1000 ** index:.3f}"
    # Return the value and the suffix as a string
    return value + suffixes[index]

