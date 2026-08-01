
def test_image_shift():
    imgData = [[1 / x + 1 / y for x in range(1, 100)] for y in range(1, 100)]
    tMin = 734717.945208
    tMax = 734717.946366

    fig, ax = plt.subplots()
    ax.imshow(imgData, norm=colors.LogNorm(), interpolation='none',
              extent=(tMin, tMax, 1, 100))
    ax.set_aspect('auto')

