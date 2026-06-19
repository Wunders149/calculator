def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return 'Erreur : Division par zéro'
    return x / y

def main():
    print('Sélectionnez une opération :')
    print('1. Addition')
    print('2. Soustraction')
    print('3. Multiplication')
    print('4. Division')
    print('5. Quitter')

    while True:
        choice = input("Entrez votre choix (1/2/3/4/5): ")

        if choice == '5':
            print('Au revoir !')
            break

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input('Entrez le premier nombre: '))
                num2 = float(input('Entrez le deuxième nombre: '))
            except ValueError:
                print('Entrée invalide. Veuillez entrer un nombre.')
                continue

            if choice == '1':
                result = add(num1, num2)
                print(f'{num1} + {num2} = {result}')
            elif choice == '2':
                result = subtract(num1, num2)
                print(f'{num1} - {num2} = {result}')
            elif choice == '3':
                result = multiply(num1, num2)
                print(f'{num1} * {num2} = {result}')
            elif choice == '4':
                result = divide(num1, num2)
                print(f'{num1} / {num2} = {result}')
        else:
            print('Choix invalide. Veuillez entrer un nombre entre 1 et 5.')

if __name__ == '__main__':
    main()
