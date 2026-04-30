import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        
        self.quotes = [
            {"text": "Будьте сами собой, все остальные роли уже заняты.", "author": "Оскар Уайльд", "theme": "жизнь"},
            {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "theme": "жизнь"},
            {"text": "Будьте изменением, которое хотите видеть в мире.", "author": "Махатма Ганди", "theme": "мудрость"},
            {"text": "Воображение важнее знаний.", "author": "Альберт Эйнштейн", "theme": "мудрость"},
            {"text": "Лучший способ предсказать будущее - это создать его.", "author": "Абрахам Линкольн", "theme": "мотивация"},
            {"text": "Успех - это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "мотивация"},
            {"text": "Любовь - это когда счастье другого является необходимым условием твоего счастья.", "author": "Роберт Хайнлайн", "theme": "любовь"},
            {"text": "Любить - значит видеть чудо, невидимое для других.", "author": "Франсуа Мориак", "theme": "любовь"},
            {"text": "Сложнее всего начать действовать, всё остальное зависит только от упорства.", "author": "Амелия Эрхарт", "theme": "мотивация"},
            {"text": "В середине трудности находится возможность.", "author": "Альберт Эйнштейн", "theme": "мудрость"}
        ]
        
        self.history = []
        self.load_history()
        
        self.setup_ui()
        self.update_history_list()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        quote_frame = ttk.LabelFrame(main_frame, text="Цитата", padding="10")
        quote_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.quote_text = tk.Text(quote_frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
        self.quote_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        quote_frame.columnconfigure(0, weight=1)
        
        self.author_label = ttk.Label(quote_frame, text="", font=("Arial", 10, "italic"))
        self.author_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.theme_label = ttk.Label(quote_frame, text="", font=("Arial", 10))
        self.theme_label.grid(row=2, column=0, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Сгенерировать цитату", command=self.generate_quote).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Добавить цитату", command=self.open_add_quote_dialog).pack(side=tk.LEFT)
        
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.author_filter = ttk.Combobox(filter_frame, state="readonly", width=30)
        self.author_filter.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.theme_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.theme_filter.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=4, padx=(10, 0))
        
        self.update_filter_options()
        
        history_frame = ttk.LabelFrame(main_frame, text="История", padding="10")
        history_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(3, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)
        
        self.history_listbox = tk.Listbox(history_frame, height=15)
        self.history_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
    
    def generate_quote(self):
        filtered_quotes = self.get_filtered_quotes()
        
        if not filtered_quotes:
            messagebox.showinfo("Информация", "Нет цитат, соответствующих выбранным фильтрам.")
            return
        
        quote = random.choice(filtered_quotes)
        
        self.quote_text.configure(state=tk.NORMAL)
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(1.0, quote["text"])
        self.quote_text.configure(state=tk.DISABLED)
        
        self.author_label.configure(text=f"— {quote['author']}")
        self.theme_label.configure(text=f"Тема: {quote['theme']}")
        
        self.history.append(quote.copy())
        self.update_history_list()
        self.save_history()
    
    def get_filtered_quotes(self):
        filtered = self.quotes.copy()
        
        author = self.author_filter.get()
        theme = self.theme_filter.get()
        
        if author and author != "Все авторы":
            filtered = [q for q in filtered if q["author"] == author]
        
        if theme and theme != "Все темы":
            filtered = [q for q in filtered if q["theme"] == theme]
        
        return filtered
    
    def reset_filters(self):
        self.author_filter.set("Все авторы")
        self.theme_filter.set("Все темы")
    
    def update_filter_options(self):
        authors = ["Все авторы"] + sorted(list(set(q["author"] for q in self.quotes)))
        themes = ["Все темы"] + sorted(list(set(q["theme"] for q in self.quotes)))
        
        self.author_filter["values"] = authors
        self.theme_filter["values"] = themes
        
        self.author_filter.set("Все авторы")
        self.theme_filter.set("Все темы")
    
    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        
        for idx, quote in enumerate(self.history, 1):
            display_text = f"{idx}. \"{quote['text']}\" — {quote['author']} [{quote['theme']}]"
            self.history_listbox.insert(tk.END, display_text)
    
    def open_add_quote_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить цитату")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Текст цитаты:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        text_entry = tk.Text(dialog, height=5, width=50)
        text_entry.pack(padx=20, pady=(0, 10))
        
        ttk.Label(dialog, text="Автор:", font=("Arial", 10, "bold")).pack(pady=(5, 5))
        author_entry = ttk.Entry(dialog, width=50)
        author_entry.pack(padx=20, pady=(0, 10))
        
        ttk.Label(dialog, text="Тема:", font=("Arial", 10, "bold")).pack(pady=(5, 5))
        theme_entry = ttk.Entry(dialog, width=50)
        theme_entry.pack(padx=20, pady=(0, 10))
        
        def save_new_quote():
            text = text_entry.get(1.0, tk.END).strip()
            author = author_entry.get().strip()
            theme = theme_entry.get().strip()
            
            if not text or not author or not theme:
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            new_quote = {
                "text": text,
                "author": author,
                "theme": theme
            }
            
            self.quotes.append(new_quote)
            self.update_filter_options()
            self.save_quotes()
            
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            dialog.destroy()
        
        ttk.Button(dialog, text="Сохранить", command=save_new_quote).pack(pady=20)
    
    def save_history(self):
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")
    
    def load_history(self):
        try:
            if os.path.exists("history.json"):
                with open("history.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        self.history = json.loads(content)
                    else:
                        self.history = []
            else:
                self.history = []
        except json.JSONDecodeError:
            print("Файл истории поврежден, создаем новую историю")
            self.history = []
        except Exception as e:
            print(f"Ошибка при загрузке истории: {e}")
            self.history = []
    
    def save_quotes(self):
        try:
            with open("quotes_data.json", "w", encoding="utf-8") as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении цитат: {e}")

def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()