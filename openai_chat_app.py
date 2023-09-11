import tkinter as tk
from tkinter import scrolledtext, ttk
import os
import openai

# 環境変数からAPIキーを取得
api_key = os.environ.get('OPENAI_API_KEY')

# APIキーが設定されているか確認
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = api_key

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def send_message():
    user_message = user_input.get()
    chat_area.insert(tk.END, f"You: {user_message}\n")
    user_input.delete(0, tk.END)

    messages.append({"role": "user", "content": user_message})

    selected_model = model_combobox.get()
    max_tokens_val = int(max_tokens_input.get())

    # OpenAI APIを呼び出して回答を取得
    response = openai.ChatCompletion.create(
        model=selected_model,
        messages=messages,
        max_tokens=max_tokens_val
    )

    ai_message = response['choices'][0]['message']['content']
    chat_area.insert(tk.END, f"AI: {ai_message}\n")
    messages.append({"role": "assistant", "content": ai_message})


# GUIの設定
root = tk.Tk()
root.title("OpenAI Chat")
root.geometry("500x600")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_area.pack(pady=15)

model_label = tk.Label(root, text="Select Model:")
model_label.pack(pady=5)
available_models = ["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613",
                    "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
model_combobox = ttk.Combobox(root, values=available_models, state="readonly")
model_combobox.set("gpt-3.5-turbo")
model_combobox.pack(pady=5)

max_tokens_label = tk.Label(root, text="Max Tokens:")
max_tokens_label.pack(pady=5)
max_tokens_var = tk.StringVar()
max_tokens_var.set("1000")
max_tokens_input = tk.Spinbox(
    root, from_=1, to=1500, width=7, textvariable=max_tokens_var)
max_tokens_input.pack(pady=5)

user_input = tk.Entry(root, width=50)
user_input.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=20)

root.mainloop()
