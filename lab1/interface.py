import tkinter as tk
import json
from tkinter import messagebox, scrolledtext
from summarize_api import summarize_text
from sentiment_api import analyze_sentiment_api

class TextAnalyzer:
    def __init__(self):
        pass

    def analyze_text(self, text, num_sentences=2):
        summary = summarize_text(text, num_sentences)
        sentiment_result = analyze_sentiment_api(summary) if summary else None
        return summary, sentiment_result

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Суммаризация и анализ тональности текста")

        self.lbl_input = tk.Label(self.root, text="Введите текст для суммаризации:")
        self.lbl_input.pack()

        self.txt_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10)
        self.txt_input.pack()

        self.btn_analyze = tk.Button(self.root, text="Анализировать", command=self.process_and_display_results)
        self.btn_analyze.pack()

        self.lbl_output = tk.Label(self.root, text="Результаты:")
        self.lbl_output.pack()

        self.txt_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10)
        self.txt_output.pack()

        self.analyzer = TextAnalyzer()

    def process_and_display_results(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для анализа.")
            return

        summary, sentiment_result = self.analyzer.analyze_text(text)

        result_message = "Результаты анализа:\n\n"
        if summary:
            result_message += f"Суммаризация:\n{summary}\n\n"
        else:
            result_message += "Не удалось получить резюме.\n\n"

        if sentiment_result:
            sentiment_data = json.loads(sentiment_result)
            result_message += (
                "Анализ тональности:\n"
                f"Положительная: {sentiment_data.get('pos', 'N/A')}\n"
                f"Нейтральная: {sentiment_data.get('neu', 'N/A')}\n"
                f"Отрицательная: {sentiment_data.get('neg', 'N/A')}\n"
                f"Сводный показатель (compound): {sentiment_data.get('compound', 'N/A')}\n"
                f"Общая тональность: {sentiment_data.get('sentiment', 'N/A')}\n"
            )
        else:
            result_message += "Не удалось получить результаты анализа тональности.\n"

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, result_message)