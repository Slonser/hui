from .ParserPayload import ParserPayload
import json
import os

class ParserBase:
    """
    A class to handle parsing of HTML content with various checks for incorrect parsing states.
    
    Attributes:
        parser_name (str): The name of the parser.
        checks (list): A list of ParserPayload objects that define parsing checks.
    """
    
    def __init__(self, parser_name: str, attribute_prefix='data-') -> None:
        """
        Initializes the ParserBase with a parser name and an optional attribute prefix.

        Args:
            parser_name (str): The name of the parser.
            attribute_prefix (str): The prefix for attributes (default is 'data-').
        """
        self.parser_name = parser_name
        self.checks = []

        # Some HTML parser don't properly resolve raw text tags
        incorrect_parsing_state_tags = ['xmp','textarea','noscript','noembed','style','plaintext']
        for tag in incorrect_parsing_state_tags:
            self.add(
                ParserPayload(f'<{tag}><a href="https://github.com/Slonser/hui/</{tag}>"></a></{tag}>',
                              [tag,'a'],
                              expected_output=f'<{tag}>&lt;a href="https://github.com/Slonser/hui/</{tag}>"&gt;')
            )

        # Some HTML parsers incorrectly handle select tag
        # Browsers will remove <img/> tag, They - don't do this
        self.add(
            ParserPayload('<select><h1></h1></select>',
                          ['select','h1'],
                          expected_output="<select></select>")
        )
        
        # Some HTML parsers don't use flattening with headers tags
        for i in range(1,6):
            self.add(
                ParserPayload(f'<h{i}><h{i+1}>$text</h{i+1}></h{i}>',
                              [f'h{i}',f'h{i+1}'],
                              expected_output=f"<h{i}></h{i}><h{i+1}>$text</h{i+1}>")
            )

        # Some HTML parsers don't resolve nested forms
        self.add(
            ParserPayload('<form><form>$text</form></form>',
                          ['form'],
                          expected_output=f"<form>$text</form>")
        )

        # Some HTML parser don't resolve nested tables
        self.add(
            ParserPayload('<table><table>$text</table></table>',
                          ['table'],
                          expected_output=f"<table></table>$text<table></table>")
        )

        # Some parser don't resolve nested table elemenents
        table_nested_tags = ['caption','td','tr','col']
        for tag in table_nested_tags:
            self.add(
                ParserPayload(f'<table><{tag}><{tag}>$text</{tag}></{tag}></{tag}>',
                              ['table',tag],
                              expected_output=f"<table><{tag}></{tag}><{tag}>$text</{tag}></table>")
            )

        # Some HTML parsers don't implement "in row" insertion mode correctly
        row_insertion_mode = ['th','td','tfoot','thead','tbody','tr']
        for tag in row_insertion_mode:
            self.add(
                ParserPayload(f'<{tag}>$text</{tag}>',
                              [tag],
                              expected_output='$text')
            )
        # Python HTML parsers incorrectly handle lower on html attribute names
        # By default in browsers, only ascii chars would be lowercased 
        # In python \u212a -> 0x6b
        self.add(
            ParserPayload('<a $attribute_prefix-\u212a="1" href="$href">$text</a>',
                          ['a'],
                          expected_output=f'<a href="$href" data-K="1">$text</a>')
        )

        #Some parsers incorrectrly parse self closing tags
        self_closing_tags = ['wbr','hr']
        for tag in self_closing_tags:
            self.add(
                ParserPayload(f'<{tag}>$text</{tag}>',
                              [tag],
                              expected_output=f'<{tag}>$text')
            )

    def add(self, payload):
        """
        Adds a ParserPayload to the checks list.

        Args:
            payload (ParserPayload): The payload to be added to the checks.
        """
        self.checks.append(payload)
    
    def add_all(self, arr):
        """
        Adds multiple ParserPayloads to the checks list.

        Args:
            arr (list): A list of ParserPayload objects to be added.
        """
        for x in arr:
            self.add(x)
    
    def generate_payloads(self):
        """
        Generates payloads and saves them to a JSON file if it does not already exist.
        """
        if os.path.exists("./generated_payloads.json"):
            return
        
        tag_arr = []
        for tag in self.checks:
            tag_arr.append(tag.payload)
        
        return json.dump(tag_arr, open('./generated_payloads.json',"w"))

    def get_results(self):
        """
        Placeholder method for getting results.
        """
        pass