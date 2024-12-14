from ..ParserBase import ParserBase
import os

class SANITIZE_HTML(ParserBase):

    def __init__(self) -> None:
        super().__init__("JS_SANITIZE_HTML")

    def get_results(self):
        self.generate_payloads()
        os.system("node ./parsers/generators/js_sanitize-html.js")
