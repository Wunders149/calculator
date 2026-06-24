import math
import ast
import operator
import re


class ExpressionError(Exception):
    pass


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        raise ExpressionError("Division par z\u00e9ro")
    return x / y


def power(x, y):
    return x ** y


def sqrt(x):
    if x < 0:
        raise ExpressionError("Racine carr\u00e9e d'un nombre n\u00e9gatif")
    return math.sqrt(x)


def sin_deg(x):
    return math.sin(math.radians(x))


def cos_deg(x):
    return math.cos(math.radians(x))


def tan_deg(x):
    result = math.tan(math.radians(x))
    if abs(result) > 1e15:
        raise ExpressionError("Tangente non d\u00e9finie pour cet angle")
    return result


def sin_rad(x):
    return math.sin(x)


def cos_rad(x):
    return math.cos(x)


def tan_rad(x):
    result = math.tan(x)
    if abs(result) > 1e15:
        raise ExpressionError("Tangente non d\u00e9finie pour cet angle")
    return result


def log10(x):
    if x <= 0:
        raise ExpressionError("Logarithme d'un nombre non positif")
    return math.log10(x)


def ln(x):
    if x <= 0:
        raise ExpressionError("Ln d'un nombre non positif")
    return math.log(x)


def factorial(x):
    if x < 0 or not math.isclose(x, round(x)):
        raise ExpressionError(
            "Factorielle d\u00e9finie seulement pour les entiers naturels"
        )
    return math.factorial(int(round(x)))


def inv(x):
    if x == 0:
        raise ExpressionError("Division par z\u00e9ro")
    return 1.0 / x


def modulus(x, y):
    if y == 0:
        raise ExpressionError("Modulo par z\u00e9ro")
    return x % y


CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}


def _make_funcs(deg_mode=True):
    if deg_mode:
        return {
            'sin': sin_deg,
            'cos': cos_deg,
            'tan': tan_deg,
            'sqrt': sqrt,
            'log10': log10,
            'log': ln,
            'factorial': factorial,
            'inv': inv,
        }
    return {
        'sin': sin_rad,
        'cos': cos_rad,
        'tan': tan_rad,
        'sqrt': sqrt,
        'log10': log10,
        'log': ln,
        'factorial': factorial,
        'inv': inv,
    }


SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr, deg_mode=True):
    funcs = _make_funcs(deg_mode)

    try:
        tree = ast.parse(expr.strip(), mode='eval')
    except SyntaxError:
        raise ExpressionError("Expression invalide")

    return _eval_node(tree.body, funcs)


def _eval_node(node, funcs):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, funcs)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ExpressionError("Type de constante non support\u00e9")

    if isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise ExpressionError(f"Constante inconnue : {node.id}")

    if isinstance(node, ast.UnaryOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ExpressionError(
                f"Op\u00e9rateur non support\u00e9 : {type(node.op).__name__}"
            )
        return op(_eval_node(node.operand, funcs))

    if isinstance(node, ast.BinOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ExpressionError(
                f"Op\u00e9rateur non support\u00e9 : {type(node.op).__name__}"
            )
        left = _eval_node(node.left, funcs)
        right = _eval_node(node.right, funcs)
        if isinstance(node.op, (ast.Div, ast.Mod)):
            if right == 0:
                if isinstance(node.op, ast.Div):
                    raise ExpressionError("Division par z\u00e9ro")
                else:
                    raise ExpressionError("Modulo par z\u00e9ro")
        return op(left, right)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ExpressionError("Appels de fonction complexes non support\u00e9s")
        func_name = node.func.id
        if func_name not in funcs:
            raise ExpressionError(f"Fonction inconnue : {func_name}")
        args = [_eval_node(arg, funcs) for arg in node.args]
        try:
            return funcs[func_name](*args)
        except ExpressionError:
            raise
        except Exception as e:
            raise ExpressionError(
                f"Erreur dans {func_name} : {str(e)}"
            )

    raise ExpressionError(
        f"Expression non support\u00e9e : {type(node).__name__}"
    )


def to_display(s):
    s = s.replace('**2', '\u00b2')
    s = s.replace('**', '^')
    s = s.replace('*', '\u00d7')
    s = s.replace('/', '\u00f7')
    s = s.replace('pi', '\u03c0')
    return s


def from_display(s):
    s = s.replace('\u00b2', '**2')
    s = s.replace('^', '**')
    s = s.replace('\u00d7', '*')
    s = s.replace('\u00f7', '/')
    s = s.replace('\u03c0', 'pi')
    return s


def preprocess(s):
    s = s.replace(')(', ')*(')
    s = re.sub(r'\)(\d)', r')*\1', s)
    s = re.sub(r'(?<!\w)(\d)\(', r'\1*(', s)
    s = re.sub(r'(\d)pi', r'\1*pi', s)
    s = re.sub(r'(\d)e(?![\d+\-])', r'\1*e', s)
    s = re.sub(r'pi\(', 'pi*(', s)
    s = re.sub(r'e\(', 'e*(', s)
    s = re.sub(r'(pi)(\d)', r'\1*\2', s)
    s = re.sub(r'(?<!\d)(e)(\d)', r'\1*\2', s)
    s = re.sub(r'\)(pi|e)', r')*\1', s)
    s = re.sub(r'(\d)inv\(', r'\1*inv(', s)
    s = re.sub(r'\)inv\(', r')*inv(', s)
    return s



