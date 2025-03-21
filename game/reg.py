import json
import hashlib
import threading
import os 

class UserManager:
    def __init__(self, users_file="data/users.json", log_file="data/logs.txt"):
        self.users_file = users_file
        self.log_file = log_file
        self.users = self.load_users()
        self.lock = threading.Lock()

        self.ensure_data_directory_exists()

    def ensure_data_directory_exists(self):
        if not os.path.exists("data"):
            try:
                os.makedirs("data")
                print("Создана папка 'data'.")
            except OSError as e:
                print(f"Ошибка при создании папки 'data': {e}")

        if not os.path.exists(self.log_file):
            try:
                with open(self.log_file, "w") as f:
                    pass
                print(f"Создан файл логов: {self.log_file}")
            except OSError as e:
                print(f"Ошибка при создании файла логов: {e}")




    def load_users(self):
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Ошибка: Некорректный формат файла users.json.  Создается новый файл.")
            return {}


    def save_users(self):
        with self.lock:
            with open(self.users_file, "w") as f:
                json.dump(self.users, f, indent=4)

    def register_user(self, username, password):
        if username in self.users:
            return False, "Пользователь с таким именем уже существует."

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_password
        self.save_users_threaded()
        self.log_message(f"Зарегистрирован новый пользователь: {username}")
        return True, "Регистрация прошла успешно."

    def authenticate_user(self, username, password):
        if username not in self.users:
            return False, "Пользователь не найден."

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self.users[username] == hashed_password:
            self.log_message(f"Пользователь {username} успешно авторизован.")
            return True, "Авторизация прошла успешно."
        else:
            return False, "Неверный пароль."

    def save_users_threaded(self):
        thread = threading.Thread(target=self.save_users)
        thread.daemon = True
        thread.start()

    def log_message(self, message):
        thread = threading.Thread(target=self._log_message, args=(message,))
        thread.daemon = True
        thread.start()

    def _log_message(self, message):
        try:
            with open(self.log_file, "a") as f:
                f.write(message + "\n")
        except FileNotFoundError:
            print(f"Ошибка: Файл логов {self.log_file} не найден.  Создается новый файл.")
            try:
                with open(self.log_file, "w") as f:
                    f.write(message + "\n")
            except OSError as e:
                print(f"Критическая ошибка при создании файла логов: {e}")
        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")


if __name__ == '__main__':
    user_manager = UserManager()