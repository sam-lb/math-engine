from Tokenizer import Operation, Unknown, Number;
from Parser import Parser;
from Errors import GeneralError;

"""
simplifies expressions. for use with:
- Insight.py (and other plotting applications)
- Derivative.py
- Solver.py

this is essentially an Evaluator.py that handles operations between Unknowns and Numbers.

not finished yet.
"""


class AlgebraicExpression():

    """ Representation of an algebraic expression """

    def __init__(self, coef, variables):
        self.coef = coef;
        self.variables = variables; # dict

    def __repr__(self):
        return "{}{}".format(self.coef, "".join(("{}^{}".format(var, exp) for var, exp in self.variables.items())));

    def __neg__(self):
        return AlgebraicExpression(-self.coef, self.variables);

    def __add__(self, other):
        if self.like_terms(other):
            return AlgebraicExpression(self.coef + other.coef, self.variables);
        elif not self.coef:
            return other;
        elif not other.coef:
            return self;
        else:
            raise GeneralError();

    def __sub__(self, other):
        return self + (-other);

    def __mul__(self, other):
        if (not self.coef) or (not other.coef):
            return AlgebraicExpression(0, {});
        new_coef = self.coef * other.coef;
        new_vars = self.variables.copy();
        for var, exp in other.variables.items():
            try:
                new_vars[var] += exp;
            except KeyError:
                new_vars[var] = exp;
        return AlgebraicExpression(new_coef, new_vars);

    def __truediv__(self, other):
        new_coef = self.coef / other.coef;
        new_vars = self.variables.copy();
        for var, exp in other.variables.items():
            try:
                new_vars[var] -= exp;
            except KeyError:
                new_vars[var] = -exp;
        return AlgebraicExpression(new_coef, new_vars);

    def __pow__(self, other):
        # assume other is AlgExpr of form coef=n, variables={}
        return AlgebraicExpression(self.coef ** other.coef, {var: exp * other.coef for var, exp in self.variables.items()});

    def like_terms(self, other):
        """ return if other is a like term with self. """
        return sorted(list(self.variables.items())) == sorted(list(other.variables.items()));


class Expression():

    """ algebraic sub-expression """

    def __init__(self, expressions):
        self.exprs = expressions;

    def __repr__(self):
        return to_infix(Parser("+".join([str(expr) for expr in self.exprs])).tree);

    def __neg__(self):
        return Expression([-expr for expr in self.exprs]);

    def __add__(self, other):
        all_exprs = self.exprs + other.exprs;
        new_exprs, all_exprs = [all_exprs[0]], all_exprs[1:];
        for expr in all_exprs:
            for i, term in enumerate(new_exprs):
                try:
                    new_exprs[i] = expr + term;
                except GeneralError:
                    continue;
                else:
                    break;
            else:
                new_exprs.append(expr);
        return Expression(new_exprs);

    def __sub__(self, other):
        return self + (-other);

    def __mul__(self, other):
        new_exprs = [];
        for expr in other.exprs:
            for expr2 in self.exprs:
                product = expr * expr2;
                new_exprs.append(product);
        return Expression(new_exprs);

    def __truediv__(self, other):
        new_exprs = [];
        for expr in other.exprs:
            for expr2 in self.exprs:
                quotient = expr / expr2;
                new_exprs.append(quotient);
        return Expression(new_exprs);

    def __pow__(self, other):
        result = self;
        for i in range(int(other.exprs[0].coef)-1):
            result = result * self;
        return result;

def simp(tree):
    """ simplify a parse tree and return an Expression """
    if isinstance(tree, Operation):
        z= tree.function(*[simp(arg) for arg in tree.args]);
        return z;
    elif isinstance(tree, Unknown):
        return Expression([AlgebraicExpression(1, {tree.name: 1})]);
    else:
        return Expression([AlgebraicExpression(tree.value, {})]);

def simplify(tree):
    """ simplify a parse tree and return the simplified tree """
    return Parser(str(simp(tree))).tree;

def cheat(strings):
    """ for development """
    p = [string.split("x^") for string in strings];
    return Expression([AlgebraicExpression(float(d[0]), {"x": float(d[1])}) for d in p]);

def to_infix(tree):
    """ converts a parse tree to a string repr of a math expression """
    if isinstance(tree, Operation):
        if len(tree.args) == 1:
            return "{}({})".format(tree.string, to_infix(tree.args[0]));
        else:
            if tree.string in "+-":
                return " {} ".format(tree.string).join([to_infix(arg) for arg in tree.args]);
            return tree.string.join([to_infix(arg) for arg in tree.args]);
    elif isinstance(tree, Number):
        if tree.value == int(tree.value):
            return str(int(tree.value));
        else:
            return str(tree);
    else:
        return str(tree);


if __name__ == "__main__":
    from Derivative import derive_tree;
    function = "3x/x"
    derivative = derive_tree(function);
    result = simplify(derivative);
    #expr = cheat(["3x^2","2x^1","6x^0"]);
    #expr2 = cheat(["4x^3","2x^2","2.5x^0"]);
