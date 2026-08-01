
def mathieu_mc2_scaled(m, q, x):
    return mathieu_modcem2(m, q, x)[0] * np.sqrt(np.pi/2)

