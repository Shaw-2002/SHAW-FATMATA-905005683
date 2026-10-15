import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_FILE = BASE / "input.txt"
OUTPUT_FILE = BASE / "output.txt"
SEPARATOR = re.compile(r"^[\-=*_]{3,}$")
TOKEN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")

class Stack:
    """Last-In, First-Out stack implemented with a Python list."""
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if self.is_empty():
            raise ValueError("Cannot pop from an empty stack.")
        return self.items.pop()
    def peek(self):
        if self.is_empty():
            raise ValueError("Cannot peek at an empty stack.")
        return self.items[-1]
    def is_empty(self):
        return len(self.items) == 0
    def __len__(self):
        return len(self.items)

def tokenize(expression):
    tokens, pos = [], 0
    while pos < len(expression):
        if expression[pos].isspace():
            pos += 1
            continue
        match = TOKEN.match(expression, pos)
        if not match:
            raise ValueError(f"Unsupported character: {expression[pos]!r}")
        tokens.append(match.group())
        pos = match.end()
    if not tokens:
        raise ValueError("Expression is empty.")
    result, previous = [], None
    for token in tokens:
        if token in ("+", "-") and (previous is None or previous in ("(", "+", "-", "*", "/")):
            result.append("u+" if token == "+" else "u-")
        else:
            result.append(token)
        previous = token
    return result

def to_postfix(expression):
    output, ops = [], Stack()
    prec = {"u+": 3, "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    right_assoc = {"u+", "u-"}
    for token in tokenize(expression):
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            output.append(token)
        elif token in prec:
            while not ops.is_empty() and ops.peek() != "(" and ops.peek() in prec:
                top = ops.peek()
                if prec[top] > prec[token] or (prec[top] == prec[token] and token not in right_assoc):
                    output.append(ops.pop())
                else:
                    break
            ops.push(token)
        elif token == "(":
            ops.push(token)
        elif token == ")":
            found = False
            while not ops.is_empty():
                top = ops.pop()
                if top == "(":
                    found = True
                    break
                output.append(top)
            if not found:
                raise ValueError("Mismatched parentheses: missing '('.")
    while not ops.is_empty():
        top = ops.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: missing ')'.")
        output.append(top)
    return output

def evaluate_postfix(postfix):
    values = Stack()
    for token in postfix:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            values.push(float(token) if "." in token else int(token))
        elif token in ("u+", "u-"):
            if len(values) < 1:
                raise ValueError("Unary operator is missing a value.")
            value = values.pop()
            values.push(value if token == "u+" else -value)
        elif token in ("+", "-", "*", "/"):
            if len(values) < 2:
                raise ValueError("Operator is missing one or more values.")
            right, left = values.pop(), values.pop()
            if token == "+": result = left + right
            elif token == "-": result = left - right
            elif token == "*": result = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                result = left / right
            values.push(result)
        else:
            raise ValueError(f"Unsupported token: {token}")
    if len(values) != 1:
        raise ValueError("Invalid expression. Check operators and operands.")
    return values.pop()

def evaluate_expression(expression):
    return evaluate_postfix(to_postfix(expression))

def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def process_file(input_path=INPUT_FILE, output_path=OUTPUT_FILE):
    input_path, output_path = Path(input_path), Path(output_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    output = []
    for number, raw in enumerate(input_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or SEPARATOR.fullmatch(line):
            output.append(line)
            continue
        try:
            output.append(format_result(evaluate_expression(line)))
        except (ValueError, ZeroDivisionError) as err:
            output.append(f"ERROR on input line {number}: {err}")
    output_path.write_text("\n".join(output) + "\n", encoding="utf-8")
    return output

if __name__ == "__main__":
    try:
        results = process_file()
        print("Finished. Results written to output.txt")
        print("\n".join(results))
    except OSError as err:
        print(f"Program could not finish: {err}")
