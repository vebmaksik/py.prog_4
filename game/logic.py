import random

def play_against_computer(username):
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print(f"Привет, {username}! Я загадал число от 1 до 100. Попробуй угадать.")

    while True:
        try:
            guess = int(input("Твоя попытка: "))
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
            break

def play_two_players(player1_username, player2_username):
    print(f"Привет, {player1_username} и {player2_username}!")
    secret_number = int(input(f"{player1_username}, загадай число от 1 до 100 для {player2_username}: "))

    attempts = 0
    while True:
        try:
            guess = int(input(f"{player2_username}, твоя попытка: "))
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
            break


if __name__ == '__main__':
    pass