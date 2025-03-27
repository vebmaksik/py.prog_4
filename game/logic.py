import random
import datetime
import getpass

def get_masked_input(prompt):
    """Запрашивает ввод, скрывая вводимые символы."""
    return getpass.getpass(prompt=prompt)

def play_against_computer(username, user_manager):
    secret_number = random.randint(1, 100)
    attempts = 0
    won = False

    print(f"Привет, {username}! Я загадал число от 1 до 100. Попробуй угадать.")

    while True:
        try:
            guess = int(get_masked_input("Твоя попытка: "))
            attempts += 1
        except ValueError:
            print("Пожалуйста, введите целое число.")
            continue

        if guess < secret_number:
            print("Загаданное число больше.")
        elif guess > secret_number:
            print("Загаданное число меньше.")
        else:
            print(f"Поздравляю, {username}! Ты угадал число {secret_number} за {attempts} попыток.")
            won = True
            break

    user_manager.record_game_result(username, "Игра против компьютера", attempts, won)


def play_two_players(player1_username, player2_username, user_manager):
    print(f"Привет, {player1_username} и {player2_username}!")
    secret_number = int(get_masked_input(f"{player1_username}, загадай число от 1 до 100 для {player2_username}: "))

    attempts = 0
    won = False

    while True:
        try:
            guess = int(get_masked_input(f"{player2_username}, твоя попытка: "))
            attempts += 1
        except ValueError:
            print("Пожалуйста, введите целое число.")
            continue

        if guess < secret_number:
            print("Загаданное число больше.")
        elif guess > secret_number:
            print("Загаданное число меньше.")
        else:
            print(f"Поздравляю, {player2_username}! Ты угадал число {secret_number} за {attempts} попыток.")
            won = True
            break

    user_manager.record_game_result(player2_username, "Игра вдвоём", attempts, won)