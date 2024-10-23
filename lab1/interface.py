import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from summarize_api1 import summarize_text1
from summarize_api2 import summarize_text2
from sentiment_api import analyze_sentiment_api

class TextAnalyzer:
    def __init__(self):
        pass

    def analyze_text(self, text, num_sentences=4):
        summary1 = summarize_text1(text, num_sentences)
        sentiment_result1 = analyze_sentiment_api(summary1) if summary1 else None
        summary2 = summarize_text2(text, num_sentences)
        sentiment_result2 = analyze_sentiment_api(summary2) if summary2 else None
        return summary1, summary2, sentiment_result1, sentiment_result2

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarization and Sentiment Analysis")
        self.root.geometry("800x1000")

        self.root.configure(bg='#E0F7FA')

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.lbl_input = ttk.Label(self.root, text="Enter the text for summarization:", background='#E0F7FA', font=('Arial', 14))
        self.lbl_input.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.txt_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=10, bg='#E3F2FD', font=('Arial', 14))
        self.txt_input.grid(row=1, column=0, padx=10, pady=10)

        self.btn_analyze = ttk.Button(self.root, text="Analyze", command=self.process_and_display_results)
        self.btn_analyze.grid(row=2, column=0, padx=10, pady=10)

        self.lbl_summary1 = ttk.Label(self.root, text="Summary 1 and Sentiment Analysis 1:", background='#E0F7FA', font=('Arial', 14))
        self.lbl_summary1.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.txt_summary1 = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=5, bg='#E3F2FD', font=('Arial', 14))
        self.txt_summary1.grid(row=4, column=0, padx=10, pady=5)

        self.lbl_sentiment1 = ttk.Label(self.root, text="Sentiment analysis results for summary 1:", background='#E0F7FA', font=('Arial', 14))
        self.lbl_sentiment1.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.txt_sentiment1 = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=4, bg='#E3F2FD', font=('Arial', 14))
        self.txt_sentiment1.grid(row=6, column=0, padx=10, pady=5)

        self.lbl_summary2 = ttk.Label(self.root, text="Summary 2 and Sentiment Analysis 2:", background='#E0F7FA', font=('Arial', 14))
        self.lbl_summary2.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.txt_summary2 = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=5, bg='#E3F2FD', font=('Arial', 14))
        self.txt_summary2.grid(row=8, column=0, padx=10, pady=5)

        self.lbl_sentiment2 = ttk.Label(self.root, text="Sentiment analysis results for summary 2:", background='#E0F7FA', font=('Arial', 14))
        self.lbl_sentiment2.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)

        self.txt_sentiment2 = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=4, bg='#E3F2FD', font=('Arial', 14))
        self.txt_sentiment2.grid(row=10, column=0, padx=10, pady=5)

        self.analyzer = TextAnalyzer()

    def process_and_display_results(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text for analysis.")
            return

        self.txt_summary1.delete("1.0", tk.END)
        self.txt_sentiment1.delete("1.0", tk.END)
        self.txt_summary2.delete("1.0", tk.END)
        self.txt_sentiment2.delete("1.0", tk.END)

        summary1, summary2, sentiment_result1, sentiment_result2 = self.analyzer.analyze_text(text)

        if summary1:
            self.txt_summary1.insert(tk.END, f"{summary1}\n")
        else:
            self.txt_summary1.insert(tk.END, "Failed to generate summary 1.\n")

        if sentiment_result1:
            sentiment_data1 = json.loads(sentiment_result1)
            sentiment1_text = (
                f"Positive: {sentiment_data1.get('pos', 'N/A')}\n"
                f"Neutral: {sentiment_data1.get('neu', 'N/A')}\n"
                f"Negative: {sentiment_data1.get('neg', 'N/A')}\n"
                f"Compound: {sentiment_data1.get('compound', 'N/A')}\n"
            )
            self.txt_sentiment1.insert(tk.END, sentiment1_text)
        else:
            self.txt_sentiment1.insert(tk.END, "Failed to generate sentiment analysis for summary 1.\n")

        if summary2:
            self.txt_summary2.insert(tk.END, f"{summary2}\n")
        else:
            self.txt_summary2.insert(tk.END, "Failed to generate summary 2.\n")

        if sentiment_result2:
            sentiment_data2 = json.loads(sentiment_result2)
            sentiment2_text = (
                f"Positive: {sentiment_data2.get('pos', 'N/A')}\n"
                f"Neutral: {sentiment_data2.get('neu', 'N/A')}\n"
                f"Negative: {sentiment_data2.get('neg', 'N/A')}\n"
                f"Compound: {sentiment_data2.get('compound', 'N/A')}\n"
            )
            self.txt_sentiment2.insert(tk.END, sentiment2_text)
        else:
            self.txt_sentiment2.insert(tk.END, "Failed to generate sentiment analysis for summary 2.\n")
