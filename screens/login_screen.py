# screens/login_screen.py
import tkinter as tk
from tkinter import messagebox
from .screen import Screen

class LoginScreen(Screen):
    """
    This class contains all the features and functionality needed to display the screen that allows you to log into your
    Twitter account.
    """
    def __init__(self, app):
        """
        The constructor for this class, it builds the display of the login screen by creating objects that are provided
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
        give the user the tools that they need to submit their account information and log in.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        # Create the login interface
        tk.Label(self.app.root, text="Login", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.app.root, text="User ID").pack()
        self.user_id_entry = tk.Entry(self.app.root)
        self.user_id_entry.pack()

        tk.Label(self.app.root, text="Password").pack()
        # by setting the show variable in the Entry object from tkinter to "*", we are hiding the password, which is
        # very important to avoid showing the password to anyone
        self.password_entry = tk.Entry(self.app.root, show="*")
        self.password_entry.pack()

        self.password_entry.bind("<Return>", lambda event: self.attempt_login())

        tk.Button(self.app.root, text="Login", command=self.attempt_login).pack(pady=10)
        tk.Button(self.app.root, text="Sign Up", command=self.app.show_signup_screen).pack()

    def attempt_login(self):
        """
        Queries the database to see if the entered username and password is really in the database
        Inputs:
            None
        Returns:
            None
        """
        user_id = self.user_id_entry.get().strip()
        password = self.password_entry.get()
        
        # Ensure user_id is a number
        if not user_id.isdigit():
            messagebox.showerror("Login Failed", "User ID must be a number.")
            return

        user_id = int(user_id)  # Convert to integer

        cursor = self.app.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE usr = ? AND pwd = ?", (user_id, password))
        user = cursor.fetchone()
        if user:
            # adds main menu to the stack
            self.app.show_main_menu(user_id)
            # adds and displays the feed screen on the stack
            self.app.show_feed_screen(user_id)
            # by changing the title of the application itself, the user can always be aware of their username and id
            # regardless of the page that they are on
            self.app.root.title("Barebones-Twitter " + user[1] + " (User ID:" + str(user_id) + ")")
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or Password")
