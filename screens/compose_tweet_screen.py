# screens/compose_tweet_screen.py

import tkinter as tk
from tkinter import messagebox
import re
import datetime
import sqlite3  # Ensure sqlite3 is imported

from .screen import Screen

class ComposeTweetScreen(Screen):
    """
    A class containing the necessary interface to allow the user to input their own tweet and send it from their account.
    """
    def __init__(self, app, user_id):
        """
        The constructor for the ComposeTweetScreen class, this constructor initializes and declares all Tkinter objects
        to create a working interface for the user to create their own tweet.
        Inputs:
            app (App object): The app instance.
            user_id (int): The ID of the current user who wants to write a tweet.
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
        give the user the tools that they need to write their own tweet
        Inputs:
            None
        Returns:
            None
        """
        # clears the previous screen's widgets, since the way that tkinter would work is that the next screen's widgets
        # would be pasted right under the previous screen's widgets
        self.app.clear_screen()

        # creates a tkinter label object that allows you to display a compose tweet label
        tk.Label(self.app.root, text="Compose Tweet", font=("Arial", 18)).pack(pady=10)

        # creates a text field that allows users to input their tweet
        self.tweet_entry = tk.Text(self.app.root, height=5, width=40)
        self.tweet_entry.pack(pady=10)

        # gives the user navigation and posting buttons
        tk.Button(self.app.root, text="Post Tweet", command=self.submit_tweet).pack(pady=5)
        tk.Button(self.app.root, text="Back", command=lambda: self.app.back()).pack()
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back_to_main_menu()).pack()

    def submit_tweet(self):
        """
        The function that is called when the user presses the button to submit a tweet, inserting a new tweet into the
        database.
        Inputs:
            None
        Returns:
            None
        """
        # this function extracts the inputted test from the text field
        text = self.tweet_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Tweet cannot be empty")
            return

        # Extract hashtags with the # symbol included
        # uses regular expressions to find and extract all text that is within each hashtag
        # the hashtag sign at the front matches with a hashtag in the text, the \w matches a character that is a part of
        # the term, the + allows you to continue matching until you hit another pound or whitespace
        hashtags = re.findall(r'#\w+', text)
        # set allows us to get rid of all duplicates
        unique_hashtags = set(map(str.lower, hashtags))  # Case-insensitive comparison
        # Ensure no standalone '#' is present

        if '#' in text.split():
            messagebox.showerror("Invalid Hashtag", "Hashtags cannot be a single '#' character. Please enter a valid hashtag (e.g. #example)")
            return
            
        if len(hashtags) != len(unique_hashtags):
            messagebox.showerror("Duplicate Hashtags", "You cannot enter the same hashtag multiple times.")
            return

        # Proceed if no duplicates
        hashtags = unique_hashtags  # Use the unique set for database insertion

        cursor = self.app.conn.cursor()
        try:
            # we want a unique tid for the tweets, so clearly we would do so by selecting a tid that is 1 more than the
            # maximum
            cursor.execute("SELECT MAX(tid) FROM tweets")
            result = cursor.fetchone()
            new_tid = int(result[0]) + 1 if result[0] else 1

            # finds the current date and time
            tdate = datetime.date.today().strftime('%Y-%m-%d')
            ttime = datetime.datetime.now().strftime('%H:%M:%S')

            cursor.execute("""
                INSERT INTO tweets (tid, writer_id, text, tdate, ttime) 
                VALUES (?, ?, ?, ?, ?)
            """, (new_tid, self.user_id, text, tdate, ttime))

            # Insert each unique hashtag
            for term in hashtags:
                cursor.execute("""
                    INSERT INTO hashtag_mentions (tid, term) 
                    VALUES (?, ?)
                """, (new_tid, term.lower()))  # Ensure hashtags are stored in lowercase

            self.app.conn.commit()
            messagebox.showinfo("Tweet Posted", "Your tweet has been posted successfully.")
            self.app.back()
        except sqlite3.IntegrityError as e:
            # Handle specific integrity errors if any
            messagebox.showerror("Database Error", "An error occurred while posting your tweet. Please try again.")
        except sqlite3.Error as e:
            # Handle other SQLite errors
            messagebox.showerror("Database Error", f"An unexpected error occurred: {e}")
