
def l_or(*f):
    l1, l2 = 'lambda v', []
    for i in range(len(f)):
        l1 = f'{l1},f{i}=f[{i}]'
        l2.append(f'f{i}(v)')
    return eval(f"{l1}:{' or '.join(l2)}")

