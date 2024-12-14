class ParserPayload:
    """
    Represents a payload for parsing with additional metadata and methods for validation.

    Attributes:
        payload (str): The actual payload to be parsed.
        expected_output (str, optional): The expected output of the parsing process. Defaults to None.
        version (str, optional): The version of the parser or the payload. Defaults to None.
        sanitizer (str, optional): The sanitizer to be used for the payload. Defaults to None.
        parametrs (str, optional): Parameters for the parsing process. Defaults to None.
        tags (list): Tags associated with the payload.

    Methods:
        check(output): Checks if the output matches the expected output, considering whitespace.
        remove_whitespace(string): Removes whitespace from a given string.
    """

    def __init__(self, payload: str, tags, expected_output: str = None, version: str = None, sanitizer: str = None, parametrs: str = None) -> None:
        self.payload = payload
        self.expected_output = expected_output
        self.version = version
        self.sanitizer = sanitizer
        self.parametrs = parametrs
        self.tags = tags

    def check(self, output):
        """
        Checks if the output matches the expected output, considering whitespace.

        Args:
            output (str): The output to be checked against the expected output.

        Returns:
            bool: True if the output matches the expected output, False otherwise.
        """
        if output in self.expected_output:
            return True
        if self.remove_whitespace(output) in self.remove_whitespace(self.expected_output):
            return True
        return False

    
    def remove_whitespace(self, string):
        """
        Removes whitespace from a given string.

        Args:
            string (str): The string from which to remove whitespace.

        Returns:
            str: The string with all whitespace removed.
        """
        return "".join(string.split())