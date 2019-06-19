from Errors import ParserException;
from Tokenizer import *;

""" this is the main part of the math engine. it parses a list of tokens into a AST. (an Operation object) """


def list_count(list_, element, start, stop):
    """ find the number of times element occurs in list_ from start index to stop index """
    return list_[start:stop].count(element);


class Parser():

    """ A parser for math expressions in strings """

    def __init__(self, expr):
        self.tokenizer = Tokenizer();
        self.set_expression(expr);

    def set_expression(self, expr):
        """ set the expression to be parsed """
        self.expr = self.tokenizer.clean_up(expr);
        self.tokens = self.tokenizer.tokenize(self.expr);
        self.tree = self.parse(self.tokens);

    def is_unary(self, tokens, i):
        """ checks if a negative sign('-') is the unary negation operator or the binary subtraction operator """
        return isinstance(tokens[i], Operator) and tokens[i].operator == "-" and ((not i) or isinstance(tokens[i-1], Operator) or (tokens[i-1] == "("));

    def get_unary_argument(self, tokens, i):
        """ get the argument of the unary negation function (or another unary function such as sin, cos, etc """
        tokens, arg = tokens[i+1:], [];
        count = 1;
        for token in tokens:
            if token == "(": count += 1;
            elif token == ")": count -= 1;
            if not count: break;
            arg.append(token);
        return arg;

    def determine_precedence(self, tokens, index, token):
        """ determine the precedence of a token in a set of tokens """
        open_parentheses_score = 5 * (list_count(tokens, "(", 0, index) - list_count(tokens, ")", 0, index));

        if isinstance(token, Operator):
            if token.operator == "^":
                return 3 + open_parentheses_score;
            elif token.operator in "*/%":
                return 1 + open_parentheses_score;
            elif token.operator == "~":
                return 2 + open_parentheses_score;
            else:
                return open_parentheses_score;
        elif isinstance(token, Function):
            return 4 + open_parentheses_score;
        else:
            return (tokens.count("(") + 1) * 5 + (str(token) in "()");

    def parse(self, tokens):
        """ parse the tokens into a parse tree """

        if len(tokens) == 1:
            # the Parser reached a terminal symbol (number or unknown)
            return tokens[0];

        last = len(tokens) * 5;
        for i, token in enumerate(tokens):
            if self.is_unary(tokens, i):
                tokens[i] = Operator("~");
                token = tokens[i];
                
            prec = self.determine_precedence(tokens, i, token);
            if prec < last:
                last, lowest, index = prec, token, i;
            elif prec == last:
                if isinstance(token, Operator):
                    if token.associativity == "right":
                        pass;
                    else:
                        last, lowest, index = prec, token, i;
                else:
                    last, lowest, index = prec, token, i;

        if isinstance(lowest, Function) or (isinstance(lowest, Operator) and lowest.operator == "~"):
            return Operation(lowest.function, [self.parse(self.get_unary_argument(tokens, index))], last, str(lowest));
        elif isinstance(lowest, (Number, Unknown)):
            return tokens[index];
        else:
            lhs, rhs = tokens[:index], tokens[index+1:];
            if len(lhs) == 2 and lhs[0] == "(": lhs = lhs[1:];
            if len(rhs) == 2 and rhs[-1] == ")": rhs = rhs[:-1];
            return Operation(lowest.function, [self.parse(lhs), self.parse(rhs)], last, str(lowest));
