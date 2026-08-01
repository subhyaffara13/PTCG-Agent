
def ratioize(list, N):
    if list[0] > N:
        return S.Zero
    if len(list) == 1:
        return list[0]
    return list[0] + ratioize(list[1:], N)

