from .ALLOWED_TAGS import *
from string import Template
import json
import os
import importlib.resources
from importlib.resources import files


class Identifier:
    def __init__(self, handler) -> None:
        """
        :param handler: handler function that must return text with an HTML response.
            Example of a handler function:
                lambda payload: requests.get(f"http://localhost:3000?payload={payload}").text
        :return: returns nothing
        """
        self.handler = handler
        self.ALLOWED_TAGS = {
            "html": [],
            "svg": [],
            "math": [],
        }
        self.TEMPLATE_VARS = dict({
            'text': 'govnoed',
            'href':'https://github.com',
            'attribute_prefix': 'data'
        })

        self.ALLOWED_TAGS_CHECKED=False

    def check_allowed_tags(self):
        self.ALLOWED_TAGS_CHECKED = True
        self.check_html_namespace()
        self.check_svg_namespace()
        self.check_math_namespace()
        return self.ALLOWED_TAGS

    def call_handler(self, template_payload: str):
       payload = Template(template_payload).safe_substitute(self.TEMPLATE_VARS)
       return self.handler(payload)

    def check_html_namespace(self):
        arr = []
        for tag in html_tags:
            arr.append([f'<{tag}>$text</{tag}>', tag])
        
        for tag in html_table_tags:
            arr.append([f'<table><{tag}>$text</{tag}></table>', tag])

        for tag_sub in arr:
            res = self.call_handler(tag_sub[0])
            if f'<{tag_sub[1]}' in res:
                self.ALLOWED_TAGS["html"].append(tag_sub[1])
        pass

    def check_svg_namespace(self):
        tag_arr = []
        for tag in svg_tags:
            tag_arr.append([f'<svg><{tag}>$text</{tag}></svg>', tag])

        for tag_sub in tag_arr:
            res = self.call_handler(tag_sub[0])
            if f'<{tag_sub[1]}>' in res:
                self.ALLOWED_TAGS["svg"].append(tag_sub[1])
        pass

    def check_math_namespace(self):
        tag_arr = []
        for tag in mathml_tags:
            tag_arr.append([f'<math><{tag}>$text</{tag}></math>', tag])

        for tag_sub in tag_arr:
            res = self.call_handler(tag_sub[0])
            if f'<{tag_sub[1]}>' in res:
                self.ALLOWED_TAGS["math"].append(tag_sub[1])
        pass

    def identify(self):
        if len(self.ALLOWED_TAGS) == 0:
            self.check_allowed_tags()
        with importlib.resources.open_text('hui', 'generated_payloads.json') as f:
            arr = json.load(f)
        res = [self.call_handler(tag) for tag in arr]
        json_files = [f for f in importlib.resources.files('hui.results_parsers').iterdir() if f.name.endswith('.json')]

        result = []

        for json_file in json_files:
            with open(json_file) as f:
                data = json.load(f)

            # Count the number of matches in the JSON file
            matches = sum([1 for i in range(len(res)) if res[i].strip() == Template(data[i]).substitute(self.TEMPLATE_VARS).strip()])
            result.append([matches/len(data),matches,json_file.name.split('.')[0]])

        result = sorted(result,reverse=True)
        return result

    def check_namespace_supported(self, namespace):
        if not self.ALLOWED_TAGS_CHECKED:
            self.check_allowed_tags()
        if not(namespace in self.ALLOWED_TAGS):
            raise Exception('Invalid namespace name')
        return len(self.ALLOWED_TAGS) > 0
    