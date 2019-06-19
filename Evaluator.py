from Errors import EvaluationError, UndefinedVariableError;
from Tokenizer import Operation, Unknown;
from Parser import Parser;
from data import constants, test_strings;


class Evaluator():

    """ An evaluator for a mathematical expression at specific values """

    def __init__(self, expr):
        self.expr = expr;
        self.parser = Parser(self.expr);

    def _evaluate(self, tree, **substitutions):
        """ evaluate the parse tree at specific values for the variables """
        if isinstance(tree, Operation):
            try:
                return tree.function(*[self._evaluate(arg, **substitutions) for arg in tree.args]);
            except ZeroDivisionError:
                raise EvaluationError("Division by zero");
            except ValueError:
                raise EvaluationError("Function input not in domain");
            except TypeError:
                raise EvaluationError("Result is complex");
            except OverflowError:
                raise EvaluationError("Result is too large");
        elif isinstance(tree, Unknown):
            try:
                return substitutions[tree.name];
            except KeyError:
                raise UndefinedVariableError("Undefined variable {}".format(tree));
        else:
            return tree.value;

    def evaluate(self, **substitutions):
        """ define the constants and evaluate the expression """
        substitutions.update(constants);
        return self._evaluate(self.parser.tree, **substitutions);
    

if __name__ == "__main__":
    e = Evaluator(test_strings[6]);
