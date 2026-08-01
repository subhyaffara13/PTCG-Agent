
def get_lebedev_recurrence_points(type_, start, a, b, v, leb):
    c = 0.0

    match type_:

        case 1:
            a = 1.0

            leb.x[start] = a
            leb.y[start] = 0.0
            leb.z[start] = 0.0
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = -a
            leb.y[start + 1] = 0.0
            leb.z[start + 1] = 0.0
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = 0.0
            leb.y[start + 2] = a
            leb.z[start + 2] = 0.0
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = 0.0
            leb.y[start + 3] = -a
            leb.z[start + 3] = 0.0
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = 0.0
            leb.y[start + 4] = 0.0
            leb.z[start + 4] = a
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = 0.0
            leb.y[start + 5] = 0.0
            leb.z[start + 5] = -a
            leb.w[start + 5] = 4.0 * pi * v
            start = start + 6

        case 2:
            a = sqrt(0.5)
            leb.x[start] = 0.0
            leb.y[start] = a
            leb.z[start] = a
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = 0.0
            leb.y[start + 1] = -a
            leb.z[start + 1] = a
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = 0.0
            leb.y[start + 2] = a
            leb.z[start + 2] = -a
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = 0.0
            leb.y[start + 3] = -a
            leb.z[start + 3] = -a
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = a
            leb.y[start + 4] = 0.0
            leb.z[start + 4] = a
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = a
            leb.y[start + 5] = 0.0
            leb.z[start + 5] = -a
            leb.w[start + 5] = 4.0 * pi * v

            leb.x[start + 6] = -a
            leb.y[start + 6] = 0.0
            leb.z[start + 6] = a
            leb.w[start + 6] = 4.0 * pi * v

            leb.x[start + 7] = -a
            leb.y[start + 7] = 0.0
            leb.z[start + 7] = -a
            leb.w[start + 7] = 4.0 * pi * v

            leb.x[start + 8] = a
            leb.y[start + 8] = a
            leb.z[start + 8] = 0.0
            leb.w[start + 8] = 4.0 * pi * v

            leb.x[start + 9] = -a
            leb.y[start + 9] = a
            leb.z[start + 9] = 0.0
            leb.w[start + 9] = 4.0 * pi * v

            leb.x[start + 10] = a
            leb.y[start + 10] = -a
            leb.z[start + 10] = 0.0
            leb.w[start + 10] = 4.0 * pi * v

            leb.x[start + 11] = -a
            leb.y[start + 11] = -a
            leb.z[start + 11] = 0.0
            leb.w[start + 11] = 4.0 * pi * v
            start = start + 12

        case 3:
            a = sqrt(1.0 / 3.0)
            leb.x[start] = a
            leb.y[start] = a
            leb.z[start] = a
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = -a
            leb.y[start + 1] = a
            leb.z[start + 1] = a
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = a
            leb.y[start + 2] = -a
            leb.z[start + 2] = a
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = a
            leb.y[start + 3] = a
            leb.z[start + 3] = -a
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = -a
            leb.y[start + 4] = -a
            leb.z[start + 4] = a
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = a
            leb.y[start + 5] = -a
            leb.z[start + 5] = -a
            leb.w[start + 5] = 4.0 * pi * v

            leb.x[start + 6] = -a
            leb.y[start + 6] = a
            leb.z[start + 6] = -a
            leb.w[start + 6] = 4.0 * pi * v

            leb.x[start + 7] = -a
            leb.y[start + 7] = -a
            leb.z[start + 7] = -a
            leb.w[start + 7] = 4.0 * pi * v
            start = start + 8

        case 4:
            # /* In this case A is inputed */
            b = sqrt(1.0 - 2.0 * a * a)
            leb.x[start] = a
            leb.y[start] = a
            leb.z[start] = b
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = -a
            leb.y[start + 1] = a
            leb.z[start + 1] = b
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = a
            leb.y[start + 2] = -a
            leb.z[start + 2] = b
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = a
            leb.y[start + 3] = a
            leb.z[start + 3] = -b
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = -a
            leb.y[start + 4] = -a
            leb.z[start + 4] = b
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = -a
            leb.y[start + 5] = a
            leb.z[start + 5] = -b
            leb.w[start + 5] = 4.0 * pi * v

            leb.x[start + 6] = a
            leb.y[start + 6] = -a
            leb.z[start + 6] = -b
            leb.w[start + 6] = 4.0 * pi * v

            leb.x[start + 7] = -a
            leb.y[start + 7] = -a
            leb.z[start + 7] = -b
            leb.w[start + 7] = 4.0 * pi * v

            leb.x[start + 8] = -a
            leb.y[start + 8] = b
            leb.z[start + 8] = a
            leb.w[start + 8] = 4.0 * pi * v

            leb.x[start + 9] = a
            leb.y[start + 9] = -b
            leb.z[start + 9] = a
            leb.w[start + 9] = 4.0 * pi * v

            leb.x[start + 10] = a
            leb.y[start + 10] = b
            leb.z[start + 10] = -a
            leb.w[start + 10] = 4.0 * pi * v

            leb.x[start + 11] = -a
            leb.y[start + 11] = -b
            leb.z[start + 11] = a
            leb.w[start + 11] = 4.0 * pi * v

            leb.x[start + 12] = -a
            leb.y[start + 12] = b
            leb.z[start + 12] = -a
            leb.w[start + 12] = 4.0 * pi * v

            leb.x[start + 13] = a
            leb.y[start + 13] = -b
            leb.z[start + 13] = -a
            leb.w[start + 13] = 4.0 * pi * v

            leb.x[start + 14] = -a
            leb.y[start + 14] = -b
            leb.z[start + 14] = -a
            leb.w[start + 14] = 4.0 * pi * v

            leb.x[start + 15] = a
            leb.y[start + 15] = b
            leb.z[start + 15] = a
            leb.w[start + 15] = 4.0 * pi * v

            leb.x[start + 16] = b
            leb.y[start + 16] = a
            leb.z[start + 16] = a
            leb.w[start + 16] = 4.0 * pi * v

            leb.x[start + 17] = -b
            leb.y[start + 17] = a
            leb.z[start + 17] = a
            leb.w[start + 17] = 4.0 * pi * v

            leb.x[start + 18] = b
            leb.y[start + 18] = -a
            leb.z[start + 18] = a
            leb.w[start + 18] = 4.0 * pi * v

            leb.x[start + 19] = b
            leb.y[start + 19] = a
            leb.z[start + 19] = -a
            leb.w[start + 19] = 4.0 * pi * v

            leb.x[start + 20] = -b
            leb.y[start + 20] = -a
            leb.z[start + 20] = a
            leb.w[start + 20] = 4.0 * pi * v

            leb.x[start + 21] = -b
            leb.y[start + 21] = a
            leb.z[start + 21] = -a
            leb.w[start + 21] = 4.0 * pi * v

            leb.x[start + 22] = b
            leb.y[start + 22] = -a
            leb.z[start + 22] = -a
            leb.w[start + 22] = 4.0 * pi * v

            leb.x[start + 23] = -b
            leb.y[start + 23] = -a
            leb.z[start + 23] = -a
            leb.w[start + 23] = 4.0 * pi * v
            start = start + 24

        case 5:
            # /* A is inputed in this case as well*/
            b = sqrt(1 - a * a)
            leb.x[start] = a
            leb.y[start] = b
            leb.z[start] = 0.0
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = -a
            leb.y[start + 1] = b
            leb.z[start + 1] = 0.0
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = a
            leb.y[start + 2] = -b
            leb.z[start + 2] = 0.0
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = -a
            leb.y[start + 3] = -b
            leb.z[start + 3] = 0.0
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = b
            leb.y[start + 4] = a
            leb.z[start + 4] = 0.0
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = -b
            leb.y[start + 5] = a
            leb.z[start + 5] = 0.0
            leb.w[start + 5] = 4.0 * pi * v

            leb.x[start + 6] = b
            leb.y[start + 6] = -a
            leb.z[start + 6] = 0.0
            leb.w[start + 6] = 4.0 * pi * v

            leb.x[start + 7] = -b
            leb.y[start + 7] = -a
            leb.z[start + 7] = 0.0
            leb.w[start + 7] = 4.0 * pi * v

            leb.x[start + 8] = a
            leb.y[start + 8] = 0.0
            leb.z[start + 8] = b
            leb.w[start + 8] = 4.0 * pi * v

            leb.x[start + 9] = -a
            leb.y[start + 9] = 0.0
            leb.z[start + 9] = b
            leb.w[start + 9] = 4.0 * pi * v

            leb.x[start + 10] = a
            leb.y[start + 10] = 0.0
            leb.z[start + 10] = -b
            leb.w[start + 10] = 4.0 * pi * v

            leb.x[start + 11] = -a
            leb.y[start + 11] = 0.0
            leb.z[start + 11] = -b
            leb.w[start + 11] = 4.0 * pi * v

            leb.x[start + 12] = b
            leb.y[start + 12] = 0.0
            leb.z[start + 12] = a
            leb.w[start + 12] = 4.0 * pi * v

            leb.x[start + 13] = -b
            leb.y[start + 13] = 0.0
            leb.z[start + 13] = a
            leb.w[start + 13] = 4.0 * pi * v

            leb.x[start + 14] = b
            leb.y[start + 14] = 0.0
            leb.z[start + 14] = -a
            leb.w[start + 14] = 4.0 * pi * v

            leb.x[start + 15] = -b
            leb.y[start + 15] = 0.0
            leb.z[start + 15] = -a
            leb.w[start + 15] = 4.0 * pi * v

            leb.x[start + 16] = 0.0
            leb.y[start + 16] = a
            leb.z[start + 16] = b
            leb.w[start + 16] = 4.0 * pi * v

            leb.x[start + 17] = 0.0
            leb.y[start + 17] = -a
            leb.z[start + 17] = b
            leb.w[start + 17] = 4.0 * pi * v

            leb.x[start + 18] = 0.0
            leb.y[start + 18] = a
            leb.z[start + 18] = -b
            leb.w[start + 18] = 4.0 * pi * v

            leb.x[start + 19] = 0.0
            leb.y[start + 19] = -a
            leb.z[start + 19] = -b
            leb.w[start + 19] = 4.0 * pi * v

            leb.x[start + 20] = 0.0
            leb.y[start + 20] = b
            leb.z[start + 20] = a
            leb.w[start + 20] = 4.0 * pi * v

            leb.x[start + 21] = 0.0
            leb.y[start + 21] = -b
            leb.z[start + 21] = a
            leb.w[start + 21] = 4.0 * pi * v

            leb.x[start + 22] = 0.0
            leb.y[start + 22] = b
            leb.z[start + 22] = -a
            leb.w[start + 22] = 4.0 * pi * v

            leb.x[start + 23] = 0.0
            leb.y[start + 23] = -b
            leb.z[start + 23] = -a
            leb.w[start + 23] = 4.0 * pi * v
            start = start + 24

        case 6:
            # /* both A and B are inputed in this case */
            c = sqrt(1.0 - a * a - b * b)
            leb.x[start] = a
            leb.y[start] = b
            leb.z[start] = c
            leb.w[start] = 4.0 * pi * v

            leb.x[start + 1] = -a
            leb.y[start + 1] = b
            leb.z[start + 1] = c
            leb.w[start + 1] = 4.0 * pi * v

            leb.x[start + 2] = a
            leb.y[start + 2] = -b
            leb.z[start + 2] = c
            leb.w[start + 2] = 4.0 * pi * v

            leb.x[start + 3] = a
            leb.y[start + 3] = b
            leb.z[start + 3] = -c
            leb.w[start + 3] = 4.0 * pi * v

            leb.x[start + 4] = -a
            leb.y[start + 4] = -b
            leb.z[start + 4] = c
            leb.w[start + 4] = 4.0 * pi * v

            leb.x[start + 5] = a
            leb.y[start + 5] = -b
            leb.z[start + 5] = -c
            leb.w[start + 5] = 4.0 * pi * v

            leb.x[start + 6] = -a
            leb.y[start + 6] = b
            leb.z[start + 6] = -c
            leb.w[start + 6] = 4.0 * pi * v

            leb.x[start + 7] = -a
            leb.y[start + 7] = -b
            leb.z[start + 7] = -c
            leb.w[start + 7] = 4.0 * pi * v

            leb.x[start + 8] = b
            leb.y[start + 8] = a
            leb.z[start + 8] = c
            leb.w[start + 8] = 4.0 * pi * v

            leb.x[start + 9] = -b
            leb.y[start + 9] = a
            leb.z[start + 9] = c
            leb.w[start + 9] = 4.0 * pi * v

            leb.x[start + 10] = b
            leb.y[start + 10] = -a
            leb.z[start + 10] = c
            leb.w[start + 10] = 4.0 * pi * v

            leb.x[start + 11] = b
            leb.y[start + 11] = a
            leb.z[start + 11] = -c
            leb.w[start + 11] = 4.0 * pi * v

            leb.x[start + 12] = -b
            leb.y[start + 12] = -a
            leb.z[start + 12] = c
            leb.w[start + 12] = 4.0 * pi * v

            leb.x[start + 13] = b
            leb.y[start + 13] = -a
            leb.z[start + 13] = -c
            leb.w[start + 13] = 4.0 * pi * v

            leb.x[start + 14] = -b
            leb.y[start + 14] = a
            leb.z[start + 14] = -c
            leb.w[start + 14] = 4.0 * pi * v

            leb.x[start + 15] = -b
            leb.y[start + 15] = -a
            leb.z[start + 15] = -c
            leb.w[start + 15] = 4.0 * pi * v

            leb.x[start + 16] = c
            leb.y[start + 16] = a
            leb.z[start + 16] = b
            leb.w[start + 16] = 4.0 * pi * v

            leb.x[start + 17] = -c
            leb.y[start + 17] = a
            leb.z[start + 17] = b
            leb.w[start + 17] = 4.0 * pi * v

            leb.x[start + 18] = c
            leb.y[start + 18] = -a
            leb.z[start + 18] = b
            leb.w[start + 18] = 4.0 * pi * v

            leb.x[start + 19] = c
            leb.y[start + 19] = a
            leb.z[start + 19] = -b
            leb.w[start + 19] = 4.0 * pi * v

            leb.x[start + 20] = -c
            leb.y[start + 20] = -a
            leb.z[start + 20] = b
            leb.w[start + 20] = 4.0 * pi * v

            leb.x[start + 21] = c
            leb.y[start + 21] = -a
            leb.z[start + 21] = -b
            leb.w[start + 21] = 4.0 * pi * v

            leb.x[start + 22] = -c
            leb.y[start + 22] = a
            leb.z[start + 22] = -b
            leb.w[start + 22] = 4.0 * pi * v

            leb.x[start + 23] = -c
            leb.y[start + 23] = -a
            leb.z[start + 23] = -b
            leb.w[start + 23] = 4.0 * pi * v

            leb.x[start + 24] = c
            leb.y[start + 24] = b
            leb.z[start + 24] = a
            leb.w[start + 24] = 4.0 * pi * v

            leb.x[start + 25] = -c
            leb.y[start + 25] = b
            leb.z[start + 25] = a
            leb.w[start + 25] = 4.0 * pi * v

            leb.x[start + 26] = c
            leb.y[start + 26] = -b
            leb.z[start + 26] = a
            leb.w[start + 26] = 4.0 * pi * v

            leb.x[start + 27] = c
            leb.y[start + 27] = b
            leb.z[start + 27] = -a
            leb.w[start + 27] = 4.0 * pi * v

            leb.x[start + 28] = -c
            leb.y[start + 28] = -b
            leb.z[start + 28] = a
            leb.w[start + 28] = 4.0 * pi * v

            leb.x[start + 29] = c
            leb.y[start + 29] = -b
            leb.z[start + 29] = -a
            leb.w[start + 29] = 4.0 * pi * v

            leb.x[start + 30] = -c
            leb.y[start + 30] = b
            leb.z[start + 30] = -a
            leb.w[start + 30] = 4.0 * pi * v

            leb.x[start + 31] = -c
            leb.y[start + 31] = -b
            leb.z[start + 31] = -a
            leb.w[start + 31] = 4.0 * pi * v

            leb.x[start + 32] = a
            leb.y[start + 32] = c
            leb.z[start + 32] = b
            leb.w[start + 32] = 4.0 * pi * v

            leb.x[start + 33] = -a
            leb.y[start + 33] = c
            leb.z[start + 33] = b
            leb.w[start + 33] = 4.0 * pi * v

            leb.x[start + 34] = a
            leb.y[start + 34] = -c
            leb.z[start + 34] = b
            leb.w[start + 34] = 4.0 * pi * v

            leb.x[start + 35] = a
            leb.y[start + 35] = c
            leb.z[start + 35] = -b
            leb.w[start + 35] = 4.0 * pi * v

            leb.x[start + 36] = -a
            leb.y[start + 36] = -c
            leb.z[start + 36] = b
            leb.w[start + 36] = 4.0 * pi * v

            leb.x[start + 37] = a
            leb.y[start + 37] = -c
            leb.z[start + 37] = -b
            leb.w[start + 37] = 4.0 * pi * v

            leb.x[start + 38] = -a
            leb.y[start + 38] = c
            leb.z[start + 38] = -b
            leb.w[start + 38] = 4.0 * pi * v

            leb.x[start + 39] = -a
            leb.y[start + 39] = -c
            leb.z[start + 39] = -b
            leb.w[start + 39] = 4.0 * pi * v

            leb.x[start + 40] = b
            leb.y[start + 40] = c
            leb.z[start + 40] = a
            leb.w[start + 40] = 4.0 * pi * v

            leb.x[start + 41] = -b
            leb.y[start + 41] = c
            leb.z[start + 41] = a
            leb.w[start + 41] = 4.0 * pi * v

            leb.x[start + 42] = b
            leb.y[start + 42] = -c
            leb.z[start + 42] = a
            leb.w[start + 42] = 4.0 * pi * v

            leb.x[start + 43] = b
            leb.y[start + 43] = c
            leb.z[start + 43] = -a
            leb.w[start + 43] = 4.0 * pi * v

            leb.x[start + 44] = -b
            leb.y[start + 44] = -c
            leb.z[start + 44] = a
            leb.w[start + 44] = 4.0 * pi * v

            leb.x[start + 45] = b
            leb.y[start + 45] = -c
            leb.z[start + 45] = -a
            leb.w[start + 45] = 4.0 * pi * v

            leb.x[start + 46] = -b
            leb.y[start + 46] = c
            leb.z[start + 46] = -a
            leb.w[start + 46] = 4.0 * pi * v

            leb.x[start + 47] = -b
            leb.y[start + 47] = -c
            leb.z[start + 47] = -a
            leb.w[start + 47] = 4.0 * pi * v
            start = start + 48

        case _:
            raise Exception('Bad grid order')

    return leb, start

