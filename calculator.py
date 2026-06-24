import calculator_math as cm

try:
    import readline
except ImportError:
    pass

WELCOME = """
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551  CALCULATRICE SCIENTIFIQUE  \u2551
\u2551  + - * /  sin cos tan log   \u2551
\u2551  \u221a x\u00b2 x^y  \u03c0 e !  ( )       \u2551
\u2551  1/x %                         \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d
"""


def show_constants():
    print(f'\u03c0 (pi) = {cm.CONSTANTS["pi"]}')
    print(f'e = {cm.CONSTANTS["e"]}')
    print(f'\u03c0/2 = {cm.CONSTANTS["pi"] / 2}')
    print(f'2\u03c0 = {2 * cm.CONSTANTS["pi"]}')
    print(f'\u03c0\u00b2 = {cm.CONSTANTS["pi"] ** 2}')


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Entr\u00e9e invalide. Veuillez entrer un nombre.')


def confirm_quit():
    while True:
        ans = input('\u00cates-vous s\u00fbr de vouloir quitter ? (o/N): ').strip().lower()
        if ans in ('o', 'oui', 'y', 'yes'):
            return True
        if ans in ('', 'n', 'non', 'no'):
            return False
        print('Veuillez r\u00e9pondre par oui (o) ou non (n).')


def show_welcome():
    print(WELCOME)
    print('Bienvenue !')
    input('Appuyez sur Entr\u00e9e pour commencer...')


def show_goodbye():
    print()
    print('\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557')
    print('\u2551        Au revoir !          \u2551')
    print('\u2551  Merci d\'avoir utilis\u00e9 la   \u2551')
    print('\u2551   Calculatrice Scientifique  \u2551')
    print('\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d')
    print()


def main():
    show_welcome()

    while True:
        print()
        print('=== Menu ===')
        print('1. Addition')
        print('2. Soustraction')
        print('3. Multiplication')
        print('4. Division')
        print('5. Puissance (x^y)')
        print('6. Racine carr\u00e9e (\u221ax)')
        print('7. Sinus (degr\u00e9s)')
        print('8. Cosinus (degr\u00e9s)')
        print('9. Tangente (degr\u00e9s)')
        print('10. Logarithme base 10')
        print('11. Logarithme n\u00e9p\u00e9rien (ln)')
        print('12. Factorielle')
        print('13. Constantes math\u00e9matiques')
        print('14. Inverse (1/x)')
        print('15. Quitter')

        choice = input('Entrez votre choix (1-15): ')

        if choice == '15':
            if confirm_quit():
                show_goodbye()
                break
            continue

        if choice == '13':
            show_constants()
            continue

        if choice in ('1', '2', '3', '4', '5'):
            num1 = get_number('Entrez le premier nombre: ')
            num2 = get_number('Entrez le deuxi\u00e8me nombre: ')

            try:
                if choice == '1':
                    result = cm.add(num1, num2)
                    print(f'{num1} + {num2} = {result}')
                elif choice == '2':
                    result = cm.subtract(num1, num2)
                    print(f'{num1} - {num2} = {result}')
                elif choice == '3':
                    result = cm.multiply(num1, num2)
                    print(f'{num1} * {num2} = {result}')
                elif choice == '4':
                    result = cm.divide(num1, num2)
                    print(f'{num1} / {num2} = {result}')
                elif choice == '5':
                    result = cm.power(num1, num2)
                    print(f'{num1} ^ {num2} = {result}')
            except cm.ExpressionError as e:
                print(f'Erreur : {e}')

        elif choice in ('6', '7', '8', '9', '10', '11', '12', '14'):
            num = get_number('Entrez un nombre: ')

            try:
                if choice == '6':
                    result = cm.sqrt(num)
                    print(f'\u221a{num} = {result}')
                elif choice == '7':
                    result = cm.sin_deg(num)
                    print(f'sin({num}\u00b0) = {result}')
                elif choice == '8':
                    result = cm.cos_deg(num)
                    print(f'cos({num}\u00b0) = {result}')
                elif choice == '9':
                    result = cm.tan_deg(num)
                    print(f'tan({num}\u00b0) = {result}')
                elif choice == '10':
                    result = cm.log10(num)
                    print(f'log({num}) = {result}')
                elif choice == '11':
                    result = cm.ln(num)
                    print(f'ln({num}) = {result}')
                elif choice == '12':
                    result = cm.factorial(num)
                    print(f'{int(round(num))}! = {result}')
                elif choice == '14':
                    result = cm.inv(num)
                    print(f'1/{num} = {result}')
            except cm.ExpressionError as e:
                print(f'Erreur : {e}')
        else:
            print('Choix invalide. Veuillez entrer un nombre entre 1 et 15.')


if __name__ == '__main__':
    main()
