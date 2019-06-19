import math;
import cmath;

functions = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt,
    "csc": lambda x: 1 / math.sin(x), "sec": lambda x: 1 / math.cos(x),
    "cot": lambda x: 1 / math.tan(x), "exp": math.exp, "abs": abs, "log": math.log,
    "asin": math.asin, "acos": math.acos, "atan": math.atan
};

derivatives = {
    "sin": math.cos, "cos": lambda x: -math.sin(x), "tan": lambda x: (1 / math.cos(x)) ** 2,
    "sqrt": lambda x: 1 / (2 * math.sqrt(x)), "csc": lambda x: -(1 / math.tan(x)) * (1 / math.sin(x)),
    "sec": lambda x: (1 / math.cos(x)) * math.tan(x), "cot": lambda x: -(1 / math.sin(x)) ** 2,
    "exp": math.exp, "abs": lambda x: x / abs(x), "log": lambda x: 1 / x
};

operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "~": lambda x: -x,
    "^": lambda x, y: x ** y
};

associativities = {
    "+": "left", "-": "left", "*": "left",
    "/": "left", "~": "left", "^": "right",
    "%": "left"
};

constants = {
    "e": math.e, "pi": math.pi
};

operators = "".join(list(operations.keys()));
function_names = list(functions.keys());
letters = "abcdefghijklmnopqrstuvwxyz";

test_strings = [
    "(1+x*3)/(5+xy)", "2xsin(x)+4", "sqrt(1-x^2)",
    "2^-1", "sin(x)+1", "(-1)^2", "(x)", "a+b+c", "a^b^c"
];
