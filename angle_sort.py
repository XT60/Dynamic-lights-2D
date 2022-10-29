def compare_angles(main_point, point_a, point_b):
    ''' a >? b '''
    # if they all lay on the same horizontal axis as main_point
    if main_point[1] == point_a[1] == point_b[1]:
        if point_b[0] < main_point[0] and main_point[0] < point_a[0]:
            return True
        elif point_a[0] < main_point[0] and main_point[0] < point_b[0]:
            return False
        return point_a[0] < point_b[0]

    # if one of them is on the same horizontal axis as main_point
    if main_point[1] == point_a[1]:
        if main_point[0] < point_a[0]:
            return True
        elif main_point[1] < point_b[1]:
            return False
        return True
    
    if main_point[1] == point_b[1]:
        if main_point[0] < point_b[0]:
            return False
        elif main_point[1] < point_a[1]:
            return True
        return False

    # if they both lay below main_point or above 
    if (point_a[1] > main_point[1] and point_b[1] > main_point[1]) or \
        (point_a[1] < main_point[1] and point_b[1] < main_point[1]):        
        det = det2x2(main_point, point_a, point_b)
        return det > 0     
    
    return point_a[1] > point_b[1] 
    

def det2x2(lineA, lineB, pointC):
    '''2x2 matrix determinant that determines how pointC lays relative to line from lineA to lineB ( >0 -> left; <0 -> right, ==0 collinear)'''
    return (lineA[0] - pointC[0]) * (lineB[1] - pointC[1]) - (lineA[1] - pointC[1]) * (lineB[0] - pointC[0])


def sort_by_angle(points, main_point):
    '''Quicksort algorithm modified to sort by angle relative to main_point'''
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

