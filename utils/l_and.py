
def l_and(*f):
    l1, l2 = 'lambda v', []
    for i in range(len(f)):
        l1 = f'{l1},f{i}=f[{i}]'
        l2.append(f'f{i}(v)')
    return eval(f"{l1}:{' and '.join(l2)}")

