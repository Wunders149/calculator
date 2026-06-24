import calculator_math as cm

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

if platform in ('android', 'ios'):
    from kivy.core.window import Window as Win
    Win.softinput_mode = 'below_target'

THEME = {
    'bg': [0.118, 0.118, 0.180, 1],
    'fg': [0.804, 0.839, 0.957, 1],
    'display_bg': [0.094, 0.094, 0.145, 1],
    'display_fg': [0.804, 0.839, 0.957, 1],
    'btn_num': [0.192, 0.192, 0.267, 1],
    'btn_num_fg': [0.804, 0.839, 0.957, 1],
    'btn_op': [0.271, 0.271, 0.357, 1],
    'btn_op_fg': [0.537, 0.706, 0.980, 1],
    'btn_sci': [0.345, 0.345, 0.447, 1],
    'btn_sci_fg': [0.651, 0.890, 0.631, 1],
    'btn_eq': [0.537, 0.706, 0.980, 1],
    'btn_eq_fg': [0.118, 0.118, 0.180, 1],
    'btn_clear': [0.953, 0.549, 0.659, 1],
    'btn_clear_fg': [0.118, 0.118, 0.180, 1],
    'btn_hover': [0.424, 0.439, 0.525, 1],
    'accent': [0.537, 0.706, 0.980, 1],
}


def rgba(r, g, b, a=1):
    return [r / 255, g / 255, b / 255, a]


THEME_RGB = {
    'bg': rgba(30, 30, 46),
    'fg': rgba(205, 214, 244),
    'display_bg': rgba(24, 24, 37),
    'display_fg': rgba(205, 214, 244),
    'btn_num': rgba(49, 50, 68),
    'btn_num_fg': rgba(205, 214, 244),
    'btn_op': rgba(69, 71, 90),
    'btn_op_fg': rgba(137, 180, 250),
    'btn_sci': rgba(88, 91, 112),
    'btn_sci_fg': rgba(166, 227, 161),
    'btn_eq': rgba(137, 180, 250),
    'btn_eq_fg': rgba(30, 30, 46),
    'btn_clear': rgba(243, 139, 168),
    'btn_clear_fg': rgba(30, 30, 46),
    'btn_hover': rgba(108, 112, 134),
    'accent': rgba(137, 180, 250),
}


class CalcButton(Button):
    def __init__(self, text, bg, fg, font_size='14sp', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.background_normal = ''
        self.background_color = bg
        self.color = fg
        self.font_size = font_size
        self.bold = True
        self.size_hint_y = None
        self.height = '52dp'


class CalculatorMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding='4dp', spacing='2dp', **kwargs)
        self._build()

        self.expression = ''
        self.deg_mode = True
        self.just_evaluated = False

        if platform in ('android', 'ios'):
            Window.bind(on_keyboard=self.on_key)

    def _build(self):
        display = BoxLayout(
            orientation='vertical',
            size_hint_y=0.14,
            padding=['8dp', '4dp'],
            spacing='2dp',
        )
        with display.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*THEME_RGB['display_bg'])
            self._display_rect = Rectangle(pos=display.pos, size=display.size)
            display.bind(pos=lambda _, v: setattr(self._display_rect, 'pos', v))
            display.bind(size=lambda _, v: setattr(self._display_rect, 'size', v))

        self.expr_label = Label(
            text='',
            font_size='18sp',
            color=THEME_RGB['display_fg'],
            halign='right',
            valign='bottom',
            text_size=(Window.width - 24, None),
            size_hint_y=0.5,
        )
        self.result_label = Label(
            text='Bienvenue !',
            font_size='26sp',
            color=THEME_RGB['accent'],
            halign='right',
            valign='middle',
            text_size=(Window.width - 24, None),
            size_hint_y=0.5,
            bold=True,
        )

        display.add_widget(self.expr_label)
        display.add_widget(self.result_label)

        self.add_widget(display)

        grid = GridLayout(cols=4, spacing='2dp', size_hint_y=0.86, padding=['2dp', '2dp'])

        t = THEME_RGB
        sc, scf = t['btn_sci'], t['btn_sci_fg']
        op, opf = t['btn_op'], t['btn_op_fg']
        num, nf = t['btn_num'], t['btn_num_fg']
        clr, clrf = t['btn_clear'], t['btn_clear_fg']
        eq, eqf = t['btn_eq'], t['btn_eq_fg']
        fs = '12sp'

        buttons = [
            ('sin', sc, scf, lambda: self.sci('sin('), fs),
            ('cos', sc, scf, lambda: self.sci('cos('), fs),
            ('tan', sc, scf, lambda: self.sci('tan('), fs),
            ('log', sc, scf, lambda: self.sci('log10('), fs),
            ('ln', sc, scf, lambda: self.sci('log('), fs),
            ('\u221a', sc, scf, lambda: self.sci('sqrt('), fs),
            ('x\u00b2', sc, scf, lambda: self.click('**2'), fs),
            ('x^y', sc, scf, lambda: self.click('**'), fs),
            ('\u03c0', sc, scf, lambda: self.click('pi'), fs),
            ('e', sc, scf, lambda: self.click('e'), fs),
            ('!', sc, scf, lambda: self.sci('factorial('), fs),
            ('1/x', sc, scf, lambda: self.sci('inv('), fs),
            ('(', sc, scf, lambda: self.click('('), fs),
            (')', sc, scf, lambda: self.click(')'), fs),
            ('%', sc, scf, lambda: self.click('%'), fs),
            ('\u232b', sc, scf, self.backspace, fs),
            ('C', clr, clrf, self.clear, fs),
            ('\u00b1', sc, scf, self.negate, fs),
            ('7', num, nf, lambda: self.click(7)),
            ('8', num, nf, lambda: self.click(8)),
            ('9', num, nf, lambda: self.click(9)),
            ('/', op, opf, lambda: self.click('/')),
            ('4', num, nf, lambda: self.click(4)),
            ('5', num, nf, lambda: self.click(5)),
            ('6', num, nf, lambda: self.click(6)),
            ('*', op, opf, lambda: self.click('*')),
            ('1', num, nf, lambda: self.click(1)),
            ('2', num, nf, lambda: self.click(2)),
            ('3', num, nf, lambda: self.click(3)),
            ('-', op, opf, lambda: self.click('-')),
            ('0', num, nf, lambda: self.click(0)),
            ('.', op, opf, lambda: self.click('.')),
            ('=', eq, eqf, self.equals),
            ('+', op, opf, lambda: self.click('+')),
        ]

        for label, bg, fg, callback, *opts in buttons:
            fs_btn = opts[0] if opts else '16sp'
            btn = CalcButton(text=label, bg=bg, fg=fg, font_size=fs_btn)
            btn.bind(on_release=callback)
            grid.add_widget(btn)

        self.add_widget(grid)

        mode_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.06,
            spacing='4dp',
            padding=['8dp', '2dp'],
        )
        mode_bar.canvas.before_color = THEME_RGB['bg']

        self.mode_btn = CalcButton(
            text='DEG', bg=t['btn_sci'], fg=t['accent'],
            font_size='12sp', size_hint_y=None, height='28dp',
            size_hint_x=0.3,
        )
        self.mode_btn.bind(on_release=self.toggle_mode)
        mode_bar.add_widget(self.mode_btn)

        status = Label(
            text='Pr\u00eate',
            font_size='11sp',
            color=t['btn_op_fg'],
            halign='right',
            size_hint_x=0.7,
        )
        mode_bar.add_widget(status)
        self.status_label = status

        self.add_widget(mode_bar)

        Window.bind(on_resize=self._on_resize)

    def _on_resize(self, win, w, h):
        self.expr_label.text_size = (w - 24, None)
        self.result_label.text_size = (w - 24, None)

    def _refresh(self):
        self.expr_label.text = cm.to_display(self.expression)

    def click(self, item):
        if self.result_label.text == 'Bienvenue !':
            self.expression = ''
        if self.just_evaluated:
            if isinstance(item, str) and item in '+-*/.**%':
                pass
            else:
                self.expression = ''
            self.just_evaluated = False
        self.expression = self.expression + str(item)
        self.result_label.text = cm.to_display(self.expression)
        self._refresh()

    def sci(self, func):
        if self.result_label.text == 'Bienvenue !':
            self.expression = ''
        if self.just_evaluated:
            self.expression = ''
            self.just_evaluated = False
        self.expression = self.expression + func
        self._refresh()
        self.result_label.text = cm.to_display(self.expression)

    def clear(self):
        self.expression = ''
        self.just_evaluated = False
        self._refresh()
        self.result_label.text = '0'

    def backspace(self):
        if self.just_evaluated:
            return
        self.expression = self.expression[:-1]
        self._refresh()
        self.result_label.text = cm.to_display(self.expression) or '0'

    def negate(self):
        if self.just_evaluated:
            self.just_evaluated = False
        if not self.expression or self.expression == '0':
            return
        if self._is_number(self.expression):
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
                self.expression = self.expression.lstrip('+')
            else:
                self.expression = '-' + self.expression
        else:
            self.expression = '-(' + self.expression + ')'
        self._refresh()
        self.result_label.text = cm.to_display(self.expression)

    @staticmethod
    def _is_number(s):
        if not s:
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    def equals(self):
        expr = cm.from_display(
            self.result_label.text
            if self.result_label.text != 'Bienvenue !'
            else ''
        )
        if not expr:
            return
        try:
            if not self._check_parens(expr):
                self._error('Parenth\u00e8ses d\u00e9s\u00e9quilibr\u00e9es')
                return
            expr = cm.preprocess(expr)
            self.status_label.text = 'Les calculs se v\u00e9rifient'
            result = cm.safe_eval(expr, deg_mode=self.deg_mode)
            result_str = str(result)
            self.result_label.text = result_str
            self.expression = result_str
            self.just_evaluated = True
            self.status_label.text = ''
        except cm.ExpressionError as e:
            self._error(str(e))
        except Exception:
            self._error('Expression invalide')

    def _error(self, msg):
        self.result_label.text = msg
        self.expression = ''
        self.just_evaluated = False
        self.status_label.text = ''
        Clock.schedule_once(lambda dt: self._clear_error(), 1.5)

    def _clear_error(self):
        self.result_label.text = '0'

    def toggle_mode(self, _btn=None):
        self.deg_mode = not self.deg_mode
        self.mode_btn.text = 'DEG' if self.deg_mode else 'RAD'

    @staticmethod
    def _check_parens(s):
        balance = 0
        for ch in s:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    def on_key(self, window, key, scancode, codepoint, modifier):
        if codepoint and codepoint.isdigit():
            self.click(int(codepoint))
            return True
        if codepoint in '+-*/.()%':
            self.click(codepoint)
            return True
        if codepoint in 'eE':
            self.click('e')
            return True
        if codepoint == 'p':
            self.click('pi')
            return True
        if key == 13:
            self.equals()
            return True
        if key == 8:
            self.backspace()
            return True
        if key == 127 or key == 27:
            self.clear()
            return True
        return False


class CalculatorApp(App):
    def build(self):
        self.title = 'Calculatrice Scientifique'
        if platform != 'android' and platform != 'ios':
            Window.size = (380, 700)
        return CalculatorMobile()


if __name__ == '__main__':
    CalculatorApp().run()
