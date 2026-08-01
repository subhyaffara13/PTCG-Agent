
def test_convolution_int():
    assert convolution_int([1], [1]) == [1]
    assert convolution_int([1, 1], [0]) == [0]
    assert convolution_int([1, 2, 3], [4, 5, 6]) == [4, 13, 28, 27, 18]
    assert convolution_int([1], [5, 6, 7]) == [5, 6, 7]
    assert convolution_int([1, 3], [5, 6, 7]) == [5, 21, 25, 21]
    assert convolution_int([10, -5, 1, 3], [-5, 6, 7]) == [-50, 85, 35, -44, 25, 21]
    assert convolution_int([0, 1, 0, -1], [1, 0, -1, 0]) == [0, 1, 0, -2, 0, 1]
    assert convolution_int(
        [-341, -5, 1, 3, -71, -99, 43, 87],
        [5, 6, 7, 12, 345, 21, -78, -7, -89]
    ) == [-1705, -2071, -2412, -4106, -118035, -9774, 25998, 2981, 5509,
          -34317, 19228, 38870, 5485, 1724, -4436, -7743]

