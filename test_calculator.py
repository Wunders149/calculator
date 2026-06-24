import math
import unittest
import calculator_math as cm


class TestBasicOps(unittest.TestCase):
    def test_add(self):
        self.assertEqual(cm.add(2, 3), 5)
        self.assertEqual(cm.add(-1, 1), 0)
        self.assertEqual(cm.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(cm.subtract(5, 3), 2)
        self.assertEqual(cm.subtract(1, 5), -4)

    def test_multiply(self):
        self.assertEqual(cm.multiply(4, 3), 12)
        self.assertEqual(cm.multiply(0, 5), 0)
        self.assertEqual(cm.multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(cm.divide(10, 2), 5)
        self.assertEqual(cm.divide(7, 2), 3.5)

    def test_divide_by_zero(self):
        with self.assertRaises(cm.ExpressionError):
            cm.divide(5, 0)

    def test_power(self):
        self.assertEqual(cm.power(2, 3), 8)
        self.assertEqual(cm.power(5, 0), 1)
        self.assertEqual(cm.power(9, 0.5), 3)


class TestScientificOps(unittest.TestCase):
    def test_sqrt(self):
        self.assertEqual(cm.sqrt(9), 3)
        self.assertEqual(cm.sqrt(0), 0)

    def test_sqrt_negative(self):
        with self.assertRaises(cm.ExpressionError):
            cm.sqrt(-1)

    def test_sin_deg(self):
        self.assertAlmostEqual(cm.sin_deg(0), 0)
        self.assertAlmostEqual(cm.sin_deg(90), 1)
        self.assertAlmostEqual(cm.sin_deg(180), 0, places=10)

    def test_cos_deg(self):
        self.assertAlmostEqual(cm.cos_deg(0), 1)
        self.assertAlmostEqual(cm.cos_deg(90), 0, places=10)
        self.assertAlmostEqual(cm.cos_deg(180), -1)

    def test_tan_deg(self):
        self.assertAlmostEqual(cm.tan_deg(0), 0)
        self.assertAlmostEqual(cm.tan_deg(45), 1, places=9)

    def test_tan_deg_undefined(self):
        with self.assertRaises(cm.ExpressionError):
            cm.tan_deg(90)

    def test_sin_rad(self):
        self.assertAlmostEqual(cm.sin_rad(0), 0)
        self.assertAlmostEqual(cm.sin_rad(math.pi / 2), 1)

    def test_log10(self):
        self.assertAlmostEqual(cm.log10(100), 2)
        self.assertAlmostEqual(cm.log10(1), 0)

    def test_log10_non_positive(self):
        with self.assertRaises(cm.ExpressionError):
            cm.log10(0)
        with self.assertRaises(cm.ExpressionError):
            cm.log10(-5)

    def test_ln(self):
        self.assertAlmostEqual(cm.ln(math.e), 1)
        self.assertAlmostEqual(cm.ln(1), 0)

    def test_ln_non_positive(self):
        with self.assertRaises(cm.ExpressionError):
            cm.ln(0)
        with self.assertRaises(cm.ExpressionError):
            cm.ln(-1)

    def test_factorial(self):
        self.assertEqual(cm.factorial(5), 120)
        self.assertEqual(cm.factorial(0), 1)
        self.assertEqual(cm.factorial(1), 1)
        self.assertEqual(cm.factorial(5.0), 120)

    def test_factorial_float_close(self):
        self.assertEqual(cm.factorial(5.0000000001), 120)

    def test_factorial_negative(self):
        with self.assertRaises(cm.ExpressionError):
            cm.factorial(-1)

    def test_factorial_non_integer(self):
        with self.assertRaises(cm.ExpressionError):
            cm.factorial(5.5)

    def test_inv(self):
        self.assertEqual(cm.inv(2), 0.5)
        self.assertEqual(cm.inv(4), 0.25)

    def test_inv_zero(self):
        with self.assertRaises(cm.ExpressionError):
            cm.inv(0)

    def test_modulus(self):
        self.assertEqual(cm.modulus(10, 3), 1)
        self.assertEqual(cm.modulus(10, 5), 0)

    def test_modulus_zero(self):
        with self.assertRaises(cm.ExpressionError):
            cm.modulus(5, 0)


class TestSafeEval(unittest.TestCase):
    def test_simple_arith(self):
        self.assertEqual(cm.safe_eval('2+3'), 5)
        self.assertEqual(cm.safe_eval('10-4'), 6)
        self.assertEqual(cm.safe_eval('3*4'), 12)
        self.assertEqual(cm.safe_eval('10/2'), 5)
        self.assertEqual(cm.safe_eval('2**3'), 8)

    def test_with_parens(self):
        self.assertEqual(cm.safe_eval('(2+3)*4'), 20)
        self.assertEqual(cm.safe_eval('2*(3+4)'), 14)

    def test_unary_minus(self):
        self.assertEqual(cm.safe_eval('-5'), -5)
        self.assertEqual(cm.safe_eval('-(3+2)'), -5)

    def test_modulus_op(self):
        self.assertEqual(cm.safe_eval('10%3'), 1)
        self.assertEqual(cm.safe_eval('10%5'), 0)

    def test_division_by_zero(self):
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('5/0')

    def test_modulus_by_zero(self):
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('5%0')

    def test_sin_deg(self):
        result = cm.safe_eval('sin(90)', deg_mode=True)
        self.assertAlmostEqual(result, 1)

    def test_cos_deg(self):
        result = cm.safe_eval('cos(0)', deg_mode=True)
        self.assertAlmostEqual(result, 1)

    def test_tan_deg_undefined(self):
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('tan(90)', deg_mode=True)

    def test_sin_rad(self):
        result = cm.safe_eval('sin(1.5707963267948966)', deg_mode=False)
        self.assertAlmostEqual(result, 1)

    def test_cos_rad(self):
        result = cm.safe_eval('cos(0)', deg_mode=False)
        self.assertAlmostEqual(result, 1)

    def test_sqrt(self):
        self.assertEqual(cm.safe_eval('sqrt(9)'), 3)
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('sqrt(-1)')

    def test_log10(self):
        self.assertAlmostEqual(cm.safe_eval('log10(100)'), 2)
        self.assertAlmostEqual(cm.safe_eval('log10(e)'), math.log10(math.e))
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('log10(0)')

    def test_log_ln(self):
        self.assertAlmostEqual(cm.safe_eval('log(1)'), 0)
        self.assertAlmostEqual(cm.safe_eval('log(2.718281828459045)'), 1, places=9)

    def test_factorial(self):
        self.assertEqual(cm.safe_eval('factorial(5)'), 120)
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('factorial(-1)')

    def test_inv(self):
        self.assertEqual(cm.safe_eval('inv(2)'), 0.5)
        self.assertEqual(cm.safe_eval('inv(4)'), 0.25)
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('inv(0)')

    def test_constants(self):
        self.assertEqual(cm.safe_eval('pi'), math.pi)
        self.assertEqual(cm.safe_eval('e'), math.e)

    def test_combined(self):
        result = cm.safe_eval('sin(30)+cos(60)', deg_mode=True)
        self.assertAlmostEqual(result, 1)
        self.assertAlmostEqual(cm.safe_eval('sqrt(9)+2**3'), 11)
        self.assertAlmostEqual(cm.safe_eval('5+3*2'), 11)
        self.assertAlmostEqual(cm.safe_eval('(5+3)*2'), 16)

    def test_chain_result(self):
        result = cm.safe_eval('2+3', deg_mode=True)
        result = cm.safe_eval(f'{result}+4', deg_mode=True)
        self.assertEqual(result, 9)

    def test_empty(self):
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('')

    def test_invalid_expression(self):
        with self.assertRaises(cm.ExpressionError):
            cm.safe_eval('2@3')

    def test_security_no_builtins(self):
        with self.assertRaises(Exception):
            cm.safe_eval('__import__("os")')
        with self.assertRaises(Exception):
            cm.safe_eval('open("/etc/passwd")')
        with self.assertRaises(Exception):
            cm.safe_eval('eval("1+1")')

    def test_float_result(self):
        result = cm.safe_eval('7/2')
        self.assertEqual(result, 3.5)

    def test_negate_wrapper(self):
        result = cm.safe_eval('-(5+3)')
        self.assertEqual(result, -8)

    def test_negate_single(self):
        result = cm.safe_eval('-42')
        self.assertEqual(result, -42)


class TestDisplayConversion(unittest.TestCase):
    def test_to_display(self):
        self.assertEqual(cm.to_display('**2'), '\u00b2')
        self.assertEqual(cm.to_display('**'), '^')
        self.assertEqual(cm.to_display('*'), '\u00d7')
        self.assertEqual(cm.to_display('/'), '\u00f7')
        self.assertEqual(cm.to_display('pi'), '\u03c0')

    def test_from_display(self):
        self.assertEqual(cm.from_display('\u00b2'), '**2')
        self.assertEqual(cm.from_display('^'), '**')
        self.assertEqual(cm.from_display('\u00d7'), '*')
        self.assertEqual(cm.from_display('\u00f7'), '/')
        self.assertEqual(cm.from_display('\u03c0'), 'pi')

    def test_roundtrip(self):
        cases = ['sin(45)', '2**3', '3.14*2', 'pi/2', 'e+1']
        for c in cases:
            self.assertEqual(cm.from_display(cm.to_display(c)), c)


class TestPreprocess(unittest.TestCase):
    def test_implicit_mul_parens(self):
        self.assertEqual(cm.preprocess('5(3)'), '5*(3)')

    def test_implicit_mul_pi(self):
        self.assertEqual(cm.preprocess('2pi'), '2*pi')

    def test_implicit_mul_e(self):
        self.assertEqual(cm.preprocess('2e'), '2*e')

    def test_implicit_mul_paren_close(self):
        self.assertEqual(cm.preprocess('(2)(3)'), '(2)*(3)')

    def test_pi_paren(self):
        self.assertEqual(cm.preprocess('pi(2)'), 'pi*(2)')

    def test_implicit_mul_inv(self):
        self.assertEqual(cm.preprocess('2inv(3)'), '2*inv(3)')

    def test_log10_preserved(self):
        self.assertEqual(cm.preprocess('log10(e)'), 'log10(e)')

    def test_log10_with_arg(self):
        self.assertEqual(cm.preprocess('log10(100)'), 'log10(100)')


class TestConstants(unittest.TestCase):
    def test_pi(self):
        self.assertEqual(cm.CONSTANTS['pi'], math.pi)

    def test_e(self):
        self.assertEqual(cm.CONSTANTS['e'], math.e)


if __name__ == '__main__':
    unittest.main()
