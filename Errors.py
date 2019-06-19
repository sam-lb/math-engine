class InvalidExpressionError(Exception):
    """ raised when an invalid mathematical expression is passed """
    pass;

class UndefinedVariableError(Exception):
    """ raised when an undefined variable is encountered """
    pass;

class ParserException(Exception):
    """ raised if something goes wrong when parsing (user or internal) """
    pass;

class EvaluationError(Exception):
    """ raised if evaluation is out of domain, invalid, etc. """
    pass;

class DerivativeError(Exception):
    """ raised if the function cannot be derivated """
    pass;

class GeneralError(Exception):
    """ anything else """
    pass;
