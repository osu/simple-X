# main.py
import tkinter as tk
from tkinter import messagebox

from db import connect_db
from screen_stack import ScreenStack

# Import screen classes
from screens.screen import Screen
from screens.login_screen import LoginScreen
from screens.signup_screen import SignupScreen
from screens.main_menu_screen import MainMenuScreen
from screens.feed_screen import FeedScreen
from screens.search_tweets_screen import SearchTweetsScreen
from screens.search_users_screen import SearchUsersScreen
from screens.user_profile_screen import UserProfileScreen
from screens.user_tweets_screen import UserTweetsScreen
from screens.tweet_detail_screen import TweetDetailScreen
from screens.compose_tweet_screen import ComposeTweetScreen
from screens.reply_tweet_screen import ReplyTweetScreen
from screens.list_followers_screen import ListFollowersScreen


class App:
    """
    For our application, we have created a class that can work with Tkinter's basic Tkinter class to add more
    functionality to it for the purpose for our application.
    """

    def __init__(self, root):
        """
        This is the constructor for the App class.
        Inputs:
            root (Tk object): a Tk object (a Tkinter widget object that gives us the basic functionality for Tkinter), 
            we take this object (which is initially declared outside the definition of this class, and is a part of the
            main program), and access its functionality from the interface provided by this class.
        Returns:
            None
        """
        self.root = root
        self.root.title("Barebones-Twitter")
        self.root.geometry("500x500")
        self.conn = connect_db()
        self.screen_stack = ScreenStack()
        self.show_login_screen()

    # Screen Switching Functions
    def show_login_screen(self):
        """
        The entry point of the program, this function is called in the constructor, and it starts off the application by
        calling an instance of the LoginScreen class.
        Inputs:
            None (this method acts on attributes of the class, which it already has access through self referencing)
        Returns:
            None
        """
        self.login = LoginScreen(self)
        self.screen_stack.push(self.login)

    def show_signup_screen(self):
        """
        Is called by the LoginScreen class whenever we want to allow the user to create a new account in case we don't
        have one already.
        Inputs:
            None (this method acts on attributes of the class, which it already has access through self referencing)
        Returns:
            None
        """
        self.signup = SignupScreen(self)
        self.screen_stack.push(self.signup)

    def show_feed_screen(self, user_id):
        """
        A function that creates an instance of the FeedScreen class, and for this, we will pull information about the
        tweets that the user is following has posted.
        Inputs:
            user_id (int): the user_id is a primary key for the users table in our database, therefore when we want to
            load the feed for a user, we need to know their user_id.
        Returns:
            None
        """
        self.feed = FeedScreen(self, user_id)
        self.screen_stack.push(self.feed)

    def show_main_menu(self, user_id):
        """
        A function that creates an instance of the MainMenuScreen class, where the user is given options to navigate to
        any other screen that they desire within the application.
        Inputs:
            user_id (int): the user_id is a primary key for the users table in our database, therefore when we want to
            load the main menu for a user and allow them to navigate to other screens from the main menu, it is helpful
            to know their user_id.
        Returns:
            None
        """
        self.main_menu = MainMenuScreen(self, user_id)
        self.screen_stack.push(self.main_menu)

    def show_search_users_screen(self, user_id):
        """
        A function that creates an instance of the SearchUsersScreen class, where the user is given options to search
        and navigate to the account pages of other accounts. The user will search through keywords, where the system
        will try to output all names that contain the keyword.
        Inputs:
            user_id (int): the user_id is a primary key for the users table in our database, even though it is not
            necessary for the functionality of the search screen itself, is still useful when we want to navigate to
            other pages from the search screen.
        Returns:
            None
        """
        self.search_user = SearchUsersScreen(self, user_id)
        self.screen_stack.push(self.search_user)

    def show_tweet_detail_screen(self, user_id, tweet_id):
        """
        A function that creates an instance of the TweetDetailScreen class, where the user is given options to look at
        the details of a given tweet.
        Inputs:
            user_id (int): the user_id is a primary key for the users table in our database, even though it is not
            necessary for the functionality of the tweet details screen itself, it is useful when we want to navigate
            to other pages from the tweet details screen.
            tweet_id (int): a primary key for the tweets table, this attribute allows us to uniquely identify the tweet
            that we are looking at and extract all the details from the tweet to display to the user.
        Returns:
            None
        """
        self.tweet_detail = TweetDetailScreen(self, user_id, tweet_id)
        self.screen_stack.push(self.tweet_detail)

    def show_reply_tweet_screen(self, user_id, tweet_id):
        """
        A function that creates an instance of the ReplyTweetScreen class, where the user is given the option to reply
        to a tweet that has already been created. This is different from the ComposeTweetScreen, where the tweet that is
        created in that screen has no value in its replyto_tid field, which means that that tweet would not be replying
        to anybody.
        Inputs:
            user_id (int): the user_id is a primary key for the users table in our database, the writer of this reply
            tweet.
            tweet_id (int): a primary key for the tweets table, this tweet_id is for the tweet that we are replying to,
            not the id for the tweet that we are creating for the reply.
        Returns:
            None
        """
        self.reply_tweet = ReplyTweetScreen(self, user_id, tweet_id)
        self.screen_stack.push(self.reply_tweet)

    def show_user_profile_screen(self, user_id, target_user_id):
        """
        A function that creates an instance of the UserProfileScreen class, where the profile of a selected user has
        been selected, and we can then view all details of it.
        Inputs:
            user_id (int): the user_id of the user that is logged in.
            target_user_id (int): the user_id of the user whose profile that we are looking at.
        Returns:
            None
        """
        self.user_profile = UserProfileScreen(self, user_id, target_user_id)
        self.screen_stack.push(self.user_profile)

    def show_user_tweets_screen(self, user_id, target_user_id):
        """
        A function that creates an instance of the UserTweetsScreen class, where all the tweets of a selected user can
        be viewed. We can also interact with this page to access the individual details of each of the listed tweets.
        Inputs:
            user_id (int): the user_id of the user that is logged in.
            target_user_id (int): the user_id of the user whose tweets that we are looking at.
        Returns:
            None
        """
        self.user_tweets = UserTweetsScreen(self, user_id, target_user_id)
        self.screen_stack.push(self.user_tweets)

    def show_search_tweets_screen(self, user_id):
        """
        A function that creates an instance of the SearchTweetsScreen class, where we get to search through all the
        tweets in the database through either the tags that the tweets mention with the hashtag feature, or through
        the words that are in the content/text of the tweet.
        Inputs:
            user_id (int): the user_id of the user that is logged in.
        Returns:
            None
        """
        self.search_tweets = SearchTweetsScreen(self, user_id)
        self.screen_stack.push(self.search_tweets)

    def show_compose_tweet_screen(self, user_id):
        """
        A function that creates an instance of the ComposeTweetScreen class, where the user gets to write a tweet.
        Unlike the show_reply_tweet_screen, this tweet written has no value in its replyto_tid field, since this is not
        a reply to anyone.
        Inputs:
            user_id (int): the user_id of the user that is logged in and is the writer of the tweet that is currently
            being written.
        Returns:
            None
        """
        self.compose_tweet = ComposeTweetScreen(self, user_id)
        self.screen_stack.push(self.compose_tweet)

    def show_list_followers_screen(self, user_id):
        """
        This function creates an instance of the ListFollowersScreen class, which allows the user to see a list of all
        their followers, and also click on their profiles to get a more detailed view of their account information (the
        display of the user information will be taken care of in another screen).
        Inputs:
            user_id (int): the user_id of the user who wants to see all of their followers.
        Returns:
            None
        """
        self.list_follower = ListFollowersScreen(self, user_id)
        self.screen_stack.push(self.list_follower)

    # Helper to clear screen
    def clear_screen(self):
        """
        Clears all widgets from the root window. This function is useful when switching from one interface to another.
        Inputs:
            None
        Returns:
            None
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def back(self):
        """
        Allows the user to go to the page that they were previously on (stored in the screen stack)
        Inputs:
            None
        Returns:
            None
        """
        self.screen_stack.pop()
        self.screen_stack.peek().build_user_interface()

    def back_to_main_menu(self):
        """
        Takes the user back to the main menu
        Inputs:
            None
        Returns:
            None
        """
        while len(self.screen_stack) > 2:
            self.screen_stack.pop()

        if type(self.screen_stack.peek()) == MainMenuScreen:
            self.screen_stack.peek().build_user_interface()
        else:
            messagebox.showwarning("Error",
                                   "Could not locate main menu, logging out")
            self.logout()

    def logout(self):
        """
        Clears all objects on the screen stack, then goes back to the login page
        Inputs:
            None
        Returns:
            None
        """
        self.screen_stack.clear()
        self.show_login_screen()
        # changes the title back to the
        self.root.title("Barebones-Twitter")

    def reload(self):
        """
        Reloads the current screen by rebuilding the current user interface
        Inputs:
            None
        Returns:
            None
        """
        self.screen_stack.peek().build_user_interface()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
