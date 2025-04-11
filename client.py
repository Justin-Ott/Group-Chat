import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import re
import webbrowser

EMOJI_MAP = {
    ":thumbsup:": "👍",
    ":smile:": "😄",
    ":heart:": "❤️",
    ":fire:": "🔥",
    ":sob:": "😭",
}

class ChatClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        self.gui_done = False
        self.running = True
        self.username = None

        self.connect_to_server()
        self.build_gui()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.window.mainloop()

    def connect_to_server(self):
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))
            exit()

        self.username = simpledialog.askstring("Username", "Enter your name:")
        if not self.username:
            self.sock.close()
            exit()

    def build_gui(self):
        self.window = tk.Tk()
        self.window.title(f"Chat Client - {self.username}")

        # UI frame for chat
        self.chat_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled', height=20, bg="#ffffff", font=("Arial", 11))
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.input_area = tk.Text(self.window, height=3, font=("Arial", 11))
        self.input_area.pack(padx=10, pady=(0, 5), fill=tk.X)
        self.input_area.bind("<Return>", self.send_message_event)
        self.input_area.bind("<Shift-Return>", lambda e: None) 
        self.input_area.bind("<KeyRelease>", self.emoji_autofill)

        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.gui_done = True

    def send_message_event(self, event):
        self.send_message()
        return "break"

    def emoji_autofill(self, event):
        text = self.input_area.get("1.0", tk.END)
        for key, emoji in EMOJI_MAP.items():
            if key in text:
                text = text.replace(key, emoji)
                self.input_area.delete("1.0", tk.END)
                self.input_area.insert("1.0", text)

    def send_message(self):
        raw_msg = self.input_area.get("1.0", tk.END).strip()
        self.input_area.delete("1.0", tk.END)
        if not raw_msg:
            return

        for key, emoji in EMOJI_MAP.items():
            raw_msg = raw_msg.replace(key, emoji)

        message = f"{self.username}: {raw_msg}"
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

        try:
            self.sock.sendall(message.encode())
        except:
            self.stop()


    def format_message(self, msg):
        # Convert URLs into clickable format
        url_regex = r"(https?://[^\s]+)"
        formatted_msg = re.sub(url_regex, lambda m: f"{m.group(0)}", msg)
        return formatted_msg

    def receive(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode()
                if msg:
                    formatted = self.format_message(msg)
                    if self.gui_done:
                        self.chat_area.config(state='normal')
                        self.chat_area.insert(tk.END, formatted + "\n")
                        self.chat_area.yview(tk.END)
                        self.chat_area.config(state='disabled')

                        # Bind all the clickable URLs
                        self.make_urls_clickable(formatted)
                else:
                    break
            except:
                break
        self.stop()

    def make_urls_clickable(self, message):
        """ Make all URLs clickable in the chat area """
        url_regex = r"(https?://[^\s]+)"
        urls = re.findall(url_regex, message)

        for url in urls:
            start_idx = self.chat_area.search(url, "1.0", tk.END)
            if start_idx:
                end_idx = f"{start_idx}+{len(url)}c"
                self.chat_area.tag_add("link", start_idx, end_idx)
                self.chat_area.tag_configure("link", foreground="blue", underline=True)
                self.chat_area.tag_bind("link", "<Button-1>", lambda e, url=url: webbrowser.open(url))

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.window.quit()

if __name__ == "__main__":
    ChatClient(host="127.0.0.1", port=5000)
