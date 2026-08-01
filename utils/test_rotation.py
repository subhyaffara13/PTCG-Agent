
def test_rotation():
    a, b, g = symbols('a b g')
    j, m = symbols('j m')
    #Uncoupled
    answ = [JxKet(1,-1)/2 - sqrt(2)*JxKet(1,0)/2 + JxKet(1,1)/2 ,
       JyKet(1,-1)/2 - sqrt(2)*JyKet(1,0)/2 + JyKet(1,1)/2 ,
       JzKet(1,-1)/2 - sqrt(2)*JzKet(1,0)/2 + JzKet(1,1)/2]
    fun = [state(1, 1) for state in (JxKet, JyKet, JzKet)]
    for state in fun:
        got = qapply(Rotation(0, pi/2, 0)*state)
        assert got in answ
        answ.remove(got)
    assert not answ
    arg = Rotation(a, b, g)*fun[0]
    assert qapply(arg) == (-exp(-I*a)*exp(I*g)*cos(b)*JxKet(1,-1)/2 +
        exp(-I*a)*exp(I*g)*JxKet(1,-1)/2 - sqrt(2)*exp(-I*a)*sin(b)*JxKet(1,0)/2 +
        exp(-I*a)*exp(-I*g)*cos(b)*JxKet(1,1)/2 + exp(-I*a)*exp(-I*g)*JxKet(1,1)/2)
    #dummy effective
    assert str(qapply(Rotation(a, b, g)*JzKet(j, m), dummy=False)) == str(
        qapply(Rotation(a, b, g)*JzKet(j, m), dummy=True)).replace('_','')
    #Coupled
    ans = [JxKetCoupled(1,-1,(1,1))/2 - sqrt(2)*JxKetCoupled(1,0,(1,1))/2 +
       JxKetCoupled(1,1,(1,1))/2 ,
       JyKetCoupled(1,-1,(1,1))/2 - sqrt(2)*JyKetCoupled(1,0,(1,1))/2 +
       JyKetCoupled(1,1,(1,1))/2 ,
       JzKetCoupled(1,-1,(1,1))/2 - sqrt(2)*JzKetCoupled(1,0,(1,1))/2 +
       JzKetCoupled(1,1,(1,1))/2]
    fun = [state(1, 1, (1,1)) for state in (JxKetCoupled, JyKetCoupled, JzKetCoupled)]
    for state in fun:
        got = qapply(Rotation(0, pi/2, 0)*state)
        assert got in ans
        ans.remove(got)
    assert not ans
    arg = Rotation(a, b, g)*fun[0]
    assert qapply(arg) == (
        -exp(-I*a)*exp(I*g)*cos(b)*JxKetCoupled(1,-1,(1,1))/2 +
        exp(-I*a)*exp(I*g)*JxKetCoupled(1,-1,(1,1))/2 -
        sqrt(2)*exp(-I*a)*sin(b)*JxKetCoupled(1,0,(1,1))/2 +
        exp(-I*a)*exp(-I*g)*cos(b)*JxKetCoupled(1,1,(1,1))/2 +
        exp(-I*a)*exp(-I*g)*JxKetCoupled(1,1,(1,1))/2)
    #dummy effective
    assert str(qapply(Rotation(a,b,g)*JzKetCoupled(j,m,(j1,j2)), dummy=False)) == str(
        qapply(Rotation(a,b,g)*JzKetCoupled(j,m,(j1,j2)), dummy=True)).replace('_','')


def test_rotation():
    mpl.rcParams['text.usetex'] = True

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set(xlim=(-0.5, 5), xticks=[], ylim=(-0.5, 3), yticks=[], frame_on=False)

    text = {val: val[0] for val in ['top', 'center', 'bottom', 'left', 'right']}
    text['baseline'] = 'B'
    text['center_baseline'] = 'C'

    for i, va in enumerate(['top', 'center', 'bottom', 'baseline', 'center_baseline']):
        for j, ha in enumerate(['left', 'center', 'right']):
            for k, angle in enumerate([0, 90, 180, 270]):
                k //= 2
                x = i + k / 2
                y = j + k / 2
                ax.plot(x, y, '+', c=f'C{k}', markersize=20, markeredgewidth=0.5)
                # 'My' checks full height letters plus descenders.
                ax.text(x, y, f"$\\mathrm{{My {text[ha]}{text[va]} {angle}}}$",
                        rotation=angle, horizontalalignment=ha, verticalalignment=va)

