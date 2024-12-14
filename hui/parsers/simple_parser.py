from ..ParserBase import ParserBase
import os

# Cheat for include basic checks into identify
# TODO: replace
class SANITIZE_HTML(ParserBase):

    def __init__(self) -> None:
        super().__init__("SIMPLE_PARSER")
    
    def get_results(self):
        self.generate_payloads()