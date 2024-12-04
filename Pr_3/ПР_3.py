import string


english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"



def atbash_cipher(text, alphabet):
    reverse_alphabet = alphabet[::-1]
    translation_table = str.maketrans(alphabet, reverse_alphabet)
    return text.translate(translation_table)



def main():
    while True:
        print("Выберите действие:")
        print("1 - Зашифровать сообщение (Атбаш)")
        print("2 - Дешифровать сообщение (Атбаш)")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            text = input("Введите текст для шифрования: ")
            alphabet_choice = input("Выберите алфавит (1 - английский, 2 - русский): ")

            if alphabet_choice == "1":
                result = atbash_cipher(text, english_alphabet)
            elif alphabet_choice == "2":
                result = atbash_cipher(text, russian_alphabet)
            else:
                print("Неверный выбор алфавита.")
                continue

            print(f"Зашифрованное сообщение: {result}")

        elif choice == "2":
            text = input("Введите текст для дешифрования: ")
            alphabet_choice = input("Выберите алфавит (1 - английский, 2 - русский): ")

            if alphabet_choice == "1":
                result = atbash_cipher(text, english_alphabet)
            elif alphabet_choice == "2":
                result = atbash_cipher(text, russian_alphabet)
            else:
                print("Неверный выбор алфавита.")
                continue

            print(f"Дешифрованное сообщение: {result}")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Выберите приемлимую цифру.")


if __name__ == '__main__':
    main()
