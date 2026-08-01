
def my_container_sum(a):
    result = a[0]
    for tensor in a[1:]:
        result += tensor
    return result

