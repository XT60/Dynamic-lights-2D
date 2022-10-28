from vector_arithmetic import *
ZERO_TOLERANCE = 1e-15

def is_equal(n1, n2):
    return abs(n1 - n2) <= 1e-12


def is_bigger(mainPoint, pointA, pointB):
    ''' a >? b '''
    d = det2x2(mainPoint, pointA, pointB)
    if d > ZERO_TOLERANCE:
        return False
    elif is_equal(d, 0):
        la = square_length(substract_vec(pointA, mainPoint))
        lb = square_length(substract_vec(pointB, mainPoint))
        if la > lb:
            return False 
        return True
    return True


def det2x2(lineA, lineB, pointC):    #2x2
    return (lineA[0] - pointC[0]) * (lineB[1] - pointC[1]) - (lineA[1] - pointC[1]) * (lineB[0] - pointC[0])


def sort_by_angle(points, mainPoint):
    def partition(start, end):
        pivot = points[end - 1]
        i = start
        for p in range(start, end - 1):
            if not is_bigger(mainPoint, points[p], pivot):
                points[i], points[p] = points[p], points[i] 
                i += 1
        points[i], points[end - 1] = points[end - 1], points[i]
        return i
    
    def quick_sort(start, end):
        if end - start < 2:
            return
        pivot = partition(start, end)
        quick_sort(start, pivot)
        quick_sort(pivot + 1, end)
    
    quick_sort(0, len(points))