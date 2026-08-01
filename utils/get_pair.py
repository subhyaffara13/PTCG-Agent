
def get_pair(dictionary, n1, n2):
    if (n1, n2) in dictionary:
        return dictionary[n1, n2]
    else:
        return dictionary[n2, n1]

