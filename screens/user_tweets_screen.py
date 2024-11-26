# screens/user_tweets_screen.py
import tkinter as tk
from tkinter import messagebox
from .screen import Screen

class UserTweetsScreen(Screen):
    """
    This class mainly displays detailed information about the tweets of a single user.
    """
    def __init__(self, app, user_id, target_user_id):
        """
        Initializes the UserTweetsScreen, setting up the interface to view a user's tweets.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user.
            target_user_id (int): The ID of the user whose tweets are being viewed.
        Returns:
            None
        """
        self.app = app
        self.user_id = int(user_id)
        self.target_user_id = int(target_user_id)
        self.build_user_interface()

    def build_user_interface(self):
        self.app.clear_screen()

        # self.current_screen_index = 0
        # self.tweets = []

        cursor = self.app.conn.cursor()
        cursor.execute("SELECT name FROM users WHERE usr = ?", (self.target_user_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            self.app.show_main_menu(self.user_id)
            return
        name = result[0]

        # Get profile details
        cursor.execute("SELECT COUNT(*) FROM tweets WHERE writer_id = ?", (self.target_user_id,))
        num_tweets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (self.target_user_id,))
        num_following = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (self.target_user_id,))
        num_followers = cursor.fetchone()[0]

        # Display profile info
        tk.Label(self.app.root, text=f"User Profile: {name} (ID: {self.target_user_id})", font=("Arial", 18)).pack(
            pady=10)
        info_text = f"Number of Tweets: {num_tweets}\nFollowing: {num_following}\nFollowers: {num_followers}"
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
        tk.Label(self.app.root, text="Recent Tweets:").pack(pady=5)
        tweets_frame = tk.Frame(self.app.root)
        tweets_frame.pack(pady=5)

        cursor.execute("""
                    SELECT tid, text, tdate, ttime FROM tweets
                    WHERE writer_id = ?
                    ORDER BY tdate DESC, ttime DESC
                    LIMIT 3
                """, (self.target_user_id,))
        tweets = cursor.fetchall()

        if tweets:
            for tid, text, tdate, ttime in tweets:
                display_text = f"{text} (Date: {tdate} {ttime})"
                button = tk.Button(tweets_frame, text=display_text, wraplength=450, justify=tk.LEFT,
                                   command=lambda tid=tid: self.app.show_tweet_detail_screen(self.user_id, tid))
                button.pack(pady=2, fill=tk.X)
        else:
            tk.Label(tweets_frame, text="No tweets to display.").pack()

        # Navigation buttons
        tk.Button(self.app.root, text="Back", command=lambda: self.app.back()).pack(
            pady=5)
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack()

        # Save follow_button reference for later update
        self.follow_button = follow_button

    def follow_user(self):
        """
        Allows the user to follow the target user.
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()
        try:
            cursor.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?)",
                           (self.user_id, self.target_user_id, datetime.date.today().strftime('%Y-%m-%d')))
            self.app.conn.commit()
            messagebox.showinfo("Success", "You are now following this user.")
            self.follow_button.config(text="Unfollow", command=self.unfollow_user)

            # Update the follower count on the user's interface
            self.app.clear_screen()
            self.app.reload()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Failed to follow the user.")

    def unfollow_user(self):
        """
        Allows the user to unfollow the target user.
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
            self.follow_button.config(text="Follow", command=self.follow_user)

            # Update the follower count on the user's interface
            self.app.clear_screen()
            UserTweetsScreen(self.app, self.user_id, self.target_user_id)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to unfollow: {e}")

    def view_tweet(self, tweet_id):
        """
        Allows the user to view details of a specific tweet.
        Inputs:
            tweet_id (int): The ID of the tweet to view.
        Returns:
            None
        """
        self.app.show_tweet_detail_screen(self.user_id, tweet_id)