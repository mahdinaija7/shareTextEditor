import tkinter as tk
import socket
import winsound
from tkinter import filedialog
from functools import partial
from client import ConnectTo
from server import HostTo


class TextEditor:
    """
    Customize The Window --> Text Editor
    """

    class MenuBar:
        """  Create Custom Menu  """

        def __init__(self, text_editor):
            self.filename = None
            self.text_editor = text_editor
            # creating menubar
            self.menu = tk.Menu(self.text_editor.window)
            # adding it to window
            text_editor.window.config(menu=self.menu)

            # creating a dropdown menu
            file = tk.Menu(self.menu, tearoff=0)

            # adding menu
            file.add_command(label="New File", command=self.new_file)
            file.add_command(label="Open File", command=self.open_file)
            file.add_command(label="Save", command=self.save)
            file.add_command(label="Save As", command=self.save_as)
            file.add_command(label="Exit", command=self.text_editor.window.destroy)
            # add it to menu bar
            self.menu.add_cascade(label="File", menu=file)
            self.menu.add_command(label="Connect", command=self.connection_window)
            self.menu.add_command(label="Share", command=self.share_window)

        # clear the text editor
        def new_file(self):
            self.text_editor.textarea.delete(1.0, tk.END)

        # openning an existing file
        def open_file(self):
            self.filename = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[
                    ("All Files", "*.*"),
                    ("Text Files", "*.txt"),
                    ("Python Scripts", "*.py"),
                    ("Markdown Documents", "*.md"),
                    ("JavaScript Files", "*.js"),
                    ("HTML Documents", "*.html"),
                    ("CSS Documents", "*.css"),
                ],
            )

            if self.filename:
                self.text_editor.textarea.delete(1.0, tk.END)
                with open(self.filename, "r") as f:
                    self.text_editor.textarea.insert(1.0, f.read())

        # save as * the file
        def save_as(self):
            try:
                new_file = filedialog.asksaveasfilename(
                    initialfile="Untitled.txt",
                    defaultextension=".txt",
                    filetypes=[
                        ("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Python Scripts", "*.py"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css"),
                    ],
                )
                textarea_content = self.text_editor.textarea.get(1.0, tk.END)
                with open(new_file, "w") as f:
                    f.write(textarea_content)
                self.filename = new_file
            except Exception as e:
                print(e)

        # save on the same file
        def save(self):
            if self.filename:
                try:
                    textarea_content = self.text_editor.textarea.get(1.0, tk.END)
                    with open(self.filename, "w") as f:
                        f.write(textarea_content)
                except Exception as e:
                    print(e)
            else:
                self.save_as()

        # prompt a window to connect
        def connection_window(self):
            pop = self.text_editor.ConnectPop(self.text_editor)

        def share_window(self):
            pop = self.text_editor.SharePop(self.text_editor)

        # todo bind CTRL Z

    # connecting window (asking for link)

    class ConnectPop:
        """ Connect Window """

        def __init__(self, text_editor):

            # creating toplevel object
            window = tk.Toplevel(text_editor.window)
            window.wm_title("Connecting")
            self.window = window
            # center the window
            # changing size window
            center_pop(window, text_editor, (250, 70))
            # creating entry
            self.label = tk.Entry(window)
            # put placeholder
            self.placeholder()
            # bind focus in and focus out event to entry
            self.label.bind("<FocusIn>", self.focus_event)
            self.label.bind("<FocusOut>", self.focus_out_event)
            self.label.pack(fill="x")
            # connect button
            self.button_connect = tk.Button(
                window,
                text="Connect",
                command=lambda: text_editor.connect(self.label, self.window),
            )
            self.button_connect.pack(fill="both")
            # close button
            self.button_close = tk.Button(window, text="Close", command=window.destroy)
            self.button_close.pack(fill="both")

        def focus_event(self, *args):
            # checking color if it's grey
            if self.label["fg"] == "#8e8e8e":
                # delete content
                self.label.delete(0, "end")
                # restore black color
                self.label["fg"] = "black"

        def focus_out_event(self, *args):
            # check if there is text on entry
            if not self.label.get():
                # put placeholder
                self.placeholder()

        def placeholder(self):
            # putting text
            self.label.insert(0, "IP:PORT")
            # changing to low opactiy grey
            self.label["fg"] = "#8e8e8e"

    class SharePop:
        """ Share Window To Open Server """

        def __init__(self, text_editor):
            window = tk.Toplevel(text_editor.window)
            window.wm_title("Host Connection")
            self.window = window
            # centring the window on middle of parent
            center_pop(window, text_editor, (200, 104))
            # text Label
            label = tk.Label(window, text="Type Your Port To Host ON")
            label.pack()
            # text field (input)
            port_entry = tk.Entry(window)
            port_entry.pack(fill="x")
            # empty label to show result in it after clicking on button
            result_label = label = tk.Label(window, text="")

            result_label.pack(fill="both")
            result_label2 = label = tk.Label(window, text="")
            result_label2.config(fg="red")
            result_label2.pack(fill="both")
            # button to share
            button = tk.Button(
                window,
                text="Share",
                command=lambda: self.show_link_share(
                    result_label, result_label2, port_entry, text_editor
                ),
            )
            button.pack(fill="x")

        def show_link_share(self, labelone, labeltwo, portEntry, text_editor):
            port = portEntry.get()
            if port and port.isnumeric():
                labelone.config(text="here is your link")
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                link = f"{ip_address}:{port}"
                labeltwo.config(text=link)
                window.clipboard_clear()
                window.clipboard_append(link)
                window.update()
                text_editor.share(port, self.window)
            else:
                labelone.config(text="PLease Check Your Input")

    ### Text Editor Object ###
    ###################################################################
    def __init__(self, window):

        self.con = None
        self.host = None

        self.window = window
        # changing title of the window
        self.window.title("Share Code")
        # center window on middle of the screen
        center(self.window)

        ## TEXT AREA ##
        self.textarea = tk.Text(self.window, font="Arial")
        self.textarea.bind("<Key>", self.text_changed)

        ## SCROLL BAR ##
        self.scroll = tk.Scrollbar(self.window, command=self.textarea.yview)

        # connect text area with scroll bar
        self.textarea.configure(yscrollcommand=self.scroll.set)

        # packing text area on left
        # fill the free space
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.textarea.focus()

        # packing the scroll bar on right side
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu = self.MenuBar(self)

    # connecting to other peer
    def connect(self, label, pop_window):
        DELIIMTER = ":"
        label_content = label.get()
        if label_content and label_content != "IP:PORT":
            if DELIIMTER in label_content:
                # check if format is right
                # getting the input
                link_list = label_content.split(":")
                if len(list(filter(bool, link_list))) == 2:
                    # split it to host_ip and port
                    host = link_list[0]
                    port = int(link_list[1])
                    # run_(host, port)
                    self.con = ConnectTo(host, port, self.textarea)
                    self.con.start()
                    pop_window.destroy()
                # makes beep if !conditions
                else:

                    winsound.Beep(500, 100)
            else:
                winsound.Beep(500, 100)
        else:
            winsound.Beep(500, 100)

    def share(self, port, window):
        self.host = HostTo(port, self.textarea)
        self.host.start()
        # destroy the child window
        window.destroy()

    def text_changed(self, key):
        if self.con and self.con.connected or self.host and self.host.connected:
            new_text = self.textarea.get("1.0", "end")
            new_text = new_text.strip() + key.char
            if not self.host and self.con.connected:
                self.con.send_msg(new_text)
            elif not self.con and self.host.connected:
                self.host.send_msg(new_text)


# center any window on middle of screen
def center(win, width=800, height=400):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry("{}x{}+{}+{}".format(width, height, x, y))


# center child window
def center_pop(toplevel, parent, wh: tuple):
    x, y = (
        parent.window.winfo_x() + parent.window.winfo_width() / 2 - 150,
        parent.window.winfo_y() + parent.window.winfo_height() / 2 - 50,
    )
    w, h = wh
    toplevel.geometry("%dx%d+%d+%d" % (w, h, x, y))


if __name__ == "__main__":
    window = tk.Tk()
    edit_window = TextEditor(window)
    window.mainloop()

