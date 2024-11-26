# screens/search_users_screen.py
import tkinter as tk
from tkinter import messagebox
from .screen import Screen

class SearchUsersScreen(Screen):
    """
    This class contains the interface needed to allow the user to search for other users on the website.
    """
    def __init__(self, app, user_id):
        """
        The constructor for the SearchUsersScreen class, this constructor initializes and declares all Tkinter objects
        to create a working interface for the user to search through users.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user.
        Returns:
            None
        """
        self.app = app
        self.user_id = int(user_id)
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to submit their search for a specific username.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        self.current_screen_index = 0
        self.users = []

        tk.Label(self.app.root, text="Search Users", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.app.root, text="Enter Keyword").pack()
        self.keyword_entry = tk.Entry(self.app.root)
        self.keyword_entry.pack()

        self.keyword_entry.bind("<Return>", lambda event: self.search_users())

        self.search_button = tk.Button(self.app.root, text="Search", command=self.search_users)
        self.search_button.pack(pady=5)

        self.users_frame = tk.Frame(self.app.root)
        self.users_frame.pack(pady=5)

        self.nav_frame = tk.Frame(self.app.root)
        self.nav_frame.pack(pady=5)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.show_prev_users)
        self.prev_button.pack(side=tk.LEFT)
        self.prev_button.config(state=tk.DISABLED)  # Disabled initially

        self.more_button = tk.Button(self.nav_frame, text="More", command=self.show_more_users)
        self.more_button.pack(side=tk.LEFT)
        self.more_button.config(state=tk.DISABLED)  # Disabled initially

        self.back_button = tk.Button(self.app.root, text="Back",
                                     command=lambda: self.app.back())
        self.back_button.pack(pady=5)

    def search_users(self):
        """
        This function allows the user to take input from the search, and then query the database to extract all users
        that match the search by name through keywords.
        Inputs:
            None
        Returns:
            None
        """
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        # Clear previous results
        for widget in self.users_frame.winfo_children():
            widget.destroy()
        self.current_screen_index = 0  # Reset index
        self.users = []
        self.more_button.config(state=tk.DISABLED)

        # Split search string into keywords separated by comma and convert it to lower case, using list comprehension
        keywords = ['%' + keyword.lower().strip() + '%' for keyword in keyword.strip().split(',') if keyword.strip() and keyword.strip() != '']

        if  keywords is None or len(keywords) == 0 or  "" in keywords or None in keywords:
            messagebox.showwarning("Warning", "Please enter keyword for search separated by comma.")
            return

        if not keywords:
            messagebox.showwarning("Warning", "Please enter one or more keywords.")
            return
        # Check for duplicate values by removing duplicates using set and comparing list length with original list
        if len(keywords) != len(set(keywords)):
            messagebox.showwarning("Warning", "Please remove duplicate keyword from search. Search keywords are not case sensitive.")
            return

        # we use list comprehension to create a list of parameterized query conditional statements. The join makes a
        # compact and easy way to both get the "OR" connective in between the keywords without getting them at the ends
        search_condition = " OR ".join([" LOWER(name) LIKE ? " for keyword in keywords])

        # the query first orders the user names by order of increasing length. Then if the lenghs are tied, we break the
        # tie in lexicographic order by using name, and then lexicographically sort by the user id
        query_for_sql = "SELECT usr, name FROM users  WHERE " + search_condition + " ORDER BY LENGTH(name), name, usr"

        cursor = self.app.conn.cursor()

        # run the parameterized query and also pass in the parameters
        cursor.execute(query_for_sql, tuple(keywords))
        matches = cursor.fetchall()

        self.users = matches

        if not self.users:
            messagebox.showinfo("No Results", "No users found.")
            return

        self.show_users()

        self.update_button_state()

    def show_users(self):
        """
        Displays the next set of users based on the current index.
        Inputs:
            None
        Returns:
            None
        """
        # Clear previous results
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        # Show next 5 users
        self.start_index = 5 * self.current_screen_index
        self.end_index = min(self.start_index + 5, len(self.users))
        for i in range(self.start_index, self.end_index):
            usr_id, name = self.users[i]
            button = tk.Button(self.users_frame, text=f"{name} (ID: {usr_id})",
                               command=lambda uid=usr_id: self.view_user(uid))
            button.pack(pady=2, fill=tk.X)

    def show_prev_users(self):
        """
        Shows the previous list of users
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index -= 1
        self.show_users()
        self.update_button_state()

    def show_more_users(self):
        """
        Loads the next list of users
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index += 1
        self.show_users()
        self.update_button_state()

    def update_button_state(self):
        """
        Switches off the buttons when they are not needed
        Inputs:
            None
        Returns:
             None
        """
        # Update the "Previous" button state
        if self.current_screen_index == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        # Update the "More" button state
        if (self.current_screen_index + 1) * 5 >= len(self.users):
            self.more_button.config(state=tk.DISABLED)
        else:
            self.more_button.config(state=tk.NORMAL)

    def view_user(self, target_user_id):
        """
        Navigates to the selected user's profile screen.
        Inputs:
            target_user_id (int): The ID of the user to view.
        Returns:
            None
        """
        self.app.show_user_profile_screen(self.user_id, int(target_user_id))
