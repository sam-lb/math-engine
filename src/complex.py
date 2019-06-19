import pygame, cmath, math;
from random import randint;

# the cmath import is so complex functions can be applied.


"""
One side of the window is a drawing canvas, the other side of the window is
the result of a complex function applied to the drawing.

The x coordinate of the input canvas serves as the real part of the input variable,
and the y coordinate serves as the imaginary part. The output side works the same way.
"""



WIDTH, HEIGHT = 1000, 500;
HWIDTH, HHEIGHT = WIDTH // 2, HEIGHT // 2;
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE);
pygame.display.set_caption("real time transformations using functions of a complex variable.");
I = 0 + 1j;

        
class Canvas(pygame.sprite.Sprite):

    """ A drawing canvas - one is used for the input and one for the output """

    def __init__(self, x, y, width=100, height=100, background=(255, 255, 255), tag="foof",
                 u_start=-8, u_stop=8, v_start=-6, v_stop=6, axes=False, function=lambda z: z, color=(255, 0, 0)):
        pygame.sprite.Sprite.__init__(self);

        self.width, self.height = width, height;
        self.hwidth, self.hheight = self.width // 2, self.height // 2;
        self.image = pygame.Surface((self.width, self.height));
        self.rect = self.image.get_rect();
        self.rect.topleft = x, y;
        
        self.set_window_bounds(u_start, u_stop, v_start, v_stop);
        self.background = background;
        self.color = color;
        self.last_point = None;
        self.function = function;
        self.tag = tag;
        self.weight = 2;

        self.reset();

    def set_window_bounds(self, u_min, u_max, v_min, v_max):
        """ set up the window and pixel scaling """
        self.u_start, self.u_stop, self.v_start, self.v_stop = u_min, u_max, v_min, v_max;
        self.u_units, self.v_units = self.u_stop - self.u_start, self.v_stop - self.v_start;
        self.u_scale, self.v_scale = self.width / self.u_units, self.height / self.v_units;

    def zoom(self, factor=1):
        """ zoom in on the canvas """
        z = lambda c: c * factor;
        self.set_window_bounds(*map(z, (self.u_start, self.u_stop, self.v_start, self.v_stop)));

    def apply(self, x, y):
        """ world coordinates -> pygame coordinates """
        return int(self.hwidth + x), int(self.hheight - y);

    def reverse(self, x, y):
        """ pygame coordinates -> world coordinates """
        return int(x - self.hwidth), int(self.hheight - y);

    def get_relative(self, x, y):
        """ gets the relative position of a screen point with respect to the canvas """
        return x - self.rect.x, y - self.rect.y;

    def get_absolute(self, x, y):
        """ gets the absolute position of a point on the canvas """
        return x + self.rect.x, y + self.rect.y;

    def plot_next(self, z, connected=True):
        """ Plot the next value and connect to the last one if connected is True """
        try:
            z = self.function(z);
            z = z.real * self.u_scale, z.imag * self.v_scale;
            point = self.apply(*z);
            if self.last_point != None and connected:
                pygame.draw.line(self.image, self.color, self.last_point, point, self.weight);
            else:
                pygame.draw.rect(self.image, self.color, (point[0], point[1], 1, 1));
            self.last_point = point;
        except Exception as e:
            print(e);
            prev_point = None;

    def reset(self):
        """ clear the screen """
        self.image.fill(self.background);

    def update(self, pos, connected=True):
        """ take in the next point and plot it """
        self.plot_next(complex(*pos), connected);

    def calculate_input(self, x, y):
        """ calculate the relative position of the input point """
        x, y = self.reverse(*self.get_relative(x, y));
        x /= self.u_scale; y /= self.v_scale;
        return x, y;

    def from_surface(self, surface):
        """ transform an entire surface (usually an image) """
        self.reset();
        if self.tag == "input":
            self.image.blit(surface, (0, 0));
            return;
        width, height = surface.get_width(), surface.get_height();
        last_point = None;
        for u in range(width):
            for v in range(height):
                color = surface.get_at((int(u), int(v)));
                x, y = self.reverse(u, v);
                x /= self.u_scale; y /= self.v_scale;
                try:
                    z = self.function(complex(x, y));
                except Exception as e:
                    continue;
                z = z.real * self.u_scale, z.imag * self.v_scale;
                x, y = self.apply(*z);
                pygame.draw.rect(self.image, color, (x, y, 1, 1));
                if last_point is not None:
                    pygame.draw.line(self.image, color, (x, y), last_point);
                last_point = (x, y);

def grid_(planes, x_dist=20, y_dist=20):
    """ draw a grid to show how the function transforms the input plane """
    
    def clear():
        color = (0, 0, randint(0, 255));
        for plane in planes:
            plane.last_point = None;
            plane.color = color;

    data, inp = [], planes.sprites()[0];
    for plane in planes:
        data.append((plane.color, plane.weight));
        plane.color = (0, 0, 0);
        plane.weight = 1;
    for x in range(x_dist, inp.width, x_dist):
        for y in range(inp.height):
            planes.update(inp.calculate_input(x, y));
        clear();
    for b in range(y_dist, inp.height, y_dist):
        for a in range(inp.width):
            planes.update(inp.calculate_input(a, b));
        clear();
    for i, plane in enumerate(planes):
        plane.color = data[i][0];
        plane.weight = data[i][1];

if __name__ == "__main__":
    
    running, drawing = True, False;
    Q = 500;
    clock = pygame.time.Clock();
    canvases = pygame.sprite.Group();
    input_plane = Canvas(0, 0, Q, Q, tag="input");
    output_plane = Canvas(Q, 0, Q, Q, background=(255, 230, 255), tag="output", function=lambda z: 2*z, color=(32, 32, 255));
    # to set the function that is used, change the lambda function right        <------here----------> (the function keyword argument)
    canvases.add(input_plane);
    canvases.add(output_plane);

    #grid = pygame.transform.scale(pygame.image.load("resources/elephant.jpg").convert(), (Q, Q));
    #input_plane.from_surface(grid);
    #output_plane.from_surface(grid);

    canvases.draw(screen);
    grid_(canvases, 14, 14);

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
                break;
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False;
                    break;
                elif event.key == pygame.K_r:
                    input_plane.reset();
                    output_plane.reset();
                elif 49 <= event.key <= 57:
                    input_plane.weight = event.key - 48;
                    output_plane.weight = event.key - 48;
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True;
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False;
                input_plane.last_point = None;
                output_plane.last_point = None;
            elif event.type == pygame.MOUSEMOTION and drawing:
                canvases.update(input_plane.calculate_input(*pygame.mouse.get_pos()));
        screen.fill((0, 200, 32));
        canvases.draw(screen);
        pygame.display.flip();
        clock.tick(200);
    pygame.quit();
