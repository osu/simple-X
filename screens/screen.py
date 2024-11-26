import tkinter as tk

class Screen:
    """
    The generic screen class, with no really useful attributes on its own. It's main goal is to act as a parent class to
    other screen classes, allowing it to unify the two common attributes between them. This is most useful with the
    screen stack, where we can call the build_user_interface method of any child class of the Screen.
    """
    def __init__(self, app):
        """
        The generic constructor of the Screen class.
        Inputs:
            app (App object): The app instance.
        Returns:
            None
        """
        self.app = app
        self.build_user_interface()
        print(self.app.screen_stack)

    def build_user_interface(self):
        """
        A parent class to the build user interface of other classes, here it does nothing much
        Inputs:
            None
        Returns:
            None
        """
        self.app.clear_screen()
