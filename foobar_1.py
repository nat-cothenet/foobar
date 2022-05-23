import math


def solution2(area):
    if area < 0 or area > 1000000:
        raise Exception("Input out of range")
    if area == 0:
        return []

    list_squares = []
    max_square = int(math.floor(math.sqrt(area)) ** 2)
    if max_square > 0:
        list_squares.append(max_square)
    list_squares.extend(
        solution(area - max_square)
    )

    list_squares.sort(reverse=True)

    return list_squares


def solution(area):
    list_squares = []
    remaining_area = area
    while remaining_area >= 1:
        max_square = int(math.floor(math.sqrt(remaining_area)) ** 2)
        list_squares.append(max_square)
        remaining_area -= max_square

    return list_squares


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(solution2(12))
    print(solution2(15324))
