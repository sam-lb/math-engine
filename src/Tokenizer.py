from Errors import InvalidExpressionError;
from data import operators, operations, associativities, functions,function_names, constants, letters;


""" tokenizes a string and classifies each token """


class Number():

    """ A number i.e. 4 or 23.1 or -2.9 """

    def __init__(self, value):
        try:
            self.value = float(value);
        except ValueError:
            raise InvalidExpressionError("Invalid number {}".format(value));

    def __repr__(self):
        return "{}".format(self.value);


class Operator():

    """ + - * / etc """

    def __init__(self, operator):
        if operator in operators:
            self.operator = operator;
            self.function = operations[self.operator];
            self.associativity = associativities[self.operator];
        else:
            raise InvalidExpressionError("Invalid operator {}".format(operator));

    def __repr__(self):
        return self.operator.replace("~", "-");

    def evaluate(self, lhs, rhs):
        return self.function(lhs.value, rhs.value);


class Function():

    """ A function that takes in arguments and returns a numerical output """

    def __init__(self, function):
        if function in function_names:
            self.function_name = function;
            self.function = functions[self.function_name];
        else:
            raise InvalidExpressionError("Invalid function {}".format(function));

    def __repr__(self):
        return self.function_name;

    def evaluate(self, argument, q=None):
        """ evaluate the function at a value """
        return self.function(argument);


class Operation():

    """ A parse tree element """

    def __init__(self, function, args, precedence, string):
        self.function = function;
        self.args = args;
        self.precedence = precedence;
        self.string = string;

    def __repr__(self):
        return "{} {}".format(self.string, tuple(self.args));


class Unknown():

    """ a terminal character that is not a constant or an operator """

    def __init__(self, name):
        self.name = name;

    def __repr__(self):
        return self.name;


class Tokenizer():

    """ tokenizes an expression """

    @classmethod
    def clean_up(cls, expr):
        """ prepare the string for tokenization, remove simple mistakes, handle implicit multiplication """
        expr = expr.replace(" ", "").replace("++", "+").replace("--", "+").replace("+-", "-");
        newexpr = expr[0];
        for i, char in enumerate(expr[1:], start=1):
            if ((char in letters+"(") and (expr[i-1] not in operators+"(")):
                newexpr += f"*{char}";
            else:
                newexpr += char;

        for func in sorted(function_names, key=lambda f: len(f), reverse=True):
            newexpr = newexpr.replace("*".join(list(func))+"*", func);
        for const in constants.keys():
            newexpr = newexpr.replace("*".join(list(const)), const);
            
        return newexpr;

    @classmethod
    def tokenize(cls, expr):
        """ takes a string and returns a list of tokens. assumes that expr has been cleaned with clean_up. """

        def empty_buffers():
            nonlocal tokens, function_buffer, number_buffer;
            if function_buffer:
                try:
                    tokens.append(Function(function_buffer));
                except InvalidExpressionError:
                    tokens.append(Unknown(function_buffer));
                function_buffer = "";
            if number_buffer:
                tokens.append(Number(number_buffer));
                number_buffer = "";
        
        tokens, function_buffer, number_buffer = [], "", "";
        count = 1;

        for char in expr:
            if not count:
                raise InvalidExpressionError("Mismatched parentheses.");
            elif char == "(":
                empty_buffers();
                tokens.append(char);
                count += 1;
            elif char == ")":
                empty_buffers();
                tokens.append(char);
                count -= 1;
            elif char in letters:
                function_buffer += char;
            elif char.isdigit() or char == ".":
                number_buffer += char;
            elif char in operators:
                empty_buffers();
                tokens.append(Operator(char));
            else:
                raise InvalidExpressionError("Invalid character {}".format(char));
        empty_buffers();
                
        if count != 1: raise InvalidExpressionError("Unequal amount of open and close parentheses.");
        return tokens;
