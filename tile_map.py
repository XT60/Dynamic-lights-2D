import Config
import pygame
NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3

class Wall:
    def __init__(self, start_pos, end_pos) -> None:
        self.start_pos = list(start_pos)
        self.end_pos = list(end_pos)


class Cell:
    def __init__(self, exist) -> None:
        self.exist = exist                          # determines if it is a wall or not
        self.has_wall = [False for _ in range (4)]  # determines if cell has wall in certain direction
        self.wall_i = [None for _ in range (4)]     # holds wall's indexes


class Point:
    def __init__(self, wall_start = None, wall_end = None) -> None:
        self.wall_start = wall_start 
        self.wall_end = wall_end     


class Tile_map:
    def __init__(self) -> None:
        self.walls = []    
        self.points = {}        # {pos : point}     
        self.cell_map = self.convert_to_cell_map(Config.TILEMAP)
        self.extract_walls()

        pygame.font.init()
        self.font = pygame.font.SysFont('FutureMillennium', 24, False, False)
        self.text = self.font.render('Wall_count: ' + str(len(self.walls)), False, (30,144,255))


    def get_cell(self, x, y):
        if 0 <= x < len(self.cell_map[0]) and 0 <= y < len(self.cell_map):
            return self.cell_map[y][x]
        else:
            return None


    def convert_to_cell_map(self, tile_map):
        return [[Cell(val == 0) for val in tile_map[y]] for y ,row in enumerate(tile_map)]


    def reset_cell_map(self):
        for row in self.cell_map:
            for curr_cell in row:
                curr_cell.has_wall = [False for _ in range (4)]
                curr_cell.wall_i = [None for _ in range (4)]


    def clear_data_structues(self):
        self.reset_cell_map()
        self.walls.clear()
        self.points.clear()


    def extract_walls(self):
        self.clear_data_structues()

        # adding map borders
        self.walls.append(Wall((Config.WINDOW_SIZE[0], 0), (0,0)))
        self.walls.append(Wall((Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1]), (Config.WINDOW_SIZE[0], 0)))
        self.walls.append(Wall( (0, Config.WINDOW_SIZE[1]), (Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1])))
        self.walls.append(Wall((0,0), (0, Config.WINDOW_SIZE[1])))

        # format of walls:
        #
        #                e             s                s - start
        #                ---------------                e - end
        #            s  |               |  e
        #               |               |   
        #               |               |
        #            e  |               |  s
        #                ---------------
        #                s             e

        for y, row in enumerate(self.cell_map):
            for x, curr_cell in enumerate(row):
                if curr_cell.exist:
                    n = self.get_cell(x, y-1)
                    e = self.get_cell(x+1, y)
                    w = self.get_cell(x-1, y)
                    s = self.get_cell(x, y+1)

                    # North cell
                    if n != None and not n.exist:
                        curr_cell.has_wall[NORTH] = True
                        if w != None and w.has_wall[NORTH]:
                            i = w.wall_i[NORTH]
                            curr_cell.wall_i[NORTH] = i
                            self.walls[i].start_pos[0] += Config.TILE_SIZE
                        else:
                            curr_cell.wall_i[NORTH] = len(self.walls)
                            start_x = x*Config.TILE_SIZE 
                            start_y = y*Config.TILE_SIZE
                            self.walls.append(Wall((start_x + Config.TILE_SIZE, start_y), (start_x, start_y)))
                        
                    # East cell
                    if e != None and not e.exist:
                        curr_cell.has_wall[EAST] = True
                        if n != None and n.has_wall[EAST]:
                            i = n.wall_i[EAST]
                            curr_cell.wall_i[EAST] = i
                            self.walls[i].start_pos[1] += Config.TILE_SIZE
                        else:
                            curr_cell.wall_i[EAST] = len(self.walls)
                            start_x = (x + 1)*Config.TILE_SIZE 
                            start_y = y*Config.TILE_SIZE
                            self.walls.append(Wall((start_x, start_y + Config.TILE_SIZE), (start_x, start_y)))

                    # West cell
                    if w != None and not w.exist:
                        curr_cell.has_wall[WEST] = True
                        if n != None and n.has_wall[WEST]:
                            i = n.wall_i[WEST]
                            curr_cell.wall_i[WEST] = i
                            self.walls[i].end_pos[1] += Config.TILE_SIZE
                        else:
                            curr_cell.wall_i[WEST] = len(self.walls)
                            start_x = x*Config.TILE_SIZE 
                            start_y = y*Config.TILE_SIZE
                            self.walls.append(Wall((start_x, start_y), (start_x, start_y + Config.TILE_SIZE)))

                    # South cell
                    if s != None and not s.exist:
                        curr_cell.has_wall[SOUTH] = True
                        if w != None and w.has_wall[SOUTH]:
                            i = w.wall_i[SOUTH]
                            curr_cell.wall_i[SOUTH] = i
                            self.walls[i].end_pos[0] += Config.TILE_SIZE
                        else:
                            curr_cell.wall_i[SOUTH] = len(self.walls)
                            start_x = x*Config.TILE_SIZE
                            start_y = (y+1)*Config.TILE_SIZE
                            self.walls.append(Wall((start_x, start_y), (start_x + Config.TILE_SIZE, start_y)))

        # formating gathered wall data to generate self.points data structure
        for wall in self.walls:
            end_pos = tuple(wall.end_pos)
            start_pos = tuple(wall.start_pos)
            if start_pos not in self.points:
                self.points[start_pos] = Point(wall_start = wall)
            else:
                self.points[start_pos].wall_start = wall
            if end_pos not in self.points:
                self.points[end_pos] = Point(wall_end = wall)
            else:
                self.points[end_pos].wall_end = wall


    def update_variables(self, mouse_pos, mouse_pressed, light_object):
        if mouse_pressed[2]:
            x = mouse_pos[0] // Config.TILE_SIZE
            y = mouse_pos[1] // Config.TILE_SIZE
            if 0 <= x < len(self.cell_map[0]) and 0 <= y < len(self.cell_map):
                self.cell_map[y][x].exist = True
                self.extract_walls()
                light_object.update_data(self.walls, self.points)
                self.text = self.font.render('Wall_count: ' + str(len(self.walls)), False, (30,144,255))

    
    def draw(self, surface:pygame.Surface):
        for wall in self.walls:
            pygame.draw.line(surface, (150,150,150), wall.start_pos, wall.end_pos , 3)
        surface.blit(self.text, (0,0))
            
                




