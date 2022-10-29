import pygame
import Config
import math
import numpy as np
from angle_sort import sort_by_angle
from compare_operators import * 
import vector_arithmetic as va

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def vector_length(vector):
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def bin_search(sorted_list, angle, start, end):
    if start >= end:        #end not included
        return None
    else:
        i = (start + end)//2
        if angle == sorted_list[i]:
            j = i
            while sorted_list[i] == angle and i > 0:
                i -= 1 
            while sorted_list[j] == angle and j < len(sorted_list):
                j += 1
            return (i+1, j)
            
        elif angle > sorted_list[i]:
            return bin_search(sorted_list, angle, i + 1, end)
        else:
            return bin_search(sorted_list, angle, start, i)
        

def light_intersection(light_source, light_vec, wall_vec, wall_anchor):
    den = light_vec[0] * wall_vec[1] - wall_vec[0] * light_vec[1]
    sgn = signum(den)
    den = abs(den)
    if not is_zero(den):
        a = (wall_anchor[0] - light_source[0], wall_anchor[1] - light_source[1])
        s = (light_vec[1] * (a[0]) - light_vec[0] * (a[1])) * sgn
        t = (wall_vec[1] * (a[0]) - wall_vec[0] * (a[1])) * sgn
        if (is_between(s, 0, den) and is_bigger(t, 0)):
            return t / den
    return None


def intersect_walls(walls, light_vec, light_source, walls_collector = None):
    min_dist = math.inf
    closest_point = None
    top_wall = None
    for wall in walls:
        wall_vec = va.get_vector(wall.start_pos, wall.end_pos)
        dist = light_intersection(light_source, light_vec, wall_vec, wall.start_pos)
        if dist:
            if walls_collector != None:                 # if which wall intersect information is needed 
                walls_collector.add(wall)
            if dist < min_dist:                 # 
                x = light_source[0] + (dist * light_vec[0])
                y = light_source[1] + (dist * light_vec[1])
                closest_point = (x, y)
                min_dist = dist
                top_wall = wall
    return [min_dist, closest_point, top_wall]



class light_handling:
    def __init__(self, walls, points) -> None:
        self.walls = walls
        self.polygon = []
        self.points = points
        self.mouse_pos = None
        self.rays = []
        self.radius = max(Config.WINDOW_SIZE) * 2
        self.multiplier = 1.5
        self.effect_size = tuple(map( lambda x: x*self.multiplier, Config.WINDOW_SIZE))
        self.light_effect = pygame.transform.scale(pygame.image.load('light_effect.png'), self.effect_size).convert() 


    def update_data(self, walls, points):
        self.walls = walls
        self.points = points


    def extract_polygon(self):
        self.polygon.clear()
        sorted_points = [ point for point in self.points]
        sort_by_angle(sorted_points, self.mouse_pos)

        curr_walls = set()
        top_wall = None

        #---------------------------------<<< 2 >>>---------------------------------
        ### checking how many walls are in curr_walls at start
        start_vec = (1, 0)                       # vector that is border between sorted_points[-1] and sorted_points[0] 
        min_dist, closest_point, closest_wall = intersect_walls(self.walls, start_vec, self.mouse_pos, curr_walls)
        self.polygon.append(closest_point)
                
        for i in range(len(sorted_points)):
            vertex = sorted_points[i]
            point = self.points[vertex]

            new_buffer = set()                  # set of lately added points
            rm_buffer = set()                   # set of walls to remove before next iteration

            if point.wall_end in curr_walls:
                curr_walls.remove(point.wall_end)
                rm_buffer.add(point.wall_end)
            else:
                new_buffer.add(point.wall_end)
            if point.wall_start in curr_walls:
                curr_walls.remove(point.wall_start)
                rm_buffer.add(point.wall_start)
            else:
                new_buffer.add(point.wall_start)

            min_dist = {}
            closest_point= {}
            closest_wall = {}

            light_vec = va.normalize(va.get_vector(self.mouse_pos, vertex))
            min_dist['curr'], closest_point['curr'], closest_wall['curr'] = intersect_walls(curr_walls, light_vec, self.mouse_pos)
            min_dist['new'], closest_point['new'], closest_wall['new'] = intersect_walls(new_buffer, light_vec, self.mouse_pos)         
            min_dist['rm'], closest_point['rm'], closest_wall['rm'] = intersect_walls(rm_buffer, light_vec, self.mouse_pos)              
            
            k = min([min_dist[key] for key in min_dist])
            
            if is_equal(k, min_dist['rm']) :   
                self.polygon.append(closest_point['rm'])
                if closest_point['curr'] != None and point.wall_end in rm_buffer and point.wall_start in rm_buffer:
                    self.polygon.append(closest_point['curr'])
                top_wall = closest_wall['rm']
            elif is_equal(k, min_dist['new']):
                if closest_point['curr'] != None and point.wall_end in new_buffer and point.wall_start in new_buffer:
                    self.polygon.append(closest_point['curr'])
                self.polygon.append(closest_point['new'])
                top_wall = closest_wall['new']
            elif is_equal(k, min_dist['curr']):
                if top_wall != closest_wall['curr']:
                    self.polygon.append(closest_point['curr'])
                    top_wall = closest_wall['curr']
            
            curr_walls.update(new_buffer)
            curr_walls -= rm_buffer
        # print(self.polygon)
        # print(self.mouse_pos)



    def update_variables(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            self.mouse_pos = mouse_pos
            self.mouse_pos = (592, 300)
            self.extract_polygon()
        else:
            self.mouse_pos = None
        


    def draw(self, surface: pygame.Surface):
        # if self.mouse_pos != None:
        #     pygame.draw.polygon(surface, (200,100,0), self.polygon)

        if self.mouse_pos != None:
            new_surface = pygame.Surface(Config.WINDOW_SIZE)
            new_surface.fill((0,0,0))
            if self.mouse_pos != None:
                pygame.draw.polygon(new_surface, (0,255,0), self.polygon)
            new_surface.set_colorkey((0,255,0))
            surface.blit(self.light_effect, (self.mouse_pos[0] - self.effect_size[0]/2, self.mouse_pos[1] - self.effect_size[1]/2))
            surface.blit(new_surface, (0,0))