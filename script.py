from Google import create_service
import tkinter as tk
from tkinter import ttk
import os

root = tk.Tk()
root.geometry('625x501')
root.title('YouTube Mass Unsubscriber')

menubar = tk.Menu(root)
root.config(menu=menubar)

CLIENT_FILE = ""

def open_client_secret():
    global CLIENT_FILE
    from tkinter import filedialog
    csfile = filedialog.askopenfile(filetypes=[("JSON Files", ".json")])
    if csfile:
        csfilepath = os.path.abspath(csfile.name)
        print("The file is located at: " + str(csfilepath))
        CLIENT_FILE = str(csfilepath)
        from tkinter import messagebox
        messagebox.showinfo("Successfully added", "The client-secret.json file was successfully added. Please do not delete/move the file.")

file_menu = tk.Menu(menubar)
file_menu.add_command(label="Open client secret file", command=open_client_secret)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

heading = ttk.Label(root, text="YouTube Mass Unsubscriber", font=("Lucida Grande", 25))
heading.pack()

try:
    with open(CLIENT_FILE) as file:
        print('File recognized - client-secret.json')
except FileNotFoundError:
    print('File not found - client-secret.json')
    from tkinter import messagebox
    messagebox.showerror("File not found", "The client-secret.json file was not found. Please make sure you have selected it through the app\'s file menu.\nIf you don\'t have a file, please watch this quick tutorial: https://www.youtube.com/watch?v=qgeYIFb5kIY")

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

def unsubscribe():
    print("Using client file " + str(CLIENT_FILE))
    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
    response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=10).execute()

    old_text = info_box.get("1.0", "end")
    new_text = old_text + "\n" + "Unsubscribing from your channels, please wait..."
    info_box.delete("1.0", "end")
    info_box.insert("1.0", new_text)

    items = []
    items.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=10, pageToken=nextPageToken).execute()
        items.extend(response.get('items'))
        nextPageToken = response.get('nextPageToken')


    for indx, item in enumerate(items):
        subscription_id = item['id']
        channel_name = item['snippet']['title']

        service.subscriptions().delete(id=subscription_id).execute()
        print(f"#{indx} channel {channel_name} has been unsubscribed")
        old_text = info_box.get("1.0", "end")
        new_text = old_text + "\n" + f"#{indx} channel {channel_name} has been unsubscribed"
        info_box.delete("1.0", "end")
        info_box.insert("1.0", new_text)
    old_text = info_box.get("1.0", "end")
    new_text = old_text + "\n" + "Unsubscribing finished."
    info_box.delete("1.0", "end")
    info_box.insert("1.0", new_text)
    

def start():
    import threading
    threading.Thread(target=unsubscribe).start()

    
start_button = ttk.Button(root, text="Start", command=start)
start_button.pack()
info_box = tk.Text(root)
info_box.pack()


root.mainloop()
