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

    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title('GPT-3.5')

        # 팝업 창 내용
        label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창 크기 조절
        window.update_idletasks()
        popup_width = label.winfo_reqwidth() + 20
        popup_height = label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창 중앙 위치
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")

        popup.transient(window)
        popup.attributes('-topmost', True)

        popup.update()
        return popup



    def on_send():
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)
        
        if user_input.lower() == "quit":
            window.destroy()
            return
        
        message_log.append({"role": "user", "content": user_input})

        thinking_popup = show_popup_message(window, "생각 중...")
        window.update_idletasks()  
        
        response = send_message(message_log)
        thinking_popup.destroy()

        message_log.append({"role": "assistant", "content": response})
        conversation.config(state=tk.NORMAL)    # conversation 수정가능하도록 설정
        conversation.insert(tk.END, f"You: {user_input}\n", "user") # tag를 추가한 부분
        conversation.insert(tk.END, f"AI assistant: {response}\n", "assistant")
        conversation.config(state=tk.DISABLED)  # conversation 수정 못하도록 설정
        conversation.see(tk.END)

    window = tk.Tk()
    window.title("AI Assistant")

    font = ("맑은 고딕", 10)

    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0', font=font)  # width, height를 없애고, 배경색 지정 (2)
    conversation.tag_configure("user", background="#c9daf8")  # tag별로 다르게 배경색 지정 (3)
    conversation.tag_configure("assistant", background="#e4e4e4")  # tag별로 다르게 배경색 지정 (3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # 윈도우 폭에 맞춰 크기 조정 (4)

    input_frame = tk.Frame(window)  # user_entry와 send_button을 담기 위한 frame (5)
    input_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)  # 윈도우 크기에 맞춰 조절되도록 (5)

    user_entry = tk.Entry(input_frame, font=font)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    send_button = tk.Button(input_frame, text="Send", command=on_send, font=font)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())

    window.mainloop()

if __name__ == "__main__":
    main()