# exceptions.py
class NonexistentDatabaseException(Exception):
    """
    An exception raised when the specified database does not exist.
    """
    def __init__(self, invalid_path, message="Database does not exist in the specified directory"):
        self.invalid_path = invalid_path
        self.message = f"{message}: {self.invalid_path}"
        super().__init__(self.message)


class EmptyStackAccessException(Exception):
    """
    An exception that is raised when the screen stack is accessed while empty
    """

    def __init__(self):
        self.message = "Cannot go back, a previous UI screen does not exist"
        super().__init__(self.message)