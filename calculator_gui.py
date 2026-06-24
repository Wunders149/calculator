import tkinter as tk

import calculator_math as cm


DPI_SCALE = 1.0
_scratch = tk.Tk()
_scratch.withdraw()
try:
    raw = _scratch.tk.call('tk', 'scaling')
    DPI_SCALE = raw / 1.333333
except Exception:
    pass
_scratch.destroy()

_scale = lambda v: max(1, round(v * DPI_SCALE))


THEME = {
    'bg': '#1e1e2e',
    'fg': '#cdd6f4',
    'display_bg': '#181825',
    'display_fg': '#cdd6f4',
    'btn_num': '#313244',
    'btn_num_fg': '#cdd6f4',
    'btn_op': '#45475a',
    'btn_op_fg': '#89b4fa',
    'btn_sci': '#585b70',
    'btn_sci_fg': '#a6e3a1',
    'btn_eq': '#89b4fa',
    'btn_eq_fg': '#1e1e2e',
    'btn_clear': '#f38ba8',
    'btn_clear_fg': '#1e1e2e',
    'btn_hover': '#6c7086',
    'accent': '#89b4fa',
    'border': '#45475a',
    'font_display': ('Segoe UI', _scale(22), 'bold'),
    'font_btn': ('Segoe UI', _scale(12), 'bold'),
    'font_sci': ('Segoe UI', _scale(10), 'bold'),
    'font_status': ('Segoe UI', _scale(9)),
    'font_dialog': ('Segoe UI', _scale(11)),
}


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title('Calculatrice Scientifique')
        w = _scale(360)
        h = _scale(650)
        master.geometry(f'{w}x{h}')
        master.resizable(False, False)
        master.configure(bg=THEME['bg'])

        self.expression = ''
        self.input_text = tk.StringVar()
        self.input_text.set('Bienvenue !')
        self.status_text = tk.StringVar()
        self.status_text.set('Pr\u00eate')
        self.deg_mode = True
        self.just_evaluated = False

        master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.build_menu()
        self.build_header()
        self.build_display()
        self.build_buttons()

        master.bind('<Key>', self.on_key)

    @staticmethod
    def _center(win, w, h):
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2 - 30)
        win.geometry(f'{w}x{h}+{x}+{y}')

    @staticmethod
    def _center_on(child, parent, w, h):
        parent.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        child.geometry(f'{w}x{h}+{x}+{y}')

    def _dialog(self, title, icon, msg, buttons=None):
        buttons = buttons or [('OK', True)]
        result = [False]
        dia = tk.Toplevel(self.master)
        dia.title(title)
        dia.configure(bg=THEME['bg'])
        dia.resizable(False, False)
        dia.transient(self.master)
        dw = _scale(300)
        dh = _scale(220)
        self._center_on(dia, self.master, dw, dh)

        frame = tk.Frame(dia, bg=THEME['accent'], height=_scale(3))
        frame.pack(fill=tk.X)

        body = tk.Frame(dia, bg=THEME['bg'])
        body.pack(fill=tk.BOTH, expand=True, padx=_scale(20), pady=(_scale(16), _scale(12)))

        tk.Label(body, text=icon, font=('Segoe UI', _scale(28)),
                 bg=THEME['bg'], fg=THEME['accent']).pack()

        tk.Label(body, text=title, font=('Segoe UI', _scale(13), 'bold'),
                 bg=THEME['bg'], fg=THEME['fg']).pack(pady=(_scale(4), _scale(2)))

        tk.Label(body, text=msg, font=THEME['font_dialog'],
                 bg=THEME['bg'], fg=THEME['btn_sci_fg'], wraplength=_scale(260),
                 justify=tk.CENTER).pack(pady=(0, _scale(10)))

        btn_frame = tk.Frame(body, bg=THEME['bg'])
        btn_frame.pack()

        def click(val):
            result[0] = val
            dia.grab_release()
            dia.destroy()

        for label, val in buttons:
            bg = THEME['btn_eq'] if val else THEME['btn_num']
            fg = THEME['btn_eq_fg'] if val else THEME['fg']
            tk.Button(btn_frame, text=label, font=('Segoe UI', _scale(10), 'bold'),
                      bg=bg, fg=fg, bd=0, padx=_scale(18), pady=_scale(4), cursor='hand2',
                      activebackground=THEME['btn_hover'], activeforeground=THEME['fg'],
                      command=lambda v=val: click(v)).pack(side=tk.LEFT, padx=_scale(4))

        dia.bind('<Escape>', lambda e: click(False))
        dia.grab_set()
        self.master.wait_window(dia)
        return result[0]

    def build_menu(self):
        menubar = tk.Menu(self.master, bg=THEME['bg'], fg=THEME['fg'],
                          activebackground=THEME['btn_sci'], activeforeground=THEME['fg'])
        menu_help = tk.Menu(menubar, tearoff=0, bg=THEME['btn_num'], fg=THEME['fg'],
                            activebackground=THEME['btn_sci'], activeforeground=THEME['fg'])
        menu_help.add_command(label='\u00c0 propos', command=self.show_about)
        menubar.add_cascade(label='?', menu=menu_help)
        self.master.config(menu=menubar)

    def show_about(self):
        self._dialog(
            '\u00c0 propos',
            '\u2328',
            'Calculatrice Scientifique v2.0\n'
            '+ \u2212 \u00d7 \u00f7  sin cos tan log ln\n'
            '\u221a x\u00b2 x^y 1/x %  \u03c0 e ! ( )\n\n'
            'Clavier : chiffres, op\u00e9rateurs, Entr\u00e9e, Suppr'
        )

    def build_header(self):
        header = tk.Frame(self.master, bg=THEME['accent'], height=_scale(36))
        header.pack(fill=tk.X)
        tk.Label(header, text='Calculatrice Scientifique',
                 font=('Segoe UI', _scale(11), 'bold'), bg=THEME['accent'],
                 fg=THEME['btn_eq_fg']).pack(side=tk.LEFT, padx=_scale(14), pady=_scale(6))

    def build_display(self):
        display_frame = tk.Frame(self.master, bg=THEME['bg'], bd=0)
        display_frame.pack(fill=tk.X, padx=0, pady=(0, 0))

        entry_frame = tk.Frame(display_frame, bg=THEME['border'],
                               highlightbackground=THEME['border'], highlightthickness=1)
        entry_frame.pack(fill=tk.X, padx=_scale(14), pady=(_scale(14), _scale(6)))

        self.input_field = tk.Entry(
            entry_frame, font=THEME['font_display'],
            textvariable=self.input_text, width=_scale(18), state='readonly',
            bg=THEME['display_bg'], fg=THEME['display_fg'],
            bd=0, justify=tk.RIGHT, insertbackground=THEME['fg'],
            readonlybackground=THEME['display_bg'],
            relief=tk.FLAT, highlightthickness=0
        )
        self.input_field.pack(fill=tk.X, ipady=_scale(14), padx=_scale(6), pady=_scale(6))

        status_frame = tk.Frame(display_frame, bg=THEME['bg'])
        status_frame.pack(fill=tk.X, padx=_scale(20), pady=(0, _scale(6)))

        self.mode_label = tk.Label(
            status_frame, text='DEG', font=THEME['font_status'],
            bg=THEME['bg'], fg=THEME['accent'], cursor='hand2',
            anchor=tk.W
        )
        self.mode_label.pack(side=tk.LEFT)
        self.mode_label.bind('<Button-1>', lambda e: self.toggle_mode())

        self.status_label = tk.Label(
            status_frame, textvariable=self.status_text,
            font=THEME['font_status'], bg=THEME['bg'], fg=THEME['btn_op_fg'],
            anchor=tk.E
        )
        self.status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def toggle_mode(self):
        self.deg_mode = not self.deg_mode
        self.mode_label.configure(text='DEG' if self.deg_mode else 'RAD')

    def make_btn(self, parent, text, color, fg_color, cmd, h=2, w=6, font=None):
        btn = tk.Button(
            parent, text=text, font=font or THEME['font_btn'],
            bg=color, fg=fg_color, bd=0, cursor='hand2',
            activebackground=THEME['btn_hover'], activeforeground=THEME['fg'],
            highlightthickness=0, pady=0, padx=0,
            width=w, height=h, command=cmd
        )
        btn.bind('<Enter>', lambda e: btn.configure(bg=THEME['btn_hover']))
        btn.bind('<Leave>', lambda e: btn.configure(bg=color))
        btn.bind('<ButtonPress-1>', lambda e: btn.configure(bg=THEME['accent'], fg=THEME['btn_eq_fg']))
        btn.bind('<ButtonRelease-1>', lambda e: btn.configure(bg=THEME['btn_hover'], fg=THEME['fg']))
        return btn

    def build_buttons(self):
        btns = tk.Frame(self.master, bg=THEME['bg'])
        btns.pack(padx=_scale(12), pady=(0, _scale(14)), fill=tk.BOTH, expand=True)

        sc = THEME['btn_sci']
        scf = THEME['btn_sci_fg']
        op = THEME['btn_op']
        opf = THEME['btn_op_fg']
        num = THEME['btn_num']
        nf = THEME['btn_num_fg']
        clr = THEME['btn_clear']
        clrf = THEME['btn_clear_fg']
        eq = THEME['btn_eq']
        eqf = THEME['btn_eq_fg']

        mk = lambda t, c, fc, cmd, h=2, w=6, fn=None: self.make_btn(btns, t, c, fc, cmd, h, w, fn)

        mk('sin', sc, scf, lambda: self.btn_sci('sin('), fn=THEME['font_sci']
           ).grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        mk('cos', sc, scf, lambda: self.btn_sci('cos('), fn=THEME['font_sci']
           ).grid(row=0, column=1, padx=2, pady=2, sticky='nsew')
        mk('tan', sc, scf, lambda: self.btn_sci('tan('), fn=THEME['font_sci']
           ).grid(row=0, column=2, padx=2, pady=2, sticky='nsew')
        mk('log', sc, scf, lambda: self.btn_sci('log10('), fn=THEME['font_sci']
           ).grid(row=0, column=3, padx=2, pady=2, sticky='nsew')

        mk('ln', sc, scf, lambda: self.btn_sci('log('), fn=THEME['font_sci']
           ).grid(row=1, column=0, padx=2, pady=2, sticky='nsew')
        mk('\u221a', sc, scf, lambda: self.btn_sci('sqrt('), fn=THEME['font_sci']
           ).grid(row=1, column=1, padx=2, pady=2, sticky='nsew')
        mk('x\u00b2', sc, scf, lambda: self.btn_click('**2'), fn=THEME['font_sci']
           ).grid(row=1, column=2, padx=2, pady=2, sticky='nsew')
        mk('x^y', sc, scf, lambda: self.btn_click('**'), fn=THEME['font_sci']
           ).grid(row=1, column=3, padx=2, pady=2, sticky='nsew')

        mk('\u03c0', sc, scf, lambda: self.btn_click('pi'), fn=THEME['font_sci']
           ).grid(row=2, column=0, padx=2, pady=2, sticky='nsew')
        mk('e', sc, scf, lambda: self.btn_click('e'), fn=THEME['font_sci']
           ).grid(row=2, column=1, padx=2, pady=2, sticky='nsew')
        mk('!', sc, scf, lambda: self.btn_sci('factorial('), fn=THEME['font_sci']
           ).grid(row=2, column=2, padx=2, pady=2, sticky='nsew')
        mk('1/x', sc, scf, lambda: self.btn_sci('inv('), fn=THEME['font_sci']
           ).grid(row=2, column=3, padx=2, pady=2, sticky='nsew')

        mk('(', op, opf, lambda: self.btn_click('('), fn=THEME['font_sci']
           ).grid(row=3, column=0, padx=2, pady=2, sticky='nsew')
        mk(')', op, opf, lambda: self.btn_click(')'), fn=THEME['font_sci']
           ).grid(row=3, column=1, padx=2, pady=2, sticky='nsew')
        mk('%', op, opf, lambda: self.btn_click('%'), fn=THEME['font_sci']
           ).grid(row=3, column=2, padx=2, pady=2, sticky='nsew')
        mk('\u232b', op, opf, self.btn_backspace
           ).grid(row=3, column=3, padx=2, pady=2, sticky='nsew')

        mk('C', clr, clrf, self.btn_clear
           ).grid(row=4, column=0, padx=2, pady=2, sticky='nsew')
        mk('7', num, nf, lambda: self.btn_click(7)
           ).grid(row=4, column=1, padx=2, pady=2, sticky='nsew')
        mk('8', num, nf, lambda: self.btn_click(8)
           ).grid(row=4, column=2, padx=2, pady=2, sticky='nsew')
        mk('9', num, nf, lambda: self.btn_click(9)
           ).grid(row=4, column=3, padx=2, pady=2, sticky='nsew')

        mk('/', op, opf, lambda: self.btn_click('/')
           ).grid(row=5, column=0, padx=2, pady=2, sticky='nsew')
        mk('4', num, nf, lambda: self.btn_click(4)
           ).grid(row=5, column=1, padx=2, pady=2, sticky='nsew')
        mk('5', num, nf, lambda: self.btn_click(5)
           ).grid(row=5, column=2, padx=2, pady=2, sticky='nsew')
        mk('6', num, nf, lambda: self.btn_click(6)
           ).grid(row=5, column=3, padx=2, pady=2, sticky='nsew')

        mk('*', op, opf, lambda: self.btn_click('*')
           ).grid(row=6, column=0, padx=2, pady=2, sticky='nsew')
        mk('1', num, nf, lambda: self.btn_click(1)
           ).grid(row=6, column=1, padx=2, pady=2, sticky='nsew')
        mk('2', num, nf, lambda: self.btn_click(2)
           ).grid(row=6, column=2, padx=2, pady=2, sticky='nsew')
        mk('3', num, nf, lambda: self.btn_click(3)
           ).grid(row=6, column=3, padx=2, pady=2, sticky='nsew')

        mk('-', op, opf, lambda: self.btn_click('-')
           ).grid(row=7, column=0, padx=2, pady=2, sticky='nsew')
        mk('0', num, nf, lambda: self.btn_click(0), fn=THEME['font_btn']
           ).grid(row=7, column=1, padx=2, pady=2, sticky='nsew')
        mk('.', op, opf, lambda: self.btn_click('.'), fn=THEME['font_sci']
           ).grid(row=7, column=2, padx=2, pady=2, sticky='nsew')
        mk('+', op, opf, lambda: self.btn_click('+')
           ).grid(row=7, column=3, padx=2, pady=2, sticky='nsew')

        mk('\u00b1', sc, scf, self.btn_negate, fn=THEME['font_sci']
           ).grid(row=8, column=0, padx=2, pady=2, sticky='nsew')
        mk('=', eq, eqf, self.btn_equal
           ).grid(row=8, column=1, columnspan=3, padx=2, pady=2, sticky='nsew')

        for r in range(9):
            btns.grid_rowconfigure(r, weight=1)
        for c in range(4):
            btns.grid_columnconfigure(c, weight=1)

    def on_key(self, event):
        if event.char.isdigit():
            self.btn_click(int(event.char))
        elif event.char in '+-*/.()%':
            self.btn_click(event.char)
        elif event.char in 'eE':
            self.btn_click('e')
        elif event.char == 'p':
            self.btn_click('pi')
        elif event.keysym == 'Return':
            self.btn_equal()
        elif event.keysym == 'BackSpace':
            self.btn_backspace()
        elif event.keysym == 'Delete' or event.keysym == 'Escape':
            self.btn_clear()

    def on_close(self):
        self.master.update_idletasks()
        self._save_x = self.master.winfo_x()
        self._save_y = self.master.winfo_y()
        self._save_w = self.master.winfo_width()
        self._save_h = self.master.winfo_height()
        if self._dialog('Quitter', '\u2716', 'Voulez-vous vraiment quitter ?',
                        [('Non', False), ('Oui', True)]):
            self.show_goodbye()

    def show_goodbye(self):
        self.master.withdraw()
        goodbye = tk.Toplevel(self.master)
        goodbye.title('')
        goodbye.configure(bg=THEME['bg'])
        goodbye.resizable(False, False)
        goodbye.overrideredirect(True)
        w, h = _scale(360), _scale(220)
        x = self._save_x + (self._save_w - w) // 2
        y = self._save_y + (self._save_h - h) // 2
        goodbye.geometry(f'{w}x{h}+{x}+{y}')

        top = tk.Frame(goodbye, bg=THEME['btn_clear'], height=_scale(3))
        top.pack(fill=tk.X)

        body = tk.Frame(goodbye, bg=THEME['bg'])
        body.pack(fill=tk.BOTH, expand=True, padx=_scale(20), pady=(_scale(20), _scale(16)))

        tk.Label(body, text='\u2716', font=('Segoe UI', _scale(42)),
                 bg=THEME['bg'], fg=THEME['btn_clear']).pack()
        tk.Label(body, text='Au revoir !', font=('Segoe UI', _scale(20), 'bold'),
                 bg=THEME['bg'], fg=THEME['fg']).pack(pady=(_scale(6), _scale(2)))
        tk.Label(body, text='Merci d\'avoir utilis\u00e9\nla Calculatrice Scientifique',
                 font=('Segoe UI', _scale(11)), bg=THEME['bg'], fg=THEME['btn_sci_fg'],
                 justify=tk.CENTER).pack(pady=(_scale(4), 0))

        self.master.after(1800, lambda: (goodbye.destroy(), self.master.destroy()))

    def _refresh_display(self):
        self.input_text.set(cm.to_display(self.expression))

    def btn_click(self, item):
        if self.input_text.get() == 'Bienvenue !':
            self.expression = ''
        if self.just_evaluated:
            if isinstance(item, str) and item in '+-*/.**%':
                pass
            else:
                self.expression = ''
            self.just_evaluated = False
        self.expression = self.expression + str(item)
        self._refresh_display()

    def btn_sci(self, func):
        if self.input_text.get() == 'Bienvenue !':
            self.expression = ''
        if self.just_evaluated:
            self.expression = ''
            self.just_evaluated = False
        self.expression = self.expression + func
        self._refresh_display()

    def btn_clear(self):
        self.expression = ''
        self.just_evaluated = False
        self._refresh_display()

    def btn_backspace(self):
        if self.just_evaluated:
            return
        self.expression = self.expression[:-1]
        self._refresh_display()

    def btn_negate(self):
        if self.just_evaluated:
            self.just_evaluated = False
        if self.expression == '' or self.expression == '0':
            return
        if self._is_simple_number(self.expression):
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
                self.expression = self.expression.lstrip('+')
            else:
                self.expression = '-' + self.expression
        else:
            self.expression = '-(' + self.expression + ')'
        self._refresh_display()

    @staticmethod
    def _is_simple_number(s):
        if not s:
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    def btn_equal(self):
        expr = cm.from_display(self.input_text.get())
        if expr == '' or expr == 'Bienvenue !':
            return
        try:
            if not self._check_parens(expr):
                self._dialog('Erreur', '!', 'Parenth\u00e8ses d\u00e9s\u00e9quilibr\u00e9es')
                return
            expr = cm.preprocess(expr)
            self.status_text.set('Les calculs se v\u00e9rifient')
            self.master.update_idletasks()
            result = cm.safe_eval(expr, deg_mode=self.deg_mode)
            result_str = str(result)
            self.input_text.set(result_str)
            self.expression = result_str
            self.just_evaluated = True
            self.status_text.set('')
        except cm.ExpressionError as e:
            self._dialog('Erreur', '!', str(e))
            self.input_text.set('')
            self.expression = ''
            self.just_evaluated = False
            self.status_text.set('')
        except Exception:
            self._dialog('Erreur', '!', 'Expression invalide')
            self.input_text.set('')
            self.expression = ''
            self.just_evaluated = False
            self.status_text.set('')

    def _check_parens(self, s):
        balance = 0
        for ch in s:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0


def show_splash(root):
    splash = tk.Toplevel(root)
    splash.title('')
    splash.configure(bg=THEME['bg'])
    splash.resizable(False, False)
    splash.overrideredirect(True)
    Calculator._center(splash, _scale(360), _scale(320))

    top = tk.Frame(splash, bg=THEME['accent'], height=_scale(4))
    top.pack(fill=tk.X)

    body = tk.Frame(splash, bg=THEME['bg'])
    body.pack(fill=tk.BOTH, expand=True, padx=_scale(20))

    logo_frame = tk.Frame(body, bg=THEME['display_bg'],
                          highlightbackground=THEME['border'], highlightthickness=1)
    logo_frame.pack(pady=(_scale(30), 0), ipadx=_scale(40), ipady=_scale(16))

    tk.Label(logo_frame, text='\u2328', font=('Segoe UI', _scale(42)),
             bg=THEME['display_bg'], fg=THEME['accent']).pack()
    tk.Label(logo_frame, text='Calculatrice', font=('Segoe UI', _scale(18), 'bold'),
             bg=THEME['display_bg'], fg=THEME['fg']).pack()
    tk.Label(logo_frame, text='Scientifique', font=('Segoe UI', _scale(18), 'bold'),
             bg=THEME['display_bg'], fg=THEME['accent']).pack()

    tk.Label(body, text='v2.0', font=('Segoe UI', _scale(11)),
             bg=THEME['bg'], fg=THEME['btn_sci_fg']).pack(pady=(_scale(8), 0))
    tk.Label(body, text='+ \u2212 \u00d7 \u00f7    sin cos tan log ln\n'
             '\u221a x\u00b2 x^y 1/x %    \u03c0 e ! ( )',
             font=('Segoe UI', _scale(11)), bg=THEME['bg'], fg=THEME['btn_op_fg'],
             justify=tk.CENTER).pack(pady=(_scale(8), 0))

    progress = tk.Frame(body, bg=THEME['border'], height=_scale(2))
    progress.pack(fill=tk.X, pady=(_scale(16), 0))
    fill = tk.Frame(progress, bg=THEME['accent'], height=_scale(2), width=0)
    fill.pack(side=tk.LEFT)

    def animate(i=0):
        if i <= 100:
            fill.configure(width=int(_scale(360) * i / 100))
            splash.after(18, lambda: animate(i + 1))
        else:
            w = _scale(360)
            h = _scale(650)
            root.geometry(f'{w}x{h}')
            Calculator._center(root, w, h)
            splash.destroy()
            root.deiconify()
            Calculator(root)

    splash.update()
    animate()


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    show_splash(root)
    root.mainloop()
