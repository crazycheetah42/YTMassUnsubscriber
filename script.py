# Importing necessary modules
from Google import create_service
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os

root = tk.Tk()
root.geometry('625x515')
root.iconbitmap("Resources/icon.ico")
root.title('YouTube Mass Unsubscribe Tool')

menubar = tk.Menu(root)
root.config(menu=menubar)

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

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

info_box = tk.Text(root)
info_box.insert("1.0", "To generate the authentication file necessary for this app to work, please refer to this video: https://youtu.be/qgeYIFb5kIY")
info_box.pack()

def open_subscription_window():
    """Opens a new window with checkboxes for each subscription."""
    # Check if CLIENT_FILE is set
    if not CLIENT_FILE:
        messagebox.showinfo("Client File Missing", "Please add a client-secret.json file to proceed.")
        return

    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
    sub_window = tk.Toplevel()
    sub_window.iconbitmap("Resources/icon.ico")
    sub_window.title("Your Subscriptions")
    sub_window.geometry("400x500")

    instructions = ttk.Label(
        sub_window,
        text="Here, you can choose which subscriptions you want to whitelist.\nThese are the ones you DON'T want to unsubscribe from.",
        wraplength=350,
        justify="center"
    )
    instructions.pack(pady=10)

    # Create a scrollable list for subscriptions
    list_frame = ttk.Frame(sub_window)
    list_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(list_frame)
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Fetch subscriptions and create checkboxes for each
    response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=50).execute()
    items = response.get("items", [])
    nextPageToken = response.get("nextPageToken")

    # Handle pagination for more subscriptions
    while nextPageToken:
        response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=50, pageToken=nextPageToken).execute()
        items.extend(response.get("items", []))
        nextPageToken = response.get("nextPageToken")

    # Store subscription names and checkbox states
    subscription_vars = {}
    for item in items:
        channel_name = item["snippet"]["title"]
        var = tk.BooleanVar(value=False)
        checkbox = ttk.Checkbutton(scrollable_frame, text=channel_name, variable=var)
        checkbox.pack(anchor="w", padx=10, pady=2)
        subscription_vars[channel_name] = var

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_confirm():
        whitelist = [name for name, var in subscription_vars.items() if var.get()]
        sub_window.destroy()
        threading.Thread(target=unsubscribe, args=(service, whitelist)).start()

    confirm_button = ttk.Button(sub_window, text="Confirm", command=on_confirm)
    confirm_button.pack(pady=10)

def unsubscribe(service, whitelist):
    """Unsubscribes from all channels not in the whitelist."""
    info_box.delete("1.0", "end")
    response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=50).execute()
    items = response.get("items", [])
    nextPageToken = response.get("nextPageToken")

    while nextPageToken:
        response = service.subscriptions().list(mine=True, part='id,snippet', maxResults=50, pageToken=nextPageToken).execute()
        items.extend(response.get("items", []))
        nextPageToken = response.get("nextPageToken")

    # Unsubscribe only from channels not in the whitelist
    for indx, item in enumerate(items):
        channel_name = item["snippet"]["title"]
        subscription_id = item["id"]

        if channel_name not in whitelist:
            service.subscriptions().delete(id=subscription_id).execute()
            info_box.insert("end", f"Unsubscribed from: {channel_name}\n")
            info_box.see("end")

    info_box.insert("end", "Unsubscribing finished.\n")
    info_box.see("end")

def start():
    open_subscription_window()

# Start button to initiate unsubscribe process
start_button = ttk.Button(root, text="Start", command=start)
start_button.pack(pady=20)

root.mainloop()