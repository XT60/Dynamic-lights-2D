from numpy import Infinity
import pygame
import Config
import math
import sortedcontainers

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
        
def find_index(sorted_points, values:list, index, starting_point):
    ret = [None for _ in range(len(values))]
    length = len(values)
    for p in range(1, len(sorted_points)):
        for i, value in enumerate(values):
            if value != None:
                if starting_point+p < len(sorted_points) and value == sorted_points[starting_point+p][index]:
                    ret[i] = (starting_point+p)
                    if length == 1:
                        return ret
                    else:
                        length -= 1
                        values[i] = None
                if starting_point-p >= 0 and value == sorted_points[starting_point-p][index]:
                    ret[i] = (starting_point-p)
                    if length == 1:
                        return ret
                    else:
                        length -= 1
                        values[i] = None

def round2 (arr):
    if arr != None:
        return tuple(map(lambda x: round(x, 2), arr))





class light_handling:
    def __init__(self, walls, points) -> None:
        self.walls = walls
        self.polygon = []
        self.points = points
        self.pressed = False
        self.mouse_pos = None
        self.rays = []
        self.radius = max(Config.WINDOW_SIZE) * 2
        #self.generate_wall_ends()
        self.multiplier = 1.5
        self.effect_size = tuple(map( lambda x: x*self.multiplier, Config.WINDOW_SIZE))
        self.light_effect = pygame.transform.scale(pygame.image.load('light_effect.png'), self.effect_size).convert() 


    def update_data(self, walls, points):
        self.walls = walls
        self.points = points


    def extract_polygon(self):
        self.polygon.clear()
        sorted_points = sortedcontainers.SortedList(key = lambda x: x[0])            # [angle, point]

        ### filling sorted_points
        for pos in self.points:
            point = self.points[pos]
            vec = (pos[0] - self.mouse_pos[0], pos[1] - self.mouse_pos[1])
            angle = math.atan2(vec[1], vec[0])
            if abs(angle) == math.pi:
                #sorted_points.add((-math.pi, point))
                sorted_points.add((math.pi, point))
            else:
                sorted_points.add((angle, point))
            

        curr_walls = set()
        top_wall = None

        ### checking how many walls are in curr_walls at start
        angle = -math.pi
        vec1 = (self.radius * math.cos(angle), self.radius * math.sin(angle))                       # vector from mouse_button to edge end_point
        min_dist = Infinity
        closest_point = None
        for wall in self.walls:
            vec2 = (wall.end_pos[0] - wall.start_pos[0], wall.end_pos[1] - wall.start_pos[1])       # vector from edge_start to edge_end
            den = vec1[0] * vec2[1] - vec2[0] * vec1[1]
            if round(den, 2) != 0 and (wall.start_pos[1] < self.mouse_pos[1] or wall.end_pos[1] < self.mouse_pos[1]):
                s = round((vec1[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec1[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                t = round((vec2[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec2[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                if (0 <= round(s, 3) <= 1 and 0 <= round(t,3) <= 1):
                    curr_walls.add(wall)
                    if t < min_dist:
                        x = self.mouse_pos[0] + (t * vec1[0])
                        y = self.mouse_pos[1] + (t * vec1[1])
                        closest_point = (x, y)
                        min_dist = t
                        top_wall = wall
        self.polygon.append(round2(closest_point))
                

        for angle, point in sorted_points:
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

            min_dist = Infinity
            closest_point = None
            closest_wall = None
            vec1 = (self.radius * math.cos(angle), self.radius * math.sin(angle))     # vector from mouse_button to edge end_point
            for wall in curr_walls:
                vec2 = (wall.end_pos[0] - wall.start_pos[0], wall.end_pos[1] - wall.start_pos[1])                # vector from edge_start to edge_end
                den = vec1[0] * vec2[1] - vec2[0] * vec1[1]
                if den != 0:
                    s = round((vec1[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec1[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    t = round((vec2[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec2[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    if (0 <= s <= 1 and 0 <= t <= 1):
                        if t < min_dist:
                            x = self.mouse_pos[0] + (t * vec1[0])
                            y = self.mouse_pos[1] + (t * vec1[1])
                            closest_point = (x, y)
                            min_dist = t
                            closest_wall = wall

            ### new walls handling
            n_min_dist = Infinity
            n_closest_point = None
            n_closest_wall = None             
            for wall in new_buffer:
                vec2 = (wall.end_pos[0] - wall.start_pos[0], wall.end_pos[1] - wall.start_pos[1])                # vector from edge_start to edge_end
                den = vec1[0] * vec2[1] - vec2[0] * vec1[1]
                if den != 0:
                    s = round((vec1[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec1[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    t = round((vec2[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec2[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    if (0 <= s <= 1 and 0 <= t <= 1):
                        if t < n_min_dist:
                            x = self.mouse_pos[0] + (t * vec1[0])
                            y = self.mouse_pos[1] + (t * vec1[1])
                            n_closest_point = (x, y)
                            n_min_dist = t
                            n_closest_wall = wall

            ### new removed handling
            r_min_dist = Infinity
            r_closest_point = None
            r_closest_wall = None             
            for wall in rm_buffer:
                vec2 = (wall.end_pos[0] - wall.start_pos[0], wall.end_pos[1] - wall.start_pos[1])                # vector from edge_start to edge_end
                den = vec1[0] * vec2[1] - vec2[0] * vec1[1]
                if den != 0:
                    s = round((vec1[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec1[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    t = round((vec2[1] * (wall.start_pos[0] - self.mouse_pos[0]) - vec2[0] * (wall.start_pos[1] - self.mouse_pos[1])) / den, 5)
                    if (0 <= s <= 1 and 0 <= t <= 1):
                        if t < n_min_dist:
                            x = self.mouse_pos[0] + (t * vec1[0])
                            y = self.mouse_pos[1] + (t * vec1[1])
                            r_closest_point = (x, y)
                            r_min_dist = t
                            r_closest_wall = wall

            closest_point = round2(closest_point)
            n_closest_point = round2(n_closest_point)
            r_closest_point = round2(r_closest_point)
            
            k = min(min_dist, n_min_dist, r_min_dist)
            if k == min_dist:
                if top_wall != closest_wall:
                    self.polygon.append(closest_point)
                    top_wall = closest_wall
            elif k == r_min_dist :   
                self.polygon.append(r_closest_point)
                if closest_point != None and point.wall_end in rm_buffer and point.wall_start in rm_buffer:
                    self.polygon.append(closest_point)
                top_wall = r_closest_wall
            elif k == n_min_dist:
                if closest_point != None and point.wall_end in new_buffer and point.wall_start in new_buffer:
                    self.polygon.append(closest_point)
                self.polygon.append(n_closest_point)
                top_wall = n_closest_wall
            
            curr_walls.update(new_buffer)
            curr_walls -= rm_buffer
        
        #elf.polygon.append(self.polygon[0])



    def update_variables(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            #self.mouse_pos = (800, 300)
            self.mouse_pos = mouse_pos
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