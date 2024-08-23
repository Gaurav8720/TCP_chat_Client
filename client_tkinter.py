import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Set up the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    global nickname
    nickname = nickname_entry.get()
    if not nickname:
        messagebox.showwarning("Nickname Required", "Please enter a nickname!")
        return

    try:
        client.connect(("127.0.0.1", 55555))
        gui_chat()
        client.send(nickname.encode('ascii'))
    except:
        messagebox.showerror("Connection Error", "Unable to connect to the server.")
        return

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            else:
                chat_text_area.config(state=tk.NORMAL)
                chat_text_area.insert(tk.END, message + "\n")
                chat_text_area.yview(tk.END)
                chat_text_area.config(state=tk.DISABLED)
        except:
            messagebox.showerror("Connection Error", "An error occurred. Disconnecting...")
            client.close()
            break

def send_message():
    message = f"{nickname}: {message_entry.get()}"
    client.send(message.encode('ascii'))
    message_entry.delete(0, tk.END)

def gui_chat():
    # Hide the connection window
    connect_window.withdraw()

    # Create the main chat window
    global chat_window
    chat_window = tk.Toplevel(connect_window)
    chat_window.title("Chat Room")

    global chat_text_area
    chat_text_area = scrolledtext.ScrolledText(chat_window)
    chat_text_area.pack(padx=20, pady=5)
    chat_text_area.config(state=tk.DISABLED)

    global message_entry
    message_entry = tk.Entry(chat_window, width=50)
    message_entry.pack(padx=20, pady=5)
    message_entry.bind("<Return>", lambda event: send_message())

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack(padx=20, pady=5)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

# Create the initial connection window
connect_window = tk.Tk()
connect_window.title("Connect to Chat")

tk.Label(connect_window, text="Enter Nickname:").pack(padx=20, pady=5)
nickname_entry = tk.Entry(connect_window, width=30)
nickname_entry.pack(padx=20, pady=5)

connect_button = tk.Button(connect_window, text="Connect", command=connect_to_server)
connect_button.pack(padx=20, pady=20)

connect_window.mainloop()
