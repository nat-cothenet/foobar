from scipy.optimize import linprog
from fractions import Fraction

def solution(pegs):
    if len(pegs) < 2 or len(pegs) > 20:
        raise Exception("Length of pegs list out of range")

    ratio_arr = [1]
    ratio_arr.extend([0] * (len(pegs) - 2))
    ratio_arr.extend([-2])
    ratio = 0

    non_overlaps = [
        ([0] * n) + [1, 1] + ([0] * (len(pegs) - n - 2)) for n in range(0, len(pegs) - 1)
    ]
    equal_overlaps = [
        pegs[n+1] - pegs[n] for n in range(0, len(pegs)-1)
    ]

    coefficients_equalities = [
        ratio_arr
    ]
    coefficients_equalities.extend(non_overlaps)
    constants_equalities = [ratio]
    constants_equalities.extend(equal_overlaps)
    constants_equalities = [constants_equalities]

    # Bounds
    min_rad = [1] * len(pegs)
    max_rad = [pegs[1] - pegs[0] - 1]
    max_rad.extend([min(pegs[i] - pegs[i - 1] - 1,
                   pegs[i + 1] - pegs[i] - 1)
               for i in range(1, len(pegs)-1)])
    max_rad.append(pegs[-1] - pegs[-2] - 1)
    bounds = [
        (min_rad[i], max_rad[i]) for i in range(len(pegs))
    ]

    # Maximize our initial radius
    max_r1 = [-1]
    max_r1.extend([0] * (len(pegs) - 1))
    max_r1.extend([])
    res = linprog(max_r1,
                  A_eq=coefficients_equalities,
                  b_eq=constants_equalities,
                  bounds=bounds)

    frac = Fraction(-res.fun).limit_denominator()
    frac = [frac.numerator, frac.denominator]
    #frac = [frac[0], frac[1]]

    if res.success:
        return frac
    else:
        return [-1, -1]

    return frac


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(solution([4, 30, 50]))
    print(solution([4, 17, 50]))
