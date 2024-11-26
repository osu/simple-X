# screens/list_followers_screen.py
import tkinter as tk
from tkinter import messagebox
from .screen import Screen

class ListFollowersScreen(Screen):
    """
    A class whose goal is to display all the followers of a given user.
    """
    def __init__(self, app, user_id):
        """
        The constructor for the ListFollowersScreen class, this constructor initializes and declares all Tkinter objects
        to allow the user to see a list of all of their followers.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user who wants to see all of their followers.
        Returns:
            None
        """
        self.app = app
        self.user_id = user_id
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to see all the accounts that are following them, and also to click on
        their account's homepage and view the information on their page
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        self.current_screen_index = 0
        self.followers = []

        tk.Label(self.app.root, text="Followers", font=("Arial", 18)).pack(pady=10)

        self.followers_frame = tk.Frame(self.app.root)
        self.followers_frame.pack(pady=5)

        self.nav_frame = tk.Frame(self.app.root)
        self.nav_frame.pack(pady=5)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.show_prev_followers)
        self.prev_button.pack(side=tk.LEFT)
        self.prev_button.config(state=tk.DISABLED)  # Disabled initially
        self.more_button = tk.Button(self.nav_frame, text="More", command=self.show_followers)
        self.more_button.pack(side=tk.LEFT)
        self.more_button.config(state=tk.DISABLED)  # Disabled initially

        self.back_button = tk.Button(self.app.root, text="Back", command=lambda: self.app.back())
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack()
        self.back_button.pack(pady=5)

        self.load_followers()

    def load_followers(self):
        """
        Queries the database to find the list of all followers for a given user.
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()
        cursor.execute("""
            SELECT u.usr, u.name FROM users u
            JOIN follows f ON u.usr = f.flwer
            WHERE f.flwee = ?
            ORDER BY u.name
        """, (self.user_id,))
        self.followers = cursor.fetchall()

        if not self.followers:
            messagebox.showinfo("No Followers", "You have no followers.")
            return

        self.show_followers()

        self.update_button_state()

    def show_followers(self):
        """
        This function is solely responsible for displaying all the items that are queried and staged to display in the
        followers list.
        Inputs:
            None
        Returns:
            None
        """
        # Show next 5 followers
        self.start_index = 5 * self.current_screen_index
        self.end_index = min(self.start_index + 5, len(self.followers))
        for i in range(self.start_index, self.end_index):
            usr_id, name = self.followers[i]
            button = tk.Button(self.followers_frame, text=f"{name} (ID: {usr_id})",
                               command=lambda uid=usr_id: self.view_follower(uid))
            button.pack(pady=2, fill=tk.X)

    def show_more_followers(self):
        """
        Loads the next list of followers
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index += 1
        self.show_followers()
        self.update_button_state()

    def show_prev_followers(self):
        """
        Shows the previous list of followers
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index -= 1
        self.show_followers()
        self.update_button_state()

    def update_button_state(self):
        """
        Switches off the buttons when they are not needed
        Inputs:
            None
        Returns:
             None
        """
        # Update "More" button state
        if (self.current_screen_index + 1) * 5 >= len(self.followers):
            self.more_button.config(state=tk.DISABLED)
        else:
            self.more_button.config(state=tk.NORMAL)

        # Update "Previous" button state
        if self.current_screen_index == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

    def view_follower(self, follower_id):
        """
        Allows the user to navigate to a selected follower's user profile page.
        Inputs:
            follower_id (int): The ID of the follower to view.
        Returns:
            None
        """
        self.app.show_user_profile_screen(self.user_id, follower_id)