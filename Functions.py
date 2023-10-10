import pygame
import math
from game2 import surface, score_file


def draw_triangle(self,x, y, w, h, ew, color):
    pygame.draw.polygon(surface, color, [(x - w, y), (x + w, y), (x, y - h)], ew)

def get_triangle_verts(x, y, w, h):
    return [(x - w, y), (x + w, y), (x, y - h)]

def draw_goal_line(self,color, x):
    pygame.draw.line(surface, color, (x, 0), (x, surface.get_size()[1]), 5)

def check_collision_triangle_circle(self, triangle_vertices, circle_position, circle_radius):
    for i in range(len(triangle_vertices)):
        p1 = triangle_vertices[i]
        p2 = triangle_vertices[(i + 1) % len(triangle_vertices)]

        # Calculate the distance between the circle's center and the line segment
        v = (p2[0] - p1[0], p2[1] - p1[1])
        w = (circle_position[0] - p1[0], circle_position[1] - p1[1])
        dot_product = v[0] * w[0] + v[1] * w[1]
        square_length = v[0] * v[0] + v[1] * v[1]
        t = max(0, min(1, dot_product / square_length))
        closest_point = (p1[0] + t * v[0], p1[1] + t * v[1])
        distance = math.sqrt(
            (circle_position[0] - closest_point[0]) ** 2 + (circle_position[1] - closest_point[1]) ** 2)

        # Check if the distance is less than the circle's radius
        if distance < circle_radius:
            return True
    return False

def save_scores(self,score):
    with open(score_file, "w") as file:
        file.write(str(score) + "\n")

def load_scores(self):
    with open(score_file, "r") as file:
        hi_score = int(file.readline())
    return hi_score