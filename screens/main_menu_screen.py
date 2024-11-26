# screens/main_menu_screen.py
import tkinter as tk
from .screen import Screen

class MainMenuScreen(Screen):
    """
    This class contains all the objects needed to build a main menu screen, which contains all the buttons needed to
    navigate to all the other interfaces
    """
    def __init__(self, app, user_id):
        """
        The constructor for the MainMenuScreen class, this constructor initializes and declares all Tkinter objects
        needed to create a working interface for the MainMenuScreen
        Inputs:
            app (App object): the app whose display we want to change to the login screen
            user_id (int): the id of the user whose screen that we want to display (is not directly used in this method,
            but we do need this information to pass it down to the called methods)
        Returns:
            None
        """
        self.app = app
        self.user_id = user_id
        self.name = None
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to see their main menu and navigate to any part of the program that they
        desire.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        # Create the main menu interface
        self.get_user_name()

        tk.Label(self.app.root, text="Main Menu", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.app.root, text=f"Welcome {self.name} (ID: {self.user_id})", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.app.root, text="View Feed", command=lambda: self.app.show_feed_screen(self.user_id)).pack(pady=5)
        tk.Button(self.app.root, text="Search for Users", command=lambda: self.app.show_search_users_screen(self.user_id)).pack(
            pady=5)
        tk.Button(self.app.root, text="Search for Tweets", command=lambda: self.app.show_search_tweets_screen(self.user_id)).pack(
            pady=5)
        tk.Button(self.app.root, text="Compose a Tweet", command=lambda: self.app.show_compose_tweet_screen(self.user_id)).pack(
            pady=5)
        tk.Button(self.app.root, text="List Followers", command=lambda: self.app.show_list_followers_screen(self.user_id)).pack(
            pady=5)
        tk.Button(self.app.root, text="Logout", command=lambda: self.app.logout()).pack(pady=10)

    def get_user_name(self):
        """
        Gets the current user's name from the table
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()

        cursor.execute("""
            SELECT name FROM users
            WHERE usr = ?
        """, (self.user_id,))

        self.name = cursor.fetchone()[0]
