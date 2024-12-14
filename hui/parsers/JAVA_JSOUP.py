from ..ParserBase import ParserBase
import os

class SANITIZE_HTML(ParserBase):

    def __init__(self) -> None:
        super().__init__("JAVA_JSOUP")

    def get_results(self):
        self.generate_payloads()
        os.system("java -jar ./parsers/generators/JSOUP/target/java-jsoup-1.0-SNAPSHOT.jar")
