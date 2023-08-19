import openai
import tkinter as tk
from tkinter import scrolledtext

openai.api_key = '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'

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        temperature=0.5,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content

def main():
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    def on_send():
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)
        
        if user_input.lower() == "quit":
            window.destroy()
            return
        
        message_log.append({"role": "user", "content": user_input})
        
        response = send_message(message_log)

        message_log.append({"role": "assistant", "content": response})
        conversation.insert(tk.END, f"You: {user_input}\n", "user")  # tag를 추가한 부분 (1)
        conversation.insert(tk.END, f"AI assistant: {response}\n", "assistant")  # tag를 추가한 부분 (1)
        conversation.see(tk.END)

    window = tk.Tk()
    window.title("AI Assistant")

    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0')  # width, height를 없애고, 배경색 지정 (2)
    conversation.tag_configure("user", background="#c9daf8")  # tag별로 다르게 배경색 지정 (3)
    conversation.tag_configure("assistant", background="#e4e4e4")  # tag별로 다르게 배경색 지정 (3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # 윈도우 폭에 맞춰 크기 조정 (4)

    input_frame = tk.Frame(window)  # user_entry와 send_button을 담기 위한 frame (5)
    input_frame.pack(fill=tk.X, padx=10, pady=10)  # 윈도우 크기에 맞춰 조절되도록 (5)

    user_entry = tk.Entry(input_frame)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    send_button = tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())

    window.mainloop()

if __name__ == "__main__":
    main()
