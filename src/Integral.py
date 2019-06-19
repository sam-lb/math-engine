import pygame, math;
from Evaluator import Evaluator;
from Errors import EvaluationError;
from helper_functions import drange;


""" approximates the signed area under a curve by using a Riemann sum """


pygame.init();
WIDTH, HEIGHT = 600, 600;
HWIDTH, HHEIGHT = WIDTH // 2, HEIGHT // 2;
screen = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("integral.py");
pygame.key.set_repeat(100, 50);


# stuff that is entered (OK to change)
x_start, x_stop = -4, 4;
y_start, y_stop = -4, 4;
background_color = (255, 255, 255);
axis_color = (0, 0, 0);
axis_weight = 3
function_color = (100, 155, 100);
function_weight = 2;
rectangle_color = (200, 200, 255);
rectangle_border_color = (255, 200, 112);
rectangles_per_unit = 4;
precision = 0.01;
continuity_threshold = 100;

# stuff that is calculated (do not change)
units_x, units_y = x_stop - x_start, y_stop - y_start;
x_scale, y_scale = WIDTH / units_x, HEIGHT / units_y;
rectangle_frequency = 1 / rectangles_per_unit;
rectangle_width = x_scale / rectangles_per_unit;


def to_pygame(x, y):
    """ scaled cart -> pygame """
    return x + HWIDTH, HHEIGHT - y;

def scale(x, y):
    """ unscaled cart -> scaled cart """
    return x * x_scale, y * y_scale;

def clear_screen():
    """ clear the screen """
    screen.fill(background_color);

def draw_axes():
    """ draw the axes """
    pygame.draw.line(screen, axis_color, (HWIDTH, 0), (HWIDTH, HEIGHT), axis_weight);
    pygame.draw.line(screen, axis_color, (0, HHEIGHT), (WIDTH, HHEIGHT), axis_weight);

def plot_function(function, rectangles=True):
    """ plot a function and it's rectangles (if enabled) """
    ev = Evaluator(function);
    prev_point, area = None, 0;
    for x in drange(x_start, x_stop+precision, precision):
        try:
            y = ev.evaluate(x=x);
            new_point = to_pygame(*scale(x, y));
            if prev_point is not None:
                if math.hypot(new_point[0] - prev_point[0], new_point[1] - prev_point[1]) < continuity_threshold:
                    pygame.draw.line(screen, function_color, prev_point, new_point, function_weight);
            if rectangles and not round(x, 2) % rectangle_frequency:
                pygame.draw.rect(screen, rectangle_color, (new_point[0], min(new_point[1], HHEIGHT), rectangle_width, abs(y * y_scale)));
                pygame.draw.rect(screen, rectangle_border_color, (new_point[0], min(new_point[1], HHEIGHT), rectangle_width, abs(y * y_scale)), 1);
                area += y * (rectangle_width / x_scale);
            prev_point = new_point;
        except EvaluationError:
            prev_point = None;
    if rectangles:
        return area;
    else:
        return None;

running = True;
clock = pygame.time.Clock();
fps = 30;

clear_screen();
draw_axes();


""" press space to enter a function """

while running:
    try:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
                break;
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False;
                    break;
                elif event.key == pygame.K_SPACE:
                    function = input("Enter a function: ");
                    r = int(input("Rectangles? 0/1: "));
                    clear_screen();
                    draw_axes();
                    v = plot_function(function, r);
                    if v: print(v);
        pygame.display.flip();
        clock.tick(fps);
        
    except Exception as e:
        pygame.quit();
        raise e;
pygame.quit();
