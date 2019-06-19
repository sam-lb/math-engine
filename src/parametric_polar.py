import pygame, math;
from Evaluator import Evaluator;
from Errors import EvaluationError;
from helper_functions import drange;


"""
Plots a 'parametric polar' equation which is something I made up. It's really what it sounds like.
It just means that the radius and the angle theta between the radius and the positive x axis
are given by parametric functions of the parameter u.
"""


SCREEN_WIDTH = 1366//2; # /1366
SCREEN_HEIGHT = 768//2; # /768
HALF_WIDTH = int(SCREEN_WIDTH / 2);
HALF_HEIGHT = int(SCREEN_HEIGHT / 2);

pygame.init();
pygame.key.set_repeat(100, 50);


def apply(x, y):
    """ cartesian -> pygame """
    x += HALF_WIDTH;
    y = HALF_HEIGHT - y;
    return int(x), int(y);

def vector_by_direction(radians, hyp):
    """ get a vector by angle and magnitude """
    x = hyp * (math.cos(radians));
    y = hyp * (math.sin(radians));
    return x, y;

def render_function(radius, theta, color=(0, 0, 0), start=-8*math.pi, stop=8*math.pi, precision=0.001):
    """ draw a 'parametric polar' function """
    radius, theta = Evaluator(radius), Evaluator(theta);
    
    prev_point = None;
    for j in drange(start, stop, precision):
        try:
            r_j, t_j = radius.evaluate(u=j), theta.evaluate(u=j);
            x, y = vector_by_direction(t_j, r_j);
            new_point = apply(x * 25, y * 25);
            if prev_point != None and abs(prev_point[1] - new_point[1]) <= 200:
                pygame.display.update(pygame.draw.line(screen, color, prev_point, new_point, 2));
            prev_point = new_point;
        except (EvaluationError, TypeError):
            prev_point = None;
        pygame.event.get();
    return;

def start():
    """ clear the screen """
    screen.fill((255, 255, 255));
    pygame.display.flip();

pygame.init();
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE);
pygame.display.set_caption("Parametric Polar Equations");
clock = pygame.time.Clock();

running = True;
start();

"""
some observations.

1. if r=c and t=u, a circle will be drawn with radius c.
2. the functions r = u^2 + f(u)^2 and t = atan(f(u)/u) will draw the function f.
3. the functions r = 13sin(1/u) and t = u kind of draw a mouse face.

"""

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False;
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False;
                break;
            elif event.key == pygame.K_SPACE:
                start();
                render_function(input("r > "), input("t > "));
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h;
            HALF_WIDTH, HALF_HEIGHT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2;
            old = pygame.transform.scale(screen, (SCREEN_WIDTH, SCREEN_HEIGHT));
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE);
            screen.blit(old, (0, 0));
            pygame.display.flip();
    clock.tick(10);
pygame.quit();
