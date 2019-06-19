import pygame;
from Evaluator import Evaluator;
from Errors import EvaluationError;
from Derivative import derive_tree;
from Simplifier import simplify;
from helper_functions import drange;

""" Plotter using the expression evaluator """


SCREEN_WIDTH = 1366; # /1366 <- full resolution on my device
SCREEN_HEIGHT = 768; # /768 <- 
HALF_WIDTH = SCREEN_WIDTH // 2;
HALF_HEIGHT = SCREEN_HEIGHT // 2;
GR = 1/4; # gradient constant - decrease for a slower gradient

pygame.init();
pygame.key.set_repeat(100, 50);


sgn = lambda x: int(x / abs(x));                           # get the sign of a number (not zero). zero does not have a sign.
constrain = lambda n, min_, max_: max(min(n, max_), min_); # constrain a value between a maximum and a minimum


def gradient(color1=(200, 0, 200), color2=(0, 0, 0)):
    """ get a iterator of RGB colors between two colors """
    r1, g1, b1 = color1;
    r2, g2, b2 = color2;
    if r1 < r2: rstep = GR;
    else: rstep = -GR;
    if g1 < g2: gstep = GR;
    else: gstep = -GR;
    if b1 < b2: bstep = GR;
    else: bstep = -GR;

    yield color1;

    while (r1, g1, b1) != (r2, g2, b2):
        if r1 != r2: r1 += rstep;
        if g1 != g2: g1 += gstep;
        if b1 != b2: b1 += bstep;
        yield (r1, g1, b1);

    rstep, gstep, bstep = -rstep, -gstep, -bstep;
    r1, g1, b1 = color1;

    while (r1, g1, b1) != (r2, g2, b2):
        if r1 != r2: r2 += rstep;
        if g1 != g2: g2 += gstep;
        if b1 != b2: b2 += bstep;
        yield (r2, g2, b2);

def calculate_offset(origin_x, origin_y):
    """ center everything at the origin """
    return origin_x - HALF_WIDTH, origin_y - HALF_HEIGHT;

def apply(x, y, x_offset=0, y_offset=0):
    """ cartesian -> pygame """
    x += HALF_WIDTH + x_offset;
    y = HALF_HEIGHT - y + y_offset;
    return int(x), int(y);

def reverse(x, y, scx, scy):
    """ pygame -> UNSCALED cartesian """
    return (x - HALF_WIDTH) / scx, (HALF_HEIGHT - y) / scy;

def render_function(window, f, color, settings, deriv=False):
    """ draw a function """
    if deriv:
        ev = Evaluator("0");
        try:
            ev.parser.tree = simplify(derive_tree(f));
        except:
            ev.parser.tree = derive_tree(f);
    else:
        ev = Evaluator(f);

    prev_point = None;
    for x in drange(settings.start_x, settings.stop_x + settings.precision, settings.precision):
        try:
            new_point = apply(x * settings.x_scale, ev.evaluate(x=x) * settings.y_scale, settings.x_offset, settings.y_offset);
            if prev_point != None and abs(prev_point[1] - new_point[1]) <= 200:
                pygame.draw.line(window, color, prev_point, new_point, settings.weight);
            prev_point = new_point;
        except (EvaluationError, TypeError):
            prev_point = None;
    return;

def vertical_line(window, x, settings):
    """ draw a vertical line. (no function of x can do this) """
    start_point = apply(x * settings.x_scale, settings.num_units_y / 2 * settings.y_scale);
    end_point = start_point[0], start_point[1] + SCREEN_HEIGHT;
    pygame.draw.line(window, (0, 255, 255), start_point, end_point, settings.weight);
    return;

def render_point(window, x, y, color=(0, 0, 0), x_scale=50, y_scale=50):
    """ draw a large point """
    pygame.draw.circle(window, color, apply(x * x_scale, y * y_scale), 10); 

def draw_axes(window, origin_x, origin_y):
    """ draw the axes """
    pygame.draw.line(window, (0, 0, 0), (origin_x, origin_y), (origin_x, -SCREEN_HEIGHT), 3); # origin -> top
    pygame.draw.line(window, (0, 0, 0), (origin_x, origin_y), (origin_x, SCREEN_HEIGHT), 3);  # origin -> bottom
    pygame.draw.line(window, (0, 0, 0), (origin_x, origin_y), (-SCREEN_WIDTH, origin_y), 3);  # origin -> left
    pygame.draw.line(window, (0, 0, 0), (origin_x, origin_y), (SCREEN_WIDTH, origin_y), 3);   # origin -> right

def draw_gridlines(window, x_scale, y_scale, lines_per_unit=1):
    """ draw the gridlines """
    for x in drange(HALF_WIDTH, 0, -x_scale/lines_per_unit):
        pygame.draw.line(window, (128, 128, 128), (x, 0), (x, SCREEN_HEIGHT));
    for x in drange(HALF_WIDTH, SCREEN_WIDTH, x_scale/lines_per_unit):
        pygame.draw.line(window, (128, 128, 128), (x, 0), (x, SCREEN_HEIGHT));
        
    for y in drange(HALF_HEIGHT, 0, -y_scale/lines_per_unit):
        pygame.draw.line(window, (128, 128, 128), (0, y), (SCREEN_WIDTH, y));
    for y in drange(HALF_HEIGHT, SCREEN_HEIGHT, y_scale/lines_per_unit):
        pygame.draw.line(window, (128, 128, 128), (0, y), (SCREEN_WIDTH, y));

def set_up(window, settings):
    """ set up the drawing window """
    window.fill(settings.background);
    if settings.gridlines: draw_gridlines(window, settings.x_scale, settings.y_scale, settings.lines_per_unit);
    if settings.axes: draw_axes(window, settings.origin_x, settings.origin_y);
    

class PlotSettings():

    """ customization for the plot """

    def __init__(self, start_x, stop_x, start_y, stop_y, axes, gridlines, lines_per_unit, background, precision, weight):
        self.set_window_bounds(start_x, stop_x, start_y, stop_y);
        self.axes, self.gridlines = axes, gridlines;
        self.lines_per_unit = lines_per_unit;
        self.background = background;
        self.precision = precision;
        self.weight = weight;

    def set_window_bounds(self, start_x, stop_x, start_y, stop_y):
        """ set the bounds and pixels scales """
        self.start_x, self.stop_x, self.start_y, self.stop_y = start_x, stop_x, start_y, stop_y;
        self.num_units_x, self.num_units_y = self.stop_x - self.start_x, self.stop_y - self.start_y;
        self.x_scale, self.y_scale = HALF_WIDTH / (self.num_units_x / 2), HALF_HEIGHT / (self.num_units_y / 2);
        self.origin_x, self.origin_y = self.x_scale * -self.start_x, self.y_scale * -self.start_y;
        self.x_offset, self.y_offset = calculate_offset(self.origin_x, self.origin_y);

    def zoom(self, factor=1):
        """ zoom by a factor """
        # factors under 1 zoom in, factors above 1 zoom out
        z = lambda c: c * factor;
        self.set_window_bounds(z(self.start_x), z(self.stop_x), z(self.start_y), z(self.stop_y));
        

running = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
pygame.display.set_caption("Plot");
clock = pygame.time.Clock();

# Settings
"""
start_x:        x value to start plotting
stop_x:         x value to stop plotting
start_y:        y value to start plotting
stop_y:         y value to stop plotting
axes:           True = axes on, False = axes off
gridlines:      True = gridlines on, False = gridlines off
lines_per_unit: number of gridlines per unit
background:     background color of the graph
precision:      accuracy of the graph. lower values have higher accuracy, but take longer
weight:         width of plot line
"""

start_x, stop_x = -8, 8; #
start_y, stop_y = -6, 6; #
axes = True;
gridlines = False;
lines_per_unit = 1;
background = (255, 255, 255);
precision = 0.01;
weight = 4;
###

# Plot setup
settings = PlotSettings(start_x, stop_x, start_y, stop_y, axes, gridlines, lines_per_unit, background, precision, weight);
plot = lambda f, color: render_function(screen, f, color, settings);                   # plot a function shortcut
plot_deriv = lambda f, color: render_function(screen, f, color, settings, deriv=True); # plot the derivative of a function shortcut
set_up(screen, settings);
###

# Plotting goes here: see graphs.txt for example functions.
###

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False;
                break;
            elif event.key == pygame.K_LEFT:
                settings.set_window_bounds(settings.start_x - 1, settings.stop_x - 1, settings.start_y, settings.stop_y);
            elif event.key == pygame.K_RIGHT:
                settings.set_window_bounds(settings.start_x + 1, settings.stop_x + 1, settings.start_y, settings.stop_y);
            elif event.key == pygame.K_UP:
                settings.set_window_bounds(settings.start_x, settings.stop_x, settings.start_y - 1, settings.stop_y - 1);
            elif event.key == pygame.K_DOWN:
                settings.set_window_bounds(settings.start_x, settings.stop_x, settings.start_y + 1, settings.stop_y + 1);
            elif event.key == pygame.K_EQUALS:
                settings.zoom(3/4);
            elif event.key == pygame.K_MINUS:
                settings.zoom(4/3);
                
    clock.tick(30);
    set_up(screen, settings);
    #plot("0.25(3x^4-2x^3-2x^2+x+1)", (255, 0, 0));
    #plot_deriv("0.25(3x^4-2x^3-2x^2+x+1)", (0, 0, 255));
    plot("4sin(x^abs(x))/2^((x^abs(x)-pi/2)/pi)", (55, 200, 100));
    pygame.display.flip();

pygame.quit();
