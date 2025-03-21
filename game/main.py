from reg import UserManager
from logic import play_against_computer, play_two_players

def main():
    user_manager = UserManager()

    while True:
        print("\nДобро пожаловать в игру 'Угадай число'!")
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            success, message = user_manager.register_user(username, password)
            print(message)

        elif choice == "2":
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            success, message = user_manager.authenticate_user(username, password)
            if success:
                print(message)
                play_game(username, user_manager)
            else:
                print(message)

        elif choice == "3":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

def play_game(username, user_manager):
    while True:
        print("\nВыберите режим игры:")
        print("1. Игра против компьютера")
        print("2. Игра вдвоём")
        print("3. Выйти из аккаунта")

        mode_choice = input("Выберите режим: ")

        if mode_choice == "1":
            play_against_computer(username)
        elif mode_choice == "2":
            player2_username = input("Имя второго игрока: ")
            play_two_players(username, player2_username)
        elif mode_choice == "3":
            print("Вы вышли из аккаунта.")
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()