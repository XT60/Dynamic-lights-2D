import pygame
import Config
import math
from angle_sort import sort_by_angle
from compare_operators import * 
import vector_arithmetic as va

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def clamp(x_val, min_val, max_val):
    return max(min_val, min(max_val, x_val))


def are_in_set(args:list, set_instance:set):
    for arg in args:
        if arg not in set_instance:
            return False
    return True


def light_intersection(light_source, light_vec, wall_vec, wall_anchor):
    '''finds intersection point between light and wall'''
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
    ''' finds closest light intersection with given walls'''
    min_dist = math.inf
    closest_point = None
    top_wall = None
    for wall in walls:
        wall_vec = va.get_vector(wall.start_pos, wall.end_pos)
        dist = light_intersection(light_source, light_vec, wall_vec, wall.start_pos)
        if dist:
            if walls_collector != None:
                walls_collector.add(wall)
            if dist < min_dist:
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

        # sorting points by angle relative to current mouse position
        sorted_points = [point for point in self.points]
        sort_by_angle(sorted_points, self.mouse_pos)

        curr_walls = set()
        top_wall = [None, None]     # candidates for real topmost wall

        # finds walls that should be in curr_walls at start
        start_vec = (1, 0)
        collide_walls = set()
        min_dist, closest_point, closest_wall = intersect_walls(self.walls, start_vec, self.mouse_pos, collide_walls)
        for wall in collide_walls:
            if wall.start_pos[1] < self.mouse_pos[1] or wall.end_pos[1] < self.mouse_pos[1]:
                curr_walls.add(wall)

        # finds first intersection point
        min_dist, closest_point, closest_wall = intersect_walls(curr_walls, start_vec, self.mouse_pos)
        top_wall[0] = closest_wall
        self.polygon.append(closest_point)

        for vertex in sorted_points:
            point = self.points[vertex]
            new_buffer = set()                  # set of walls added in current iteration
            rm_buffer = set()                   # set of walls that will be removed in next iteration

            for wall in point.walls:
                if wall:
                    if wall in curr_walls:
                        curr_walls.remove(wall)
                        rm_buffer.add(wall)
                    else:
                        new_buffer.add(wall)

            min_dist = {}
            closest_point= {}
            closest_wall = {}

            light_vec = va.normalize(va.get_vector(self.mouse_pos, vertex))
            min_dist['curr'], closest_point['curr'], closest_wall['curr'] = intersect_walls(curr_walls, light_vec, self.mouse_pos)
            min_dist['new'], closest_point['new'], closest_wall['new'] = intersect_walls(new_buffer, light_vec, self.mouse_pos)         
            min_dist['rm'], closest_point['rm'], closest_wall['rm'] = intersect_walls(rm_buffer, light_vec, self.mouse_pos)              
            
            k = min([min_dist[key] for key in min_dist])

            if is_equal(k, min_dist['new']):
                if closest_point['curr'] != None and are_in_set(point.walls, new_buffer):
                    self.polygon.append(closest_point['curr'])
                self.polygon.append(closest_point['new'])
                top_wall[1] = None
                if are_points_equal(closest_point['new'], vertex):
                    # when closest point is on vertex and both walls are good candidates for top_wall
                    i = 0
                    for wall in point.walls:
                        if wall in new_buffer:
                            top_wall[i] = wall
                            i += 1
                else:
                    top_wall[0] = closest_wall['new']       

            elif is_equal(k, min_dist['rm']) :   
                self.polygon.append(closest_point['rm'])
                if closest_point['curr'] != None and are_in_set(point.walls, rm_buffer):
                    self.polygon.append(closest_point['curr'])
                if are_points_equal(closest_point['rm'], vertex):
                    # when closest point is on vertex and we don't know which wall to set as top_wall
                    for wall in point.walls:
                        if wall in new_buffer:
                            top_wall[0] = wall
                else:
                    top_wall[0] = closest_wall['rm']
                top_wall[1] = None

            elif is_equal(k, min_dist['curr']):
                if len(point.walls) == 0 and are_points_equal(vertex, closest_point['curr']):
                    self.polygon.append(closest_point['curr'])
                else:
                    if top_wall[0] != closest_wall['curr']:
                        if top_wall[1] == closest_wall['curr']:
                            top_wall[1] = top_wall[0]
                        else:
                            self.polygon.append(closest_point['curr'])
                            top_wall[0] = closest_wall['curr']
                        top_wall[1] = None
            
            curr_walls.update(new_buffer)
            curr_walls -= rm_buffer


    def update_variables(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            self.mouse_pos = (clamp(mouse_pos[0], Config.BORDER_BLOCK, Config.WINDOW_SIZE[0] - Config.BORDER_BLOCK),
             clamp(mouse_pos[1], Config.BORDER_BLOCK, Config.WINDOW_SIZE[1] - Config.BORDER_BLOCK))
            self.extract_polygon()
        else:
            self.mouse_pos = None
        

    def draw(self, surface: pygame.Surface):
        if self.mouse_pos != None:
            new_surface = pygame.Surface(Config.WINDOW_SIZE)
            new_surface.fill((0,0,0))
            if self.mouse_pos != None:
                pygame.draw.polygon(new_surface, (0,255,0), self.polygon)
            new_surface.set_colorkey((0,255,0))
            surface.blit(self.light_effect, (self.mouse_pos[0] - self.effect_size[0]/2, self.mouse_pos[1] - self.effect_size[1]/2))
            surface.blit(new_surface, (0,0))