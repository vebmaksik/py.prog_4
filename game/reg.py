import json
import hashlib
import threading
import os
import random
import datetime
import getpass

class UserManager:
    def __init__(self, users_file="data/users.json", log_file="data/logs.txt", results_file="data/results.txt"):
        self.users_file = users_file
        self.log_file = log_file
        self.results_file = results_file
        self.users = self.load_users()
        self.lock = threading.Lock()

        self._ensure_file_exists(self.users_file)
        self._ensure_file_exists(self.log_file)
        self._ensure_file_exists(self.results_file)

    def _ensure_file_exists(self, filepath):
        """Убеждается, что файл существует; если нет - создает пустой."""
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                pass

                if filepath.endswith('.json'):
                    json.dump({}, f)

    def load_users(self):
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Ошибка: Файл users.json не найден. Создается новый файл.")
            return {}
        except json.JSONDecodeError:
            print("Ошибка: Некорректный формат файла users.json. Создается новый файл.")
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
            print(f"Ошибка: Файл логов {self.log_file} не найден.")
        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")

    def record_game_result(self, username, game_mode, attempts, won):
        thread = threading.Thread(target=self._record_game_result, args=(username, game_mode, attempts, won))
        thread.daemon = True
        thread.start()

    def _record_game_result(self, username, game_mode, attempts, won):
        try:
            with open(self.results_file, "a") as f:
                timestamp = datetime.datetime.now().isoformat()
                result_string = f"[{timestamp}] Пользователь: {username}, Режим: {game_mode}, Попытки: {attempts}, Победа: {won}\n"
                f.write(result_string)
        except FileNotFoundError:
            print(f"Ошибка: Файл результатов {self.results_file} не найден.")
        except Exception as e:
            print(f"Ошибка при записи в файл результатов: {e}")