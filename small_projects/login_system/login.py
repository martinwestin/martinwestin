import tkinter as tk
from tkinter import messagebox
from models import DBModels


class LoginSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.widgets = []
        self.models_instance = DBModels()
    
    def main_interface(self):
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()

        create_btn = tk.Button(self, text="Create account", command=lambda: self.create_account_page())
        create_btn.pack()
        login_btn = tk.Button(self, text="Login", command=lambda: self.login_page())
        login_btn.pack()

        self.widgets.append(create_btn)
        self.widgets.append(login_btn)
    
    def create_account_page(self):
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()
        
        username_label = tk.Label(self, text="Enter a username")
        username_label.pack()
        username_input = tk.Entry(self)
        username_input.pack()

        password_label = tk.Label(self, text="Enter a password")
        password_label.pack()
        password_input = tk.Entry(self, show="*")
        password_input.pack()

        confirm_label = tk.Label(self, text="Confirm your password")
        confirm_label.pack()
        confirm_input = tk.Entry(self, show="*")
        confirm_input.pack()

        create_btn = tk.Button(self, text="Create", command=lambda: self.create_user(username_input.get(), password_input.get(), confirm_input.get()))
        create_btn.pack()

        back_btn = tk.Button(self, text="Back", command=lambda: self.main_interface())
        back_btn.pack()

        self.widgets.append(back_btn)
        self.widgets.append(username_label)
        self.widgets.append(username_input)
        self.widgets.append(password_label)
        self.widgets.append(password_input)
        self.widgets.append(confirm_label)
        self.widgets.append(confirm_input)
        self.widgets.append(create_btn)

    def login_page(self):
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()
        
        username_label = tk.Label(self, text="Enter your username")
        username_label.pack()
        username_input = tk.Entry(self)
        username_input.pack()

        password_label = tk.Label(self, text="Enter your password")
        password_label.pack()
        password_input = tk.Entry(self, show="*")
        password_input.pack()

        login_btn = tk.Button(self, text="Login", command=lambda: self.login_user(username_input.get(), password_input.get()))
        login_btn.pack()

        back_btn = tk.Button(self, text="Back", command=lambda: self.main_interface())
        back_btn.pack()
        
        self.widgets.append(back_btn)
        self.widgets.append(username_label)
        self.widgets.append(username_input)
        self.widgets.append(password_label)
        self.widgets.append(password_input)
        self.widgets.append(login_btn)
    
    def create_user(self, username, password, confirm):
        if self.models_instance.username_available(username):
            if len(password) >= 6 and password == confirm:
                self.models_instance.create_account(username, password)
                messagebox.showinfo("Success", "Account created!")
            else:
                messagebox.showerror("Error", "Make sure to confirm your password and that it is at least 6 characters long.")
        
        else:
            messagebox.showerror("Error", "Username not avaidable")
    
    def login_user(self, username, password):
        if self.models_instance.successfull_login(username, password):
            messagebox.showinfo("Success", "Logged in!")
        else:
            messagebox.showerror("Error", "Wrong username or password")

login = LoginSystem()
login.main_interface()
login.mainloop()
