import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests
import json
from datetime import datetime

class CurrencyConverter:
    def __init__(self):
        self.api_key = "ВАШ_КЛЮЧ_API"
        self.history_file = "history.json"
        
        # Настройка окна
        self.root = ctk.CTk()
        self.root.title("Currency Converter")
        self.root.geometry("500x600")

        # Элементы интерфейса
        self.label = ctk.CTkLabel(self.root, text="Конвертер валют", font=("Arial", 20))
        self.label.pack(pady=20)

        self.amount_entry = ctk.CTkEntry(self.root, placeholder_text="Введите сумму")
        self.amount_entry.pack(pady=10)

        self.from_currency = ctk.CTkOptionMenu(self.root, values=["USD", "EUR", "RUB", "GBP"])
        self.from_currency.pack(pady=10)

        self.to_currency = ctk.CTkOptionMenu(self.root, values=["RUB", "USD", "EUR", "GBP"])
        self.to_currency.pack(pady=10)

        self.convert_button = ctk.CTkButton(self.root, text="Конвертировать", command=self.convert)
        self.convert_button.pack(pady=20)

        self.history_box = tk.Listbox(self.root, width=50, height=10)
        self.history_box.pack(pady=10)

        self.load_history()

    def convert(self):
        amount = self.amount_entry.get()
        
        # Валидация ввода
        if not amount.isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Введите положительное число")
            return

        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        
        try:
            url = f"https://exchangerate-api.com{self.api_key}/pair/{from_val}/{to_val}/{amount}"
            response = requests.get(url).json()
            
            if response['result'] == 'success':
                result = response['conversion_result']
                messagebox.showinfo("Результат", f"{amount} {from_val} = {result:.2f} {to_val}")
                self.save_to_history(from_val, to_val, amount, result)
            else:
                messagebox.showerror("Ошибка API", "Не удалось получить курс")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема с сетью: {e}")

    def save_to_history(self, f, t, amt, res):
        entry = f"{datetime.now().strftime('%H:%M')} | {amt} {f} -> {res:.2f} {t}"
        self.history_box.insert(0, entry)
        
        # Сохранение в JSON
        history_data = []
        try:
            with open(self.history_file, "r") as f_file:
                history_data = json.load(f_file)
        except FileNotFoundError:
            pass

        history_data.append(entry)
        with open(self.history_file, "w") as f_file:
            json.dump(history_data, f_file)

    def load_history(self):
        try:
            with open(self.history_file, "r") as f_file:
                data = json.load(f_file)
                for item in data:
                    self.history_box.insert(0, item)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = CurrencyConverter()
    app.root.mainloop()
