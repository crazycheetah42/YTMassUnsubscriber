# Importing necessary modules
from Google import create_service
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os

root = tk.Tk()
root.geometry('625x501')
root.iconbitmap("Resources/icon.ico")
root.title('YouTube Mass Unsubscribe Tool')

menubar = tk.Menu(root)
root.config(menu=menubar)


#Empty string because it will be filled in by the user. 
CLIENT_FILE = ""

def open_client_secret():
    global CLIENT_FILE
    csfile = filedialog.askopenfile(filetypes=[("JSON Files", ".json")])
    if csfile:
        csfilepath = os.path.abspath(csfile.name)
        print("The file is located at: " + str(csfilepath))
        CLIENT_FILE = str(csfilepath)
        messagebox.showinfo("Successfully added", "The client-secret.json file was successfully added. Please do not delete/move the file.")

file_menu = tk.Menu(menubar)
file_menu.add_command(label="Open client secret file", command=open_client_secret)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

heading = ttk.Label(root, text="YT Mass Unsubscribe Tool", font=("Lucida Grande", 25))
heading.pack()

try:
    with open(CLIENT_FILE) as file:
        print('File recognized - client-secret.json')
except FileNotFoundError:
    print('File not found - client-secret.json')
    messagebox.showinfo("File not found", "You have not added a client-secret.json file, which is required for this application to work.\nIf you don\'t have a file, please check this project's GitHub repository for more info.")

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
    threading.Thread(target=unsubscribe).start()

    
start_button = ttk.Button(root, text="Start", command=start)
start_button.pack()
info_box = tk.Text(root)
info_box.pack()


root.mainloop()