import vector_arithmetic as va
import compare_operators as co
import Config

def compare_angles(main_point, point_a, point_b):
    ''' a >? b '''
    # if they all lay on the same horizontal axis 
    if main_point[1] == point_a[1] == point_b[1]:
        return point_a[0] < point_b[0]

    # if they both lay below main_point or above 
    if (point_a[1] > main_point[1] and point_b[1] > main_point[1]) or \
        (point_a[1] < main_point[1] and point_b[1] < main_point[1]):        
        det = det2x2(main_point, point_a, point_b)
        return det > 0     
    
    return point_a[1] > point_b[1] 
    


# def is_on_left(line_point_a, line_point_b, point):
#     det = det2x2(line_point_a, line_point_b, point)
#     if co.is_zero(det, 0):
#         return None
#     if det > 0:
#         return True
#     return False


def det2x2(lineA, lineB, pointC):    #2x2
    return (lineA[0] - pointC[0]) * (lineB[1] - pointC[1]) - (lineA[1] - pointC[1]) * (lineB[0] - pointC[0])


def sort_by_angle(points, main_point):
    def partition(start, end):
        pivot = points[end - 1]
        i = start
        for p in range(start, end - 1):
            if not compare_angles(main_point, points[p], pivot):
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