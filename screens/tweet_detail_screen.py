# screens/tweet_detail_screen.py
import tkinter as tk
from tkinter import messagebox
import datetime
import sqlite3
from .screen import Screen

class TweetDetailScreen(Screen):
    """
    This class mainly displays detailed information about a single, selected tweet.
    """
    def __init__(self, app, user_id, tweet_id):
        """
        The constructor for the TweetDetailScreen class, this constructor initializes and declares all Tkinter objects
        to create a working interface for the user to view a tweet's profile.
        Inputs:
            app (App object): the app whose display we want to change to the login screen
            user_id (int): the id of the current user
            tweet_id (int): the id of the tweet we want to view
        Returns:
            None
        """
        self.app = app
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.build_user_interface()

    def build_user_interface(self):
        """
        An inherited method from the Screen class that is specialized to be able to display the user interface of the
        application. This specific screen is designed to display all the elements of the user interface that is used to
        give the user the tools that they need to interact with and see all of the information that they need from a
        particular tweet.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        cursor = self.app.conn.cursor()

        # Get tweet details
        cursor.execute("""
            SELECT text, tdate, ttime, writer_id FROM tweets WHERE tid = ?
        """, (self.tweet_id,))
        self.tweet = cursor.fetchone()
        if not self.tweet:
            messagebox.showerror("Error", "Tweet not found.")
            self.app.show_search_tweets_screen(self.user_id)
            return
        self.text, self.tdate, self.ttime, self.writer_id = self.tweet

        # Determine if the tweet is a retweet
        cursor.execute("""
            SELECT COUNT(*) FROM retweets WHERE tid = ? AND retweeter_id = ?
        """, (self.tweet_id, self.user_id))
        is_retweet = cursor.fetchone()[0] > 0
        display_type = "Retweet" if is_retweet else "Tweet"

        # Get number of retweets
        cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid = ?", (self.tweet_id,))
        num_retweets = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid = ? AND spam=1", (self.tweet_id,))
        num_retweet_spams = cursor.fetchone()[0]

        # Get number of replies
        cursor.execute("SELECT COUNT(*) FROM tweets WHERE replyto_tid = ?", (self.tweet_id,))
        num_replies = cursor.fetchone()[0]

        # Display tweet details in the specified order
        tk.Label(self.app.root, text="Tweet Details", font=("Arial", 18)).pack(pady=10)

        # Format display as requested
        tweet_info = (
            f"Type: {display_type}\n"
            f"Tweet ID: {self.tweet_id}\n"
            f"Date: {self.tdate}\n"
            f"Time: {self.ttime}\n"
            f"Tweet: {self.text}\n"
            f"Retweets: {num_retweets} (Spams: {num_retweet_spams})\n"
            f"Replies: {num_replies}"
        )
        tk.Label(self.app.root, text=tweet_info, justify=tk.LEFT, wraplength=400).pack(pady=5)

        # Options
        tk.Button(self.app.root, text="Reply to Tweet",
                  command=lambda: self.app.show_reply_tweet_screen(self.user_id, self.tweet_id)).pack(pady=5)
        tk.Button(self.app.root, text="View Writer's Profile", command=self.view_writer_details).pack(pady=5)
        tk.Button(self.app.root, text="Retweet", command=lambda: self.retweet(self.tweet_id)).pack(pady=5)
        tk.Button(self.app.root, text="Back", command=lambda: self.app.back()).pack(pady=5)
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack(pady=5)

    def retweet(self, tweet_id):
        """
        A method that allows the user viewing the tweet to retweet it from their account.
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()
        try:
            # Insert into retweets table including rdate for consistency
            cursor.execute(
                """
                INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    tweet_id,
                    self.user_id,
                    self.writer_id,  # Original writer's ID
                    0,  # Assuming 0 for non-spam
                    datetime.date.today().strftime('%Y-%m-%d')  # rdate
                )
            )
            self.app.conn.commit()
            messagebox.showinfo("Success", "Tweet retweeted successfully.")
            self.app.reload()

        except sqlite3.Error:
            messagebox.showerror("Error", "Failed to retweet as you can only retweet once.")

    def view_writer_details(self):
        """
        Navigates to the writer's profile page.
        Inputs:
            None
        Returns:
            None
        """
        self.app.show_user_profile_screen(self.user_id, self.writer_id)
