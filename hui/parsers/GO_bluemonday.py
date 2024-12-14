from ..ParserBase import ParserBase
from ..ParserPayload import ParserPayload
import os

class SANITIZE_HTML(ParserBase):

    def __init__(self) -> None:
        super().__init__("GO_bluemonday")

    def get_results(self):
        self.generate_payloads()
        os.system("cd ./parsers/generators/;go run go_bluemonday.go")
