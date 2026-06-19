import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title('Calculatrice')
        master.geometry('300x400')
        master.resizable(False, False)
        
        self.expression = ''
        self.input_text = tk.StringVar()
        self.status_text = tk.StringVar()
        
        # Entry field
        self.input_frame = tk.Frame(master, width=312, height=50, bd=0, highlightbackground='black', highlightcolor='black', highlightthickness=2)
        self.input_frame.pack(side=tk.TOP)
        
        self.input_field = tk.Entry(self.input_frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg='#eee', bd=0, justify=tk.RIGHT)
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=10)  # internal padding to increase height
        
        # Status label
        self.status_label = tk.Label(self.input_frame, textvariable=self.status_text, font=('arial', 10), bg='#eee')
        self.status_label.pack()
        
        # Buttons frame
        self.btns_frame = tk.Frame(master, width=312, height=272.5, bg='grey')
        self.btns_frame.pack()
        
        # First row
        self.clear = tk.Button(self.btns_frame, text='C', fg='black', width=32, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_clear())
        self.clear.grid(row=0, column=0, columnspan=3, padx=1, pady=1)
        
        self.divide = tk.Button(self.btns_frame, text='/', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_click('/'))
        self.divide.grid(row=0, column=3, padx=1, pady=1)
        
        # Second row
        self.seven = tk.Button(self.btns_frame, text='7', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(7))
        self.seven.grid(row=1, column=0, padx=1, pady=1)
        
        self.eight = tk.Button(self.btns_frame, text='8', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(8))
        self.eight.grid(row=1, column=1, padx=1, pady=1)
        
        self.nine = tk.Button(self.btns_frame, text='9', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(9))
        self.nine.grid(row=1, column=2, padx=1, pady=1)
        
        self.multiply = tk.Button(self.btns_frame, text='*', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_click('*'))
        self.multiply.grid(row=1, column=3, padx=1, pady=1)
        
        # Third row
        self.four = tk.Button(self.btns_frame, text='4', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(4))
        self.four.grid(row=2, column=0, padx=1, pady=1)
        
        self.five = tk.Button(self.btns_frame, text='5', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(5))
        self.five.grid(row=2, column=1, padx=1, pady=1)
        
        self.six = tk.Button(self.btns_frame, text='6', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(6))
        self.six.grid(row=2, column=2, padx=1, pady=1)
        
        self.minus = tk.Button(self.btns_frame, text='-', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_click('-'))
        self.minus.grid(row=2, column=3, padx=1, pady=1)
        
        # Fourth row
        self.one = tk.Button(self.btns_frame, text='1', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(1))
        self.one.grid(row=3, column=0, padx=1, pady=1)
        
        self.two = tk.Button(self.btns_frame, text='2', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(2))
        self.two.grid(row=3, column=1, padx=1, pady=1)
        
        self.three = tk.Button(self.btns_frame, text='3', fg='black', width=10, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(3))
        self.three.grid(row=3, column=2, padx=1, pady=1)
        
        self.plus = tk.Button(self.btns_frame, text='+', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_click('+'))
        self.plus.grid(row=3, column=3, padx=1, pady=1)
        
        # Fifth row
        self.zero = tk.Button(self.btns_frame, text='0', fg='black', width=21, height=3, bd=0, bg='#fff', cursor='hand2', command=lambda: self.btn_click(0))
        self.zero.grid(row=4, column=0, columnspan=2, padx=1, pady=1)
        
        self.point = tk.Button(self.btns_frame, text='.', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_click('.'))
        self.point.grid(row=4, column=2, padx=1, pady=1)
        
        self.equals = tk.Button(self.btns_frame, text='=', fg='black', width=10, height=3, bd=0, bg='#eee', cursor='hand2', command=lambda: self.btn_equal())
        self.equals.grid(row=4, column=3, padx=1, pady=1)
    
    def btn_click(self, item):
        self.expression = self.expression + str(item)
        self.input_text.set(self.expression)
    
    def btn_clear(self):
        self.expression = ''
        self.input_text.set('')
    
    def btn_equal(self):
        try:
            self.status_text.set("Les calculs se vérifient")
            self.master.update_idletasks()
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
            self.status_text.set('')
        except Exception as e:
            self.input_text.set('Erreur')
            self.expression = ''
            self.status_text.set('')
    

if __name__ == '__main__':
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

