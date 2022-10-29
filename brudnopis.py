from light_handling import *
from tile_map import *
import vector_arithmetic as va
from angle_sort import sort_by_angle
from geoAlg.tool import * 
from angle_sort import *

# wall = Wall((960, 640), (960,0))
# light_source = (959,0)
# light_vec = va.normalize(va.get_vector(light_source, (0,0)))
# res = light_intersection(light_source, light_vec, va.get_vector(wall.start_pos, wall.end_pos), wall.start_pos)
# print(res)

# ------ VISUALS    
# main_point = (5, 5)
# points = [(0, 0), (9, 0), (3, 5), (7, 9), (9, 1), (2, 3), (5, 9), (8, 7)]
# sort_by_angle(points, main_point)
# print(points)

# scenes = [Scene(points=[PointsCollection(points), PointsCollection([main_point], color='red')])]
# scenes = [Scene(points=[PointsCollection([(720.0, 260.0), (960.0, 0.0), (348.0, -5.684341886080802e-14), (540.0, 160.0), (720.0, 260.0), (720.0, 260.0), (540.0, 274.11764705882354), (540.0, 300.0), (0.0, 480.0), (1.1368683772161603e-13, 640.0), (960.0, 640.0), (960.0, 460.0), (720.0, 300.0), (720.0, 284.0)]), PointsCollection([(660, 260)], color='red')])]

# plot = Plot(scenes)

# ------ SORTING
print(compare_angles((592, 240), (700, 240), (960, 0)))
points = [(960, 0), (540, 160), (0, 0), (320, 160), (320, 300), (0, 640), (540, 300), (620, 300), (960, 640), (700, 300), (620, 240), (700, 240)]
sort_by_angle(points, (592, 300))
print(points)