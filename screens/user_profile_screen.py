# screens/user_profile_screen.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
from .screen import Screen

class UserProfileScreen(Screen):
    """
    The class that contains the interface for displaying all the individual details of any selected user.
    """
    def __init__(self, app, user_id, target_user_id):
        """
        Initializes the UserProfileScreen, setting up the interface to view another user's profile.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user.
            target_user_id (int): The ID of the user whose profile is being viewed.
        Returns:
            None
        """
        self.app = app
        self.user_id = user_id
        self.target_user_id = target_user_id
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to see all the relevant details of a particular user, and also interact
        with that user.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        # Page variables
        self.current_screen_page = 0
        self.tweets_per_page = 3
        self.tweets = []

        cursor = self.app.conn.cursor()

        # Get user information
        cursor.execute("SELECT name FROM users WHERE usr = ?", (self.target_user_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            self.app.show_search_users_screen(self.user_id)
            return
        name = result[0]

        # Get profile details with combined tweet and retweet count using UNION
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT tid FROM tweets WHERE writer_id = ?
                UNION ALL
                SELECT tid FROM retweets WHERE retweeter_id = ?
            )
        """, (self.target_user_id, self.target_user_id))
        num_tweets = cursor.fetchone()[0]

        # Get follower and following counts
        cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (self.target_user_id,))
        num_following = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (self.target_user_id,))
        num_followers = cursor.fetchone()[0]

        # Display profile info
        tk.Label(self.app.root, text=f"User Profile: {name} (ID: {self.target_user_id})", font=("Arial", 18)).pack(pady=10)
        info_text = f"Total Posts (Tweets & Retweets): {num_tweets}\nFollowing: {num_following}\nFollowers: {num_followers}"
        tk.Label(self.app.root, text=info_text).pack(pady=5)

        # Follow/Unfollow button
        cursor.execute("SELECT 1 FROM follows WHERE flwer = ? AND flwee = ?", (self.user_id, self.target_user_id))
        is_following = cursor.fetchone() is not None

        if self.target_user_id == self.user_id:
            follow_button = tk.Button(self.app.root, text="You cannot follow yourself", state=tk.DISABLED)
        elif is_following:
            follow_button = tk.Button(self.app.root, text="Unfollow", command=self.unfollow_user)
        else:
            follow_button = tk.Button(self.app.root, text="Follow", command=self.follow_user)
        follow_button.pack(pady=5)

        # Display recent tweets with clickable buttons
        tk.Label(self.app.root, text="Recent Tweets:", font=("Arial", 14)).pack(pady=5)
        self.tweets_frame = tk.Frame(self.app.root)
        self.tweets_frame.pack(pady=5)

        self.prev_button = tk.Button(self.app.root, text="Previous", command=self.show_prev_tweets)
        self.prev_button.pack(pady=5)
        self.more_button = tk.Button(self.app.root, text="More", command=self.show_more_tweets)
        self.more_button.pack(pady=5)

        # Load all tweets
        self.load_tweets()

        # Navigation buttons
        tk.Button(self.app.root, text="Back", command=lambda: self.app.back()).pack(pady=5)
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack()

    def load_tweets(self):
        """
        Fetches all tweets from the target user, ordered by date descending.
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()
        cursor.execute("""
            SELECT writer_id, tid, text, tdate, ttime FROM tweets
            WHERE writer_id = ?
            ORDER BY tdate DESC, ttime DESC
        """, (self.target_user_id,))
        self.tweets = cursor.fetchall()
        self.show_tweets()
        self.update_button_state()

    def show_tweets(self):
        """
        Displays the next set of 3 tweets, replacing the previous ones.
        Inputs:
            None
        Returns:
            None
        """
        # Clear the tweets frame before loading new tweets
        for widget in self.tweets_frame.winfo_children():
            widget.destroy()

        # Calculate start and end indices
        self.start_index = self.current_screen_page * self.tweets_per_page
        self.end_index = min(self.start_index + self.tweets_per_page, len(self.tweets))

        # Slice the tweets list to get the current batch
        current_tweets = self.tweets[self.start_index:self.end_index]

        if not current_tweets:
            # No more tweets to display
            messagebox.showinfo("Info", "No more tweets to display.")
            self.more_button.config(state=tk.DISABLED)
            return

        # Display the current batch of tweets
        for writer_id, tid, text, tdate, ttime in current_tweets:
            display_text = f"TID:{tid} (Date: {tdate} {ttime}) {text}"
            button = tk.Button(self.tweets_frame, text=display_text, wraplength=450, justify=tk.LEFT,
                               command=lambda tid=tid: self.app.show_tweet_detail_screen(self.user_id, tid))
            button.pack(pady=2, fill=tk.X)


    def show_prev_tweets(self):
        """
        Shows the previous list of tweets
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_page -= 1
        self.show_tweets()
        self.update_button_state()
    def show_more_tweets(self):
        """
        Loads the next list of tweets
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_page += 1
        self.show_tweets()
        self.update_button_state()

    def update_button_state(self):
        """
        Switches off the buttons when they are not needed
        Inputs:
            None
        Returns:
             None
        """
        if self.current_screen_page == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)
        # Disable the "More" button if there are no more tweets
        if (self.current_screen_page + 1) * self.tweets_per_page >= len(self.tweets):
            self.more_button.config(state=tk.DISABLED)
        else:
            self.more_button.config(state=tk.NORMAL)

    def follow_user(self):
        """
        A method that allows the user viewing the other user's profile to then follow them too
        Inputs:
            None
        Returns:
            None
        """
        if self.user_id == self.target_user_id:
            messagebox.showerror("Error", "You cannot follow yourself.")
            return

        cursor = self.app.conn.cursor()
        try:
            cursor.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?)", 
                           (self.user_id, self.target_user_id, datetime.date.today().strftime('%Y-%m-%d')))
            self.app.conn.commit()
            messagebox.showinfo("Success", "You are now following this user.")
            self.more_button.config(state=tk.NORMAL)  # Re-enable if needed

            # Update the interface
            self.app.clear_screen()
            self.app.reload()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Failed to follow the user.")

    def unfollow_user(self):
        """
        A method that allows the user already following another user to unfollow them
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()
        try:
            cursor.execute("DELETE FROM follows WHERE flwer = ? AND flwee = ?", 
                           (self.user_id, self.target_user_id))
            self.app.conn.commit()
            messagebox.showinfo("Success", "You have unfollowed this user.")
            self.more_button.config(state=tk.NORMAL)  # Re-enable if needed

            # Update the interface
            self.app.clear_screen()
            UserProfileScreen(self.app, self.user_id, self.target_user_id)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to unfollow: {e}")
