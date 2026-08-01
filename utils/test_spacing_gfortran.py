
def test_spacing_gfortran():
    # Reference from this fortran file, built with gfortran 4.3.3 on linux
    # 32bits:
    #       PROGRAM test_spacing
    #        INTEGER, PARAMETER :: SGL = SELECTED_REAL_KIND(p=6, r=37)
    #        INTEGER, PARAMETER :: DBL = SELECTED_REAL_KIND(p=13, r=200)
    #
    #        WRITE(*,*) spacing(0.00001_DBL)
    #        WRITE(*,*) spacing(1.0_DBL)
    #        WRITE(*,*) spacing(1000._DBL)
    #        WRITE(*,*) spacing(10500._DBL)
    #
    #        WRITE(*,*) spacing(0.00001_SGL)
    #        WRITE(*,*) spacing(1.0_SGL)
    #        WRITE(*,*) spacing(1000._SGL)
    #        WRITE(*,*) spacing(10500._SGL)
    #       END PROGRAM
    ref = {np.float64: [1.69406589450860068E-021,
                        2.22044604925031308E-016,
                        1.13686837721616030E-013,
                        1.81898940354585648E-012],
           np.float32: [9.09494702E-13,
                        1.19209290E-07,
                        6.10351563E-05,
                        9.76562500E-04]}

    for dt, dec_ in zip([np.float32, np.float64], (10, 20)):
        x = np.array([1e-5, 1, 1000, 10500], dtype=dt)
        assert_array_almost_equal(np.spacing(x), ref[dt], decimal=dec_)

