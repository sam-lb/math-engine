import pygame;
from Evaluator import Evaluator;
from Errors import EvaluationError;
from helper_functions import drange;

""" Plots a real-input function (from R->R or R->C) with the real and imaginary parts drawn seperately """


SCREEN_WIDTH = 683;
SCREEN_HEIGHT = 394;
HALF_WIDTH = SCREEN_WIDTH // 2;
HALF_HEIGHT = SCREEN_HEIGHT // 2;

pygame.init();
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
pygame.display.set_caption("chicken house");


def apply(x, y):
    """ cartesian -> pygame coordinates """
    x += HALF_WIDTH;
    y = HALF_HEIGHT - y;
    return int(x), int(y);

def render_function(f):
    """ draws a function passed as a string """
    ev = Evaluator(f);

    prev_point_real = None;
    prev_point_imag = None;
    for x in drange(-8, 8.001, 0.001):
        try:
            y = ev.evaluate(x=x);
            y = complex(y);
            new_point_real = apply(x * (341/8), y.real * (197/6)); # these are just scale values, they should be precalculated
            new_point_imag = apply(x * (341/8), y.imag * (197/6)); # and stored in a var
            if prev_point_real is not None: pygame.draw.line(screen, (0, 128, 255), prev_point_real, new_point_real, 2);
            if prev_point_imag is not None: pygame.draw.line(screen, (255, 128, 0), prev_point_imag, new_point_imag, 2);
            prev_point_real = new_point_real;
            prev_point_imag = new_point_imag;
        except (ValueError, OverflowError, EvaluationError):
            prev_point_real = None;
            prev_point_imag = None;

    pygame.display.flip();
    return;

screen.fill((255,255,255));
pygame.draw.line(screen, (0,0,0), (HALF_WIDTH, 0), (HALF_WIDTH, SCREEN_HEIGHT));
pygame.draw.line(screen, (0,0,0), (0, HALF_HEIGHT), (SCREEN_WIDTH, HALF_HEIGHT));
render_function("x^0.5"); # to get the square root you have to do x^0.5 because math.sqrt raises a ValueError instead of returning a complex

running = True;
clock = pygame.time.Clock();

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False;
                break;
                
    clock.tick(10);
pygame.quit();
