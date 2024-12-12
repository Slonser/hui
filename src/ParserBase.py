from ParserPayload import ParserPayload
import json
import os

class ParserBase:
    def __init__(self, parser_name: str, attribute_prefix='data-') -> None:
        self.parser_name = parser_name
        self.checks = []

        # Some HTML parser don't properly resolve raw text tags
        incorrect_parsing_state_tags = ['xmp','textarea','noscript','noembed','style','plaintext']
        for tag in incorrect_parsing_state_tags:
            self.add(
                ParserPayload(f'<{tag}><a href="</{tag}>"></a></{tag}>',[tag])
            )

        # Some HTML parsers incorrectly handle select tag
        # Browsers will remove <img/> tag, They - don't do this
        self.add(
            ParserPayload('<select><img/></select>',['select','img'])
        )
        
        # Some HTML parsers don't use flattening with headers tags
        for i in range(1,6):
            self.add(
                ParserPayload(f'<h{i}><h{i+1}>$text</h{i+1}></h{i}>',[f'h{i}',f'h{i+1}'])
            )

        # Some HTML parsers don't resolve nested forms
        self.add(
            ParserPayload('<form><form>$text</form></form>',['form'])
        )

        # Some HTML parser don't resolve nested tables
        self.add(
            ParserPayload('<table><table>$text</table></table>',['table'])
        )

        # Some parser don't resolve nested table elemenents
        table_nested_tags = ['caption','td','tr','col']
        for tag in table_nested_tags:
            self.add(
                ParserPayload(f'<table><{tag}><{tag}>$text</{tag}></{tag}></{tag}>',['table',tag])
            )

        # Some HTML parsers don't implement "in row" insertion mode correctly
        row_insertion_mode = ['th','td','tfoot','thead','tbody','tr']
        for tag in row_insertion_mode:
            self.add(
                ParserPayload(f'<{tag}>$text</{tag}>',[tag])
            )
        # Python HTML parsers incorrectly handle lower on html attribute names
        # By default in browsers, only ascii chars would be lowercased 
        # In python \u212a -> 0x6b
        self.add(
            ParserPayload('<a $attribute_prefix-\u212a href="$href">$text</a>',['a'])
        )

    def add(self, payload):
        self.checks.append(payload)
    
    def add_all(self, arr):
        for x in arr:
            self.add(x)
    
    def generate_payloads(self):
        if os.path.exists("./generated_payloads.json"):
            return
        
        tag_arr = []
        for tag in self.checks:
            tag_arr.append(tag.payload)
        
        return json.dump(tag_arr, open('./generated_payloads.json',"w"))

    def get_results():
        pass