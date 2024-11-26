# screens/search_tweets_screen.py
import tkinter as tk
from tkinter import messagebox
import re
from .screen import Screen


class SearchTweetsScreen(Screen):
    """
    This class allows you to create a screen that gives you the ability to search for tweets based on keywords and get
    back all results.
    """

    def __init__(self, app, user_id):
        """
        The constructor for the SearchTweetsScreen class, this constructor initializes and declares all Tkinter objects
        to create a working interface for the user to search through tweets.
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
        give the user the tools that they need to search through all possible tweets.
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()

        self.current_screen_index = 0
        self.tweets = []

        tk.Label(self.app.root, text="Search Tweets", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.app.root, text="Enter Keywords (comma-separated) - case insensitive").pack()
        self.keyword_entry = tk.Entry(self.app.root, width=50)
        self.keyword_entry.pack(pady=5)

        self.keyword_entry.bind("<Return>", lambda event: self.search_tweets())

        tk.Button(self.app.root, text="Search", command=self.search_tweets).pack(pady=5)

        self.tweets_frame = tk.Frame(self.app.root)
        self.tweets_frame.pack(pady=5)

        self.nav_frame = tk.Frame(self.app.root)
        self.nav_frame.pack(pady=5)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.show_prev_tweets)
        self.prev_button.pack(side=tk.LEFT)
        self.prev_button.config(state=tk.DISABLED) # Don't enable until tweets have been loaded
        self.more_button = tk.Button(self.nav_frame, text="More", command=self.show_more_tweets)
        self.more_button.pack(side=tk.LEFT)
        self.more_button.config(state=tk.DISABLED)  # Disabled initially

        tk.Button(self.app.root, text="Back", command=lambda: self.app.back()).pack(pady=5)


    def search_tweets(self):
        """
        This function allows the user to take input from the search, and then query the database to extract all tweets
        that match the search by either keyword in hashtag or by text content through special keywords.
        Inputs:
            None
        Returns:
            None
        """
        raw_input = self.keyword_entry.get()
        if not raw_input.strip():
            messagebox.showwarning("Warning", "Please enter one or more keywords.")
            return
        # Split search string into keywords separated by comma and convert it to lowercase.
        keywords = [keyword.lower().strip() for keyword in raw_input.strip().split(',') if keyword.strip()]

        if  keywords is None or len(keywords) == 0 or  "" in keywords or None in keywords:
            messagebox.showwarning("Warning", "Please enter keyword for search separated by comma.")
            return


        # Check for duplicate values by removing duplicates using set and comparing list length with original list
        if len(keywords) != len(set(keywords)):
            messagebox.showwarning("Warning",
                                   "Please remove duplicate keyword from search. Search keywords are not case sensitive.")
            return

        # seperate out hashtag and non-hashtag keywords and exclude empty strings
        hashtag_search_terms = [x.lower().strip() for x in keywords if x.startswith('#')]

        if '#' in hashtag_search_terms or None in hashtag_search_terms:
            messagebox.showwarning("Warning", "Please enter keyword after hashtag(#).")
            return

        # this regex expression is specifically here to make sure that we can exactly match each word in text with a
        # corresponding term in the search bar. First, the (?i) makes the search case insensitive. Next, the
        # (?<=\s|^|\W) essentially looks what comes before our matched string, where we need to match a whitespace (\s),
        # the start of a string (^), or not a word (\W), while after the matched string must be a whitespace, end of
        # text ($), or a non-word
        non_hashtag_search_terms = ['(?i)(?<=\s|^|\W)' + x + '(?=\s|$|\W)' for x in keywords if
                                    not x.startswith('#')]

        if "" in non_hashtag_search_terms or None in non_hashtag_search_terms:
            messagebox.showwarning("Warning", "Please enter keyword for search separated by comma.")
            return

        # Clear previous results
        for widget in self.tweets_frame.winfo_children():
            widget.destroy()

        self.current_screen_index = 0  # Reset index
        self.tweets = []
        self.prev_button.config(state=tk.DISABLED)
        self.more_button.config(state=tk.DISABLED)

        cursor = self.app.conn.cursor()



        non_hashtag_search_query = None
        # If we have non-hashtag search terms, we will build a query string for it
        if non_hashtag_search_terms:
            search_condition_1 =  ' OR '.join([' regexp_like(LOWER(T.text), ?) ' for e in non_hashtag_search_terms])
            non_hashtag_search_query = '''SELECT T.writer_id, T.tid, T.text, T.tdate, T.ttime FROM tweets T
                               WHERE  ''' + search_condition_1
        hashtag_search_query = None
        # If we have hashtag search terms, then we will build a query string for it too
        if hashtag_search_terms:
            search_condition_2 =  ' OR '.join( ' LOWER(H.term) = ? 'for e in hashtag_search_terms)
            hashtag_search_query = '''SELECT  T.writer_id, T.tid, T.text, T.tdate, T.ttime FROM tweets T
                        JOIN hashtag_mentions H ON H.tid = T.tid
                    WHERE ''' + search_condition_2

        # builds the query string to extract all the data from the database
        full_sql_query = None
        parameters = None
        if non_hashtag_search_query and hashtag_search_query:
            full_sql_query = 'SELECT writer_id, tid, text, tdate, ttime FROM (' + non_hashtag_search_query  + ' UNION ' + hashtag_search_query + ' ) ORDER BY tdate DESC, ttime DESC'
            parameters = non_hashtag_search_terms + hashtag_search_terms
        elif non_hashtag_search_query:
            full_sql_query = non_hashtag_search_query + ' ORDER BY tdate DESC, ttime DESC'
            parameters = non_hashtag_search_terms
        elif hashtag_search_query:
            full_sql_query = hashtag_search_query + ' ORDER BY tdate DESC, ttime DESC'
            parameters = hashtag_search_terms

        cursor.execute(full_sql_query, parameters)
        query_results = cursor.fetchall()

        self.tweets = query_results

        if not self.tweets:
            messagebox.showinfo("No Results", "No tweets found.")
            return

        self.show_tweets()
        self.update_button_state()

    def show_tweets(self):
        """
        This function is solely responsible for displaying all the items that are queried and staged to display in the
        tweets list.
        Inputs:
            None
        Returns:
            None
        """
        # Clear previous tweets
        for widget in self.tweets_frame.winfo_children():
            widget.destroy()

        # Display the next batch of tweets
        self.start_index = 5 * self.current_screen_index
        self.end_index = min(self.start_index + 5, len(self.tweets))
        for i in range(self.start_index, self.end_index):
            tweet = self.tweets[i]
            writer_id, tid, text, tdate, ttime = tweet
            display_text = f"User ID: {writer_id}, TID:{tid} (Date: {tdate} {ttime}) {text}"
            button = tk.Button(self.tweets_frame, text=display_text, wraplength=350, justify=tk.LEFT,
                               command=lambda tid=tid: self.view_tweet(tid))
            button.pack(pady=2, fill=tk.X)

    def show_prev_tweets(self):
        """
        Shows the previous list of tweets
        Inputs:
            None
        Returns:
             None
        """
        self.current_screen_index -= 1
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
        self.current_screen_index += 1
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
        # Enable/disable "More" button based on remaining tweets
        if (self.current_screen_index + 1) * 5 >= len(self.tweets):
            self.more_button.config(state=tk.DISABLED)
        else:
            self.more_button.config(state=tk.NORMAL)

        # Enable/disable "Previous" button based on remaining tweets
        if self.current_screen_index == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

    def view_tweet(self, tweet_id):
        """
        Allows the user to navigate to the tweet's main page.
        Inputs:
            tweet_id (int): The ID of the tweet to view.
        Returns:
            None
        """
        self.app.show_tweet_detail_screen(self.user_id, tweet_id)
