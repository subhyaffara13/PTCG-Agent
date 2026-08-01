
def test_lambertw_hard():
    def check(x,y):
        y = convert(y)
        type_ok = True
        if isinstance(y, mpf):
            type_ok = isinstance(x, mpf)
        real_ok = abs(x.real-y.real) <= abs(y.real)*8*eps
        imag_ok = abs(x.imag-y.imag) <= abs(y.imag)*8*eps
        #print x, y, abs(x.real-y.real), abs(x.imag-y.imag)
        return real_ok and imag_ok
    # Evaluation near 0
    mp.dps = 15
    assert check(lambertw(1e-10), 9.999999999000000000e-11)
    assert check(lambertw(-1e-10), -1.000000000100000000e-10)
    assert check(lambertw(1e-10j), 9.999999999999999999733e-21 + 9.99999999999999999985e-11j)
    assert check(lambertw(-1e-10j), 9.999999999999999999733e-21 - 9.99999999999999999985e-11j)
    assert check(lambertw(1e-10,1), -26.303186778379041559 + 3.265093911703828397j)
    assert check(lambertw(-1e-10,1), -26.326236166739163892 + 6.526183280686333315j)
    assert check(lambertw(1e-10j,1), -26.312931726911421551 + 4.896366881798013421j)
    assert check(lambertw(-1e-10j,1), -26.297238779529035066 + 1.632807161345576513j)
    assert check(lambertw(1e-10,-1), -26.303186778379041559 - 3.265093911703828397j)
    assert check(lambertw(-1e-10,-1), -26.295238819246925694)
    assert check(lambertw(1e-10j,-1), -26.297238779529035028 - 1.6328071613455765135j)
    assert check(lambertw(-1e-10j,-1), -26.312931726911421551 - 4.896366881798013421j)
    # Test evaluation very close to the branch point -1/e
    # on the -1, 0, and 1 branches
    add = lambda x, y: fadd(x,y,exact=True)
    sub = lambda x, y: fsub(x,y,exact=True)
    addj = lambda x, y: fadd(x,fmul(y,1j,exact=True),exact=True)
    subj = lambda x, y: fadd(x,fmul(y,-1j,exact=True),exact=True)
    mp.dps = 1500
    a = -1/e + 10*eps
    d3 = mpf('1e-3')
    d10 = mpf('1e-10')
    d20 = mpf('1e-20')
    d40 = mpf('1e-40')
    d80 = mpf('1e-80')
    d300 = mpf('1e-300')
    d1000 = mpf('1e-1000')
    mp.dps = 15
    # ---- Branch 0 ----
    # -1/e + eps
    assert check(lambertw(add(a,d3)), -0.92802015005456704876)
    assert check(lambertw(add(a,d10)), -0.99997668374140088071)
    assert check(lambertw(add(a,d20)), -0.99999999976683560186)
    assert lambertw(add(a,d40)) == -1
    assert lambertw(add(a,d80)) == -1
    assert lambertw(add(a,d300)) == -1
    assert lambertw(add(a,d1000)) == -1
    # -1/e - eps
    assert check(lambertw(sub(a,d3)), -0.99819016149860989001+0.07367191188934638577j)
    assert check(lambertw(sub(a,d10)), -0.9999999998187812114595992+0.0000233164398140346109194j)
    assert check(lambertw(sub(a,d20)), -0.99999999999999999998187+2.331643981597124203344e-10j)
    assert check(lambertw(sub(a,d40)), -1.0+2.33164398159712420336e-20j)
    assert check(lambertw(sub(a,d80)), -1.0+2.33164398159712420336e-40j)
    assert check(lambertw(sub(a,d300)), -1.0+2.33164398159712420336e-150j)
    assert check(lambertw(sub(a,d1000)), mpc(-1,'2.33164398159712420336e-500'))
    # -1/e + eps*j
    assert check(lambertw(addj(a,d3)), -0.94790387486938526634+0.05036819639190132490j)
    assert check(lambertw(addj(a,d10)), -0.9999835127872943680999899+0.0000164870314895821225256j)
    assert check(lambertw(addj(a,d20)), -0.999999999835127872929987+1.64872127051890935830e-10j)
    assert check(lambertw(addj(a,d40)), -0.9999999999999999999835+1.6487212707001281468305e-20j)
    assert check(lambertw(addj(a,d80)), -1.0 + 1.64872127070012814684865e-40j)
    assert check(lambertw(addj(a,d300)), -1.0 + 1.64872127070012814684865e-150j)
    assert check(lambertw(addj(a,d1000)), mpc(-1.0,'1.64872127070012814684865e-500'))
    # -1/e - eps*j
    assert check(lambertw(subj(a,d3)), -0.94790387486938526634-0.05036819639190132490j)
    assert check(lambertw(subj(a,d10)), -0.9999835127872943680999899-0.0000164870314895821225256j)
    assert check(lambertw(subj(a,d20)), -0.999999999835127872929987-1.64872127051890935830e-10j)
    assert check(lambertw(subj(a,d40)), -0.9999999999999999999835-1.6487212707001281468305e-20j)
    assert check(lambertw(subj(a,d80)), -1.0 - 1.64872127070012814684865e-40j)
    assert check(lambertw(subj(a,d300)), -1.0 - 1.64872127070012814684865e-150j)
    assert check(lambertw(subj(a,d1000)), mpc(-1.0,'-1.64872127070012814684865e-500'))
    # ---- Branch 1 ----
    assert check(lambertw(addj(a,d3),1), -3.088501303219933378005990 + 7.458676867597474813950098j)
    assert check(lambertw(addj(a,d80),1), -3.088843015613043855957087 + 7.461489285654254556906117j)
    assert check(lambertw(addj(a,d300),1), -3.088843015613043855957087 + 7.461489285654254556906117j)
    assert check(lambertw(addj(a,d1000),1), -3.088843015613043855957087 + 7.461489285654254556906117j)
    assert check(lambertw(subj(a,d3),1), -1.0520914180450129534365906 + 0.0539925638125450525673175j)
    assert check(lambertw(subj(a,d10),1), -1.0000164872127056318529390 + 0.000016487393927159250398333077j)
    assert check(lambertw(subj(a,d20),1), -1.0000000001648721270700128 + 1.64872127088134693542628e-10j)
    assert check(lambertw(subj(a,d40),1), -1.000000000000000000016487 + 1.64872127070012814686677e-20j)
    assert check(lambertw(subj(a,d80),1), -1.0 + 1.64872127070012814684865e-40j)
    assert check(lambertw(subj(a,d300),1), -1.0 + 1.64872127070012814684865e-150j)
    assert check(lambertw(subj(a,d1000),1), mpc(-1.0, '1.64872127070012814684865e-500'))
    # ---- Branch -1 ----
    # -1/e + eps
    assert check(lambertw(add(a,d3),-1), -1.075608941186624989414945)
    assert check(lambertw(add(a,d10),-1), -1.000023316621036696460620)
    assert check(lambertw(add(a,d20),-1), -1.000000000233164398177834)
    assert lambertw(add(a,d40),-1) == -1
    assert lambertw(add(a,d80),-1) == -1
    assert lambertw(add(a,d300),-1) == -1
    assert lambertw(add(a,d1000),-1) == -1
    # -1/e - eps
    assert check(lambertw(sub(a,d3),-1), -0.99819016149860989001-0.07367191188934638577j)
    assert check(lambertw(sub(a,d10),-1), -0.9999999998187812114595992-0.0000233164398140346109194j)
    assert check(lambertw(sub(a,d20),-1), -0.99999999999999999998187-2.331643981597124203344e-10j)
    assert check(lambertw(sub(a,d40),-1), -1.0-2.33164398159712420336e-20j)
    assert check(lambertw(sub(a,d80),-1), -1.0-2.33164398159712420336e-40j)
    assert check(lambertw(sub(a,d300),-1), -1.0-2.33164398159712420336e-150j)
    assert check(lambertw(sub(a,d1000),-1), mpc(-1,'-2.33164398159712420336e-500'))
    # -1/e + eps*j
    assert check(lambertw(addj(a,d3),-1), -1.0520914180450129534365906 - 0.0539925638125450525673175j)
    assert check(lambertw(addj(a,d10),-1), -1.0000164872127056318529390 - 0.0000164873939271592503983j)
    assert check(lambertw(addj(a,d20),-1), -1.0000000001648721270700 - 1.64872127088134693542628e-10j)
    assert check(lambertw(addj(a,d40),-1), -1.00000000000000000001648 - 1.6487212707001281468667726e-20j)
    assert check(lambertw(addj(a,d80),-1), -1.0 - 1.64872127070012814684865e-40j)
    assert check(lambertw(addj(a,d300),-1), -1.0 - 1.64872127070012814684865e-150j)
    assert check(lambertw(addj(a,d1000),-1), mpc(-1.0,'-1.64872127070012814684865e-500'))
    # -1/e - eps*j
    assert check(lambertw(subj(a,d3),-1), -3.088501303219933378005990-7.458676867597474813950098j)
    assert check(lambertw(subj(a,d10),-1), -3.088843015579260686911033-7.461489285372968780020716j)
    assert check(lambertw(subj(a,d20),-1), -3.088843015613043855953708-7.461489285654254556877988j)
    assert check(lambertw(subj(a,d40),-1), -3.088843015613043855957087-7.461489285654254556906117j)
    assert check(lambertw(subj(a,d80),-1), -3.088843015613043855957087 - 7.461489285654254556906117j)
    assert check(lambertw(subj(a,d300),-1), -3.088843015613043855957087 - 7.461489285654254556906117j)
    assert check(lambertw(subj(a,d1000),-1), -3.088843015613043855957087 - 7.461489285654254556906117j)
    # One more case, testing higher precision
    mp.dps = 500
    x = -1/e + mpf('1e-13')
    ans = "-0.99999926266961377166355784455394913638782494543377383"\
    "744978844374498153493943725364881490261187530235150668593869563"\
    "168276697689459394902153960200361935311512317183678882"
    mp.dps = 15
    assert lambertw(x).ae(ans)
    mp.dps = 50
    assert lambertw(x).ae(ans)
    mp.dps = 150
    assert lambertw(x).ae(ans)

