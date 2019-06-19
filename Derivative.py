from Parser import Parser;
from Tokenizer import Number, Unknown, Operation;
from Errors import DerivativeError;
from Simplifier import to_infix;
from data import operations, derivatives;

"""
tools for finding the derivative of a function
"""


def d(f, var="x"):
    """ takes a parse tree and returns the parse tree for the derivative """
    # a lot of recursion, a lot of pain.
    if isinstance(f, Operation):
        if f.string in "+-" and len(f.args) == 2:
            return Operation(operations[f.string], [d(f.args[0], var), d(f.args[1], var)], None, f.string);
        elif f.string == "*":
            return Operation(operations["+"], [Operation(operations["*"], [d(f.args[0], var), f.args[1]], None, "*"),
                                               Operation(operations["*"], [d(f.args[1], var), f.args[0]], None, "*")],
                             None, "+");
        elif f.string == "/":
            return Operation(operations["/"], [Operation(operations["-"], [Operation(operations["*"], [d(f.args[0], var), f.args[1]], None, "*"),
                                                                           Operation(operations["*"], [d(f.args[1], var), f.args[0]], None, "*")],
                                                         None, "-"),
                                               Operation(operations["*"], [f.args[1], f.args[1]], None, "*")],
                             None, "/");
        elif f.string == "^":
            a, b = f.args;
            return Operation(operations["*"], [Operation(operations["*"], [d(a, var), b], None, "*"),
                                               Operation(operations["^"], [a, Number(b.value-1)], None, "^")], None, "*");
        elif f.string == "-":
            return Operation(operations["~"], [d(f.args[0], var)], None, "~");
        else:
            return Operation(operations["*"], [Operation(derivatives[f.string], f.args, None, "SPFUNC"), d(f.args[0], var)], None, "*");
    elif isinstance(f, Unknown):
        if f.name == var:
            return Parser("1").tree;
        else:
            raise DerivativeError("Cannot explicitly take derivative of symbol \"{}\" w.r.t. {}".format(f.name, var));
    elif isinstance(f, Number):
        return Parser("0").tree;
    
    return tree;

def derive_tree(f,var="x"):
    """ takes a function in a string and returns the derivative as a parse tree """
    return d(Parser(f).tree, var);

def derive(f, var="x"):
    """ takes a function in a string and returns the derivative as a string """
    return to_infix(derive_tree(f, var));
