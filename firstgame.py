import math
import random

import pygame
from pygame.locals import *
import Stuff
import Bouncy

pygame.init()

window_width = 1280
window_height = 720

surface = pygame.display.set_mode((window_width, window_height), RESIZABLE)
redish = (255, 182, 193)
black = (0, 0, 0)
blue = (255, 223, 0)
green = (0, 255, 0)


score = 0
high_score = 0

font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 36)

held_left = False

held_right = False

player_pos = (20, 20)

time_ms = 0

clock = pygame.time.Clock()
running = True

goal_right = True

score_file = "scores.txt"

triangle_speed = 1

bouncy_balls = [Bouncy.Bounceyball(.75, 0)]
#obsticles = [Stuff.Obstruction(.5,70, 100)]

r = random.Random()

trianle_trail = []


crash_sound = pygame.mixer.Sound("drill_something.wav")

crash_sound.play()


# Functions
def add_ball():
    # x = r.uniform(.15, .85)
    x = ((score + 1) / 0.3697) % 1.0
    x = x * .7 + .15
    bouncy_balls.append(Bouncy.Bounceyball(x, r.random()))


def draw_triangle(x, y, w, h, ew, color):
    pygame.draw.polygon(surface, color, [(x - w, y), (x + w, y), (x, y - h)], ew)

def draw_square(x, y, w, h, ew, color):
    pygame.draw.rect(surface, color, (x, y, w, h), ew)

def get_triangle_verts(x, y, w, h):
    return [(x - w, y), (x + w, y), (x, y - h)]


def draw_goal_line(color, x):
    pygame.draw.line(surface, color, (x, 0), (x, surface.get_size()[1]), 5)


def check_collision_triangle_circle(triangle_vertices, circle_position, circle_radius):
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




def save_scores(score):
    with open(score_file, "w") as file:
        file.write(str(score) + "\n")


def load_scores():
    with open(score_file, "r") as file:
        hi_score = int(file.readline())
    return hi_score


high_score = load_scores()
is_boost_held = False

# Game loop begins
while running:
    clock.tick(15)
    time_ms += 15

    time = time_ms / 1000.0

    screen_size = pygame.display.get_window_size()
    x_center = screen_size[0] / 2.0
    x_center_left = screen_size[0] / 4.0
    y_bottom = screen_size[1]

    ball_radius = max(min(min(screen_size[0], screen_size[1]) / 6.0, 120), 20)

    # surface.blit(image, (x,y))
    surface.fill(redish)

    score_text = font.render("score: " + str(score), True, (0, 0, 0, 1))
    surface.blit(score_text, (x_center, screen_size[1] / 5.0))

    high_score_text = font.render("High Score: " + str(high_score), True, (0, 0, 0, 1))
    surface.blit(high_score_text, (x_center, screen_size[1] / 10.0))

    for bouncyball in bouncy_balls:
        y_circle = y_bottom - abs(math.sin((time + bouncyball.time_offset) * 3.14 * 2)) * 200 - ball_radius
        pygame.draw.circle(surface, blue, (bouncyball.x_position * screen_size[0], y_circle), ball_radius, 5)

    #for obsticle in obsticles:
        #draw_square(obsticle.x_position * screen_size[0], y_bottom-obsticle.height,obsticle.width, obsticle.height, 2, blue)


    current_triangle_speed = 10 * triangle_speed
    if is_boost_held:
        current_triangle_speed *= 3

    trianle_trail.append(player_pos)
    if len(trianle_trail) > 8:
        trianle_trail.pop(0)

    if held_left:
        player_pos = (player_pos[0] - current_triangle_speed, player_pos[1])

    if held_right:
        player_pos = (player_pos[0] + current_triangle_speed, player_pos[1])

    player_pos = (min(max(player_pos[0], 25), screen_size[0] - 25), player_pos[1])

    player_verts = get_triangle_verts(player_pos[0], y_bottom, 23, 23)

    is_colliding = False

    for bouncyball in bouncy_balls:
        y_circle = y_bottom - abs(math.sin((time + bouncyball.time_offset) * 3.14 * 2)) * 200 - ball_radius
        is_colliding = is_colliding or check_collision_triangle_circle(player_verts, (
        bouncyball.x_position * screen_size[0], y_circle), ball_radius)

    for previous_triangle in trianle_trail:
        draw_triangle(previous_triangle[0], y_bottom, 23, 23, 2, (180,180,180))

    if is_colliding:
        draw_triangle(player_pos[0], y_bottom, 23, 23, 5, green)
        if score > high_score:
            save_scores(score)
        running = False
    else:
        draw_triangle(player_pos[0], y_bottom, 23, 23, 5, black)


    if goal_right:
        draw_goal_line(black, screen_size[0] - 30)
        if player_pos[0] > screen_size[0] - 30:
            add_ball()
            score += 1
            goal_right = False
    else:
        draw_goal_line(black, 30)
        if player_pos[0] < 30:
            add_ball()
            score += 1
            goal_right = True

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == VIDEORESIZE:
            window_width, window_height = event.size
            surface = pygame.display.set_mode((window_width, window_height), RESIZABLE)

        elif event.type == KEYDOWN:
            if event.key == K_q:
                running = False
            elif event.key == K_LEFT:
                held_left = True
            elif event.key == K_RIGHT:
                held_right = True
            elif event.key == K_LSHIFT:
                is_boost_held = True

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                held_left = False
            elif event.key == K_RIGHT:
                held_right = False
            elif event.key == K_LSHIFT:
                is_boost_held = False

pygame.display.update()
