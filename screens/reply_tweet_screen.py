# screens/reply_tweet_screen.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import datetime
from .screen import Screen

class ReplyTweetScreen(Screen):
    """
    A class containing the necessary interface to not only allow the user to input their own tweet, but also have this
    tweet be written in response to another tweet.
    """
    def __init__(self, app, user_id, tweet_id):
        """
        The constructor for the ReplyTweetScreen class, this constructor initializes and declares all Tkinter objects to
        create a working interface for the user to create their own reply.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user who wants to write a reply.
            tweet_id (int): The ID of the tweet being replied to.
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
        give the user the tools that they need to submit their reply to another tweet.
        Inputs:
            None
        Returns:
            None
        """

        self.app.clear_screen()

        tk.Label(self.app.root, text="Compose Reply", font=("Arial", 18)).pack(pady=10)

        self.reply_entry = tk.Text(self.app.root, height=5, width=40)
        self.reply_entry.pack(pady=10)

        tk.Button(self.app.root, text="Post Reply", command=self.post_reply).pack(pady=5)
        tk.Button(self.app.root, text="Back",
                  command=lambda: self.app.back()).pack(pady=5)

        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack()

    def post_reply(self):
        """
        The function that is called when the user presses the button to submit a reply, inserting a new reply into the
        tweets database.
        Inputs:
            None
        Returns:
            None
        """
        reply_text = self.reply_entry.get("1.0", tk.END).strip()
        if not reply_text:
            messagebox.showwarning("Warning", "Reply cannot be empty.")
            return

        # Extract hashtags with the # symbol included
        # uses regular expressions to find and extract all text that is within each hashtag
        # the hashtag sign at the front matches with a hashtag in the text, the \w matches a character that is a part of
        # the term, the + allows you to continue matching until you hit another pound or whitespace
        hashtags = set(re.findall(r'#\w+', reply_text))
        # set allows us to get rid of all duplicates
        unique_hashtags = set(map(str.lower, hashtags))  # Case-insensitive comparison
        # Ensure no standalone '#' is present

        if '#' in reply_text.split():
            messagebox.showerror("Invalid Hashtag", "Hashtags cannot be a single '#' character. Please enter a valid hashtag (e.g. #example)")
            return
            
        if len(hashtags) != len(unique_hashtags):
            messagebox.showerror("Duplicate Hashtags", "You cannot enter the same hashtag multiple times.")
            return

        # Proceed if no duplicates
        hashtags = unique_hashtags  # Use the unique set for database insertion

        cursor = self.app.conn.cursor()
        try:
            # Insert reply as a new tweet with replyto_tid field
            cursor.execute("SELECT MAX(tid) FROM tweets")
            result = cursor.fetchone()
            new_tid = str(int(result[0]) + 1) if result[0] else '1'
            tdate = datetime.date.today().strftime('%Y-%m-%d')
            ttime = datetime.datetime.now().strftime('%H:%M:%S')

            cursor.execute("""
                INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (new_tid, self.user_id, reply_text, tdate, ttime, self.tweet_id))
            
            # Insert each unique hashtag
            for term in hashtags:
                cursor.execute("""
                    INSERT INTO hashtag_mentions (tid, term) 
                    VALUES (?, ?)
                """, (new_tid, term.lower()))  # Ensure hashtags are stored in lowercase

            self.app.conn.commit()
            messagebox.showinfo("Success", "Reply posted successfully.")
            self.app.back()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to post reply: {e}")
