# screens/feed_screen.py
import tkinter as tk
from tkinter import messagebox
from .screen import Screen


class FeedScreen(Screen):
    """
    This class mainly displays information that is relevant to the user who wants to just browse the app, such as
    showing the tweets from all the users that they are following
    """

    def __init__(self, app, user_id):
        """
        The constructor for the FeedScreen class, this constructor initializes and declares all Tkinter objects needed
        to create a working interface for the user's feed
        Inputs:
            app (App object): the app whose display we want to change to the login screen
            user_id (int): the id of the user whose feed that we want to display
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
        give the user the tools that they need to view their feed of tweets from the accounts that they follow, and
        provide the necessary functionality that they need to either navigate towards the interface of the tweet that
        they want to view, or to navigate back to the main menu to be able to do other tasks that they want on the app
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        self.current_screen_index = 0
        self.feed_items = []

        # Build the feed interface
        tk.Label(self.app.root, text="Your Feed", font=("Arial", 18)).pack(pady=10)

        # creates a feed frame, a collection of GUI elements on the screen that allows us to view the elements of the
        # feed (by grouping together on a frame, it makes it easier to scroll through the feed elements too)
        self.feed_frame = tk.Frame(self.app.root)
        self.feed_frame.pack(pady=5)

        # creates a frame that allows us to navigate the feed items
        self.nav_frame = tk.Frame(self.app.root)
        self.nav_frame.pack(pady=5)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.show_prev_feed_items)
        self.prev_button.pack(side=tk.LEFT)
        self.more_button = tk.Button(self.nav_frame, text="More", command=self.show_more_feed_items)
        self.more_button.pack(side=tk.LEFT)

        # Buttons to navigate to main menu or logout
        tk.Button(self.app.root, text="Back to Main Menu", command=lambda: self.app.back()).pack(pady=5)
        tk.Button(self.app.root, text="Logout", command=lambda:self.app.logout()).pack(pady=5)

        self.load_feed()

    def load_feed(self):
        """
        The function that loads all the relevant items for the user into the program from the database
        Inputs:
            None
        Returns:
            None
        """
        cursor = self.app.conn.cursor()

        # Get the list of users the current user is following
        cursor.execute("""
            SELECT flwee FROM follows WHERE flwer = ?
        """, (self.user_id,))
        followed_users = [row[0] for row in cursor.fetchall()]

        if not followed_users:
            tk.Label(self.feed_frame, text="You are not following any users yet.", font=("Arial", 14)).pack(pady=10)
            tk.Button(self.feed_frame, text="Search Users to Follow",
                      command=lambda: self.app.show_search_users_screen(self.user_id)).pack(pady=5)
            # when the web page is being loaded for the first time, we must remember to disable the buttons
            self.prev_button.config(state=tk.DISABLED)
            self.more_button.config(state=tk.DISABLED)
            return

        # Fetch tweets from followed users
        cursor.execute("""
            SELECT tid, text, tdate, ttime, writer_id, name, status FROM
            (SELECT t.tid, t.text, t.tdate, t.ttime, t.writer_id, u.name, 'tweeted' AS status
            FROM tweets t
            JOIN users u ON t.writer_id = u.usr
            WHERE EXISTS (SELECT flwee FROM follows WHERE  flwee=t.writer_id AND flwer = ?)
            
            UNION
            
            SELECT rt.tid, t.text, rt.rdate AS tdate, TIME('00:00:00') AS ttime, rt.retweeter_id AS writer_id, u.name,  'retweeted' AS status
            FROM retweets rt
            JOIN tweets t ON rt.tid = t.tid
            JOIN users u ON rt.retweeter_id = u.usr
            WHERE EXISTS (SELECT flwee FROM follows WHERE flwee=rt.retweeter_id AND flwer = ?)
            )
            ORDER BY tdate DESC, ttime desc, tid
        """, (self.user_id, self.user_id))
        self.feed_items = [(tid, text, str(tdate), str(ttime), writer_id, name, status) for
                  tid, text, tdate, ttime, writer_id, name, status in cursor.fetchall()]

        # does the initial loading of the feed items
        self.show_feed_items()

        self.update_button_state()

    def show_feed_items(self):
        """
        This function is solely responsible for displaying all the items that are queried and staged to display in the
        feed_items list
        Inputs:
            None
        Returns:
             None
        """
        # Clear previous feed items
        for widget in self.feed_frame.winfo_children():
            widget.destroy()

        self.start_index = 5 * self.current_screen_index

        # Display the next batch of feed items
        self.end_index = min(self.start_index + 5, len(self.feed_items))

        # loops through all feed items that need to be displayed
        for i in range(self.start_index, self.end_index):

            # extracts all the information from each item tuple
            item = self.feed_items[i]
            tid, text, tdate, ttime, user_id, user_name, status = item
            if status == 'tweeted':
                display_text = f"{user_name} {tid} (Date: {tdate} {ttime}) {status}: {text}"
            else:
                display_text = f"{user_name} {tid} (Date: {tdate}) {status}: {text}"

            # gives the user the option to click on and navigate to the other tweet's interface
            button = tk.Button(self.feed_frame, text=display_text, wraplength=450, justify=tk.LEFT,
                               command=lambda tid=tid: self.view_tweet(tid))
            button.pack(pady=2, fill=tk.X)

    def show_more_feed_items(self):
        """
        Displays feed items on the next page
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index += 1
        self.show_feed_items()
        self.update_button_state()

    def show_prev_feed_items(self):
        """
        Shows the feed items on the previous page
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index -= 1
        self.show_feed_items()
        self.update_button_state()

    def update_button_state(self):
        """
        Ensures that we don't overstep the boundaries of the returned list of items
        Inputs:
            None
        Returns:
             None
        """
        # Update "More" button state
        if (self.current_screen_index + 1) * 5 >= len(self.feed_items):
            self.more_button.config(state=tk.DISABLED)
        else:
            self.more_button.config(state=tk.NORMAL)

        # Update "Previous" button state
        if self.current_screen_index == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

    def view_tweet(self, tweet_id):
        """
        Allows the user to navigate to the tweet's main page.
        """
        self.app.show_tweet_detail_screen(self.user_id, tweet_id)
