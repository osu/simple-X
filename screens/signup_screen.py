# screens/signup_screen.py
import tkinter as tk
from tkinter import messagebox
import re
from .screen import Screen

class SignupScreen(Screen):
    """
    This class contains all the features and functionality needed to display the screen that allows you to create a new
    twitter account.
    """
    def __init__(self, app):
        """
        The constructor for this class, it builds the display of the signup screen by creating objects that are provided
        by the classes of Tkinter to create various GUI features, such as buttons, text fields, and text displays
        Inputs:
            app (App object): the app whose display we want to change to the login screen
        Returns:
            None
        """
        self.app = app
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to submit their account information and sign up as a new user.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        # Create the signup interface
        tk.Label(self.app.root, text="Sign Up", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.app.root, text="Name").pack()
        self.name_entry = tk.Entry(self.app.root)
        self.name_entry.pack()

        tk.Label(self.app.root, text="Email").pack()
        self.email_entry = tk.Entry(self.app.root)
        self.email_entry.pack()

        tk.Label(self.app.root, text="Phone").pack()
        self.phone_entry = tk.Entry(self.app.root)
        self.phone_entry.pack()

        tk.Label(self.app.root, text="Password").pack()
        self.password_entry = tk.Entry(self.app.root, show="*")
        self.password_entry.pack()

        tk.Button(self.app.root, text="Submit", command=self.submit_signup).pack(pady=10)
        tk.Button(self.app.root, text="Back to Login", command=lambda: self.app.back()).pack()

    def submit_signup(self):
        """
        A function that activates whenever the user clicks the signup button, does all the processing necessary for the
        user to sign up
        Inputs:
            None
        Returns:
            None
        """
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()

        # Check if any field is empty
        if not name or not email or not phone or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        # Additional validation
        if any(char.isdigit() for char in name):
            messagebox.showwarning("Input Error", "Name should not contain numbers.")
            return
        if len(phone) != 10 or not phone.isdigit():
            messagebox.showwarning("Input Error", "Phone number must be exactly 10 digits.")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Input Error", "Email must contain '@' and a domain part (e.g., '.com').")
            return

        # Proceed with sign-up if all validations pass
        cursor = self.app.conn.cursor()
        cursor.execute("SELECT MAX(usr) FROM users")
        result = cursor.fetchone()
        new_usr = str(int(result[0]) + 1) if result[0] else '1'
        cursor.execute("INSERT INTO users (usr, name, email, phone, pwd) VALUES (?, ?, ?, ?, ?)",
                       (new_usr, name, email.lower(), phone, password))
        self.app.conn.commit()
        messagebox.showinfo("Sign Up Successful", f"Account created successfully! Your user ID is: {new_usr}")
        self.app.back()
