from ..ParserBase import ParserBase
import os

# Python LXML_HTML parser
class SANITIZE_HTML(ParserBase):

    def __init__(self) -> None:
        super().__init__("PYTHON_LXML_HTML")
    
    def get_results(self):
        self.generate_payloads()
        os.system("python ./parsers/generators/python-lxml-html.py")
        