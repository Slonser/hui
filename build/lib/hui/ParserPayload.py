class ParserPayload:
    def __init__(self, payload: str, tags, expected_output: str = None, version: str = None, sanitizer: str = None, parametrs: str = None) -> None:
        self.payload = payload
        self.expected_output = expected_output
        self.version = version
        self.sanitizer = sanitizer
        self.parametrs = parametrs
        self.tags = tags

    def check(self, output):
        if output in self.expected_output:
            return True
        if self.remove_whitespace(output) in self.remove_whitespace(self.expected_output):
            return True
        return False

    
    def remove_whitespace(string):
        return "".join(string.split())