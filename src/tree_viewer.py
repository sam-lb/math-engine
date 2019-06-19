from Parser import Parser;
from Tokenizer import Operation;
import pygame;

pygame.init();
screen = pygame.display.set_mode((1000, 600));
pygame.display.set_caption("tree viewer.");

factor = 1.5;

""" generates a visual for a parse tree using nodes and edges """


def create_text_surface(text):
    return pygame.font.SysFont("arial", 16).render(text, 1, (255, 0, 0));


class Node():

    """ class for a node that holds a single token """

    def __init__(self, letter, x, y):
        self.letter = letter;
        self.x, self.y = int(x), int(y);
        self.fontsurf = create_text_surface(self.letter);
        self.fx, self.fy = x - (self.fontsurf.get_width() // 2), y - (self.fontsurf.get_height() // 2);

    def draw(self):
        """ draw the node to the screen """
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 16)
        screen.blit(self.fontsurf, (self.fx, self.fy));

class Line():

    """ class for an edge that connects two tokens """

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = map(int, (x1, y1, x2, y2));

    def draw(self):
        """ draw the edge to the screen """
        pygame.draw.line(screen, (255, 255, 255), (self.x1, self.y1), (self.x2, self.y2));
        

def generate_nodes(tree, x=500, y=16, h=200):
    """ generate the nodes and the lines for a parse tree """
    nodes,lines = [],[];
    if isinstance(tree, Operation):
        nodes.append(Node(tree.string, x, y));
        if len(tree.args) == 1:
            lines.append(Line(x, y, x, y+60));
            n, l = generate_nodes(tree.args[0], x,y+60,h);
            nodes += n; lines += l;
        else:
            h = max(20, h);
            lines += [Line(x, y, x-h, y+60), Line(x, y, x+h, y+60)];
            n, l = generate_nodes(tree.args[0],x-h,y+60,h/factor);
            nodes += n; lines += l;
            n, l = generate_nodes(tree.args[1],x+h,y+60,h/factor);
            nodes += n; lines += l;
    else:
        return [Node(str(tree), x, y)], [];
    return nodes,lines;

running = True;
clock = pygame.time.Clock();
#tr = Parser("1/sqrt(2pi)exp(-x^2)");               # <-- some other interesting ones
#tr = Parser("a*b*c*d*e");                          # <--
tr = Parser("sin(x^abs(x))/2^((x^abs(x)-pi/2)/pi)"); # put any function here
tree = tr.tree;
nodes,lines = generate_nodes(tree);

while running:
    screen.fill((0,0,0));
    for line in lines:
        line.draw();
    for node in nodes:
        node.draw();
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False;
                break;
            elif event.key == pygame.K_SPACE:
                try:
                    nodes, lines = generate_nodes(Parser(input("Enter a function: ")).tree);
                except Exception as e:
                    nodes, lines = [], [];
                    print(e);
    clock.tick(10);
    pygame.display.update();
pygame.quit();
