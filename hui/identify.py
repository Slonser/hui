from .ALLOWED_TAGS import *
from .ALLOWED_ATTRS import *
from string import Template
import json
import os
import importlib.resources
from importlib.resources import files
from .parsers.simple_parser import SANITIZE_HTML
import logging
from .CustomParser import CustomParser

class Identifier:
    def __init__(self, handler, buffer_enabled=False, buffer_delimeter="<div>TEXTTEXT</div>", buffer_limit=32, template_vars=None, debug_mode=False) -> None:
        """
        Initializes the Identifier class with a handler function and optional parameters for buffer management, template variables, and logging.

        :param handler: handler function that must return text with an HTML response.
            Example of a handler function:
                lambda payload: requests.get(f"http://localhost:3000?payload={payload}").text
        :param buffer_enabled: Boolean indicating whether to enable buffering of payloads before sending to the handler.
        :param buffer_delimeter: String used to delimit payloads in the buffer.
        :param buffer_limit: Integer specifying the maximum number of payloads to buffer before sending to the handler.
        :param template_vars: Optional dictionary of template variables to use for substitution in payloads.
        :param debug_mode: Boolean indicating whether to enable debug logging.
        :return: returns nothing
        """
        self.handler = handler
        self.ALLOWED_TAGS = {
            "html": [],
            "svg": [],
            "math": [],
        }
        self.TEMPLATE_VARS = template_vars if template_vars is not None else {
            'text': 'govnoed',
            'href': 'https://github.com',
            'attribute_prefix': 'data'
        }

        self.ALLOWED_TAGS_CHECKED = False
        self.DEFAULT_SANITIZER = SANITIZE_HTML()

        self.BUFFER = ""
        self.BUFFER_LIMIT = buffer_limit
        self.BUFFER_ENABLED = buffer_enabled
        self.BUFFER_DELIMETER = buffer_delimeter
        
        self.INCORRECT_PARSED = []
        
        self.DEPTH_LIMITS = ()

        self.ATTRIBUTES = {
            "custom_attribute" : None, # is custom attributes allowed
            "event_attributes_blocked": None, # is event attributes directly blocked
            "data_attributes": None, # is data attributes allowed
            "attrs_allowed":{
                "global":[], # global attributes
                "events":[] # events attributes
            }
        }

        # Configure logging based on debug_mode
        if debug_mode:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__name__)
        self.parser = CustomParser()

    def check_allowed_tags(self) -> dict:
        """
        Check and validate allowed HTML, SVG, and MathML tags.

        :return: A dictionary of allowed tags.
        """
        self.logger.debug("Checking allowed tags...")
        self.ALLOWED_TAGS_CHECKED = True
        self.check_html_namespace()
        self.check_namespace("math")
        self.check_namespace("svg")

        self.logger.debug("Allowed tags checked: %s", self.ALLOWED_TAGS)
        return self.ALLOWED_TAGS

    def call_handler(self, template_payloads: list[str]) -> list[str]:
        """
        Call the handler function with the provided template payloads.

        :param template_payloads: List of template strings to process.
        :return: List of processed results from the handler.
        """
        self.logger.debug("Calling handler with payloads: %s", template_payloads)
        for i in range(len(template_payloads)):
            template_payloads[i] = Template(template_payloads[i]).safe_substitute(self.TEMPLATE_VARS)

        if self.BUFFER_ENABLED:
            res = []
            buffer = []
            for payload in template_payloads:
                buffer.append(payload)
                if len(buffer) >= self.BUFFER_LIMIT:
                    res.extend(self.handler(self.BUFFER_DELIMETER.join(buffer)).split(self.BUFFER_DELIMETER))
                    buffer = []
            if buffer:
                res.extend(self.handler(self.BUFFER_DELIMETER.join(buffer)).split(self.BUFFER_DELIMETER))
            self.logger.debug("Handler results: %s", res)
            return res

        res = [self.handler(payload) for payload in template_payloads]
        self.logger.debug("Handler results: %s", res)
        return res

    def check_html_namespace(self) -> None:
        """
        Check and validate allowed HTML tags.

        :return: None
        """
        self.logger.debug("Checking HTML namespace...")
        arr = []
        for tag in html_tags:
            arr.append([f'<{tag}>$text</{tag}>', tag])

        for tag in html_table_tags:
            arr.append([f'<table><{tag}>$text</{tag}></table>', tag])

        handler_results = self.call_handler([x[0] for x in arr])
        for i in range(len(handler_results)):
            res = handler_results[i]
            if f'<{arr[i][1]}' in res:
                self.ALLOWED_TAGS["html"].append(arr[i][1])

        self.logger.debug("Allowed HTML tags: %s", self.ALLOWED_TAGS["html"])

    def check_namespace(self, namespace: str) -> None:
        """
        Check and validate tags in the specified namespace (math or svg).

        :param namespace: The namespace to check (math or svg).
        :raises Exception: If the namespace is not supported.
        :return: None
        """
        self.logger.debug("Checking namespace: %s", namespace)
        if namespace not in self.ALLOWED_TAGS:
            raise Exception(f'{namespace} namespace is not supported')

        tag_arr = []
        namespace_tags = []
        if namespace == "math":
            namespace_tags = mathml_tags
        elif namespace == "svg":
            namespace_tags = svg_tags

        for tag in namespace_tags:
            tag_arr.append([f'<{namespace}><{tag}>$text</{tag}></{namespace}>', tag])

        handler_results = self.call_handler([x[0] for x in tag_arr])

        for i in range(len(handler_results)):
            res = handler_results[i]
            if f'<{tag_arr[i][1]}' in res:
                self.ALLOWED_TAGS[namespace].append(tag_arr[i][1])

        self.logger.debug("Allowed tags for namespace '%s': %s", namespace, self.ALLOWED_TAGS[namespace])

    def check_tag_allowed(self, tag: str) -> bool:
        """
        Check if a tag is allowed.

        :param tag: The tag to check.
        :return: True if the tag is allowed, False otherwise.
        """
        return any([(tag in self.ALLOWED_TAGS[namespace]) for namespace in self.ALLOWED_TAGS])

    def identify(self) -> list[list[float | int | str]]:
        """
        Identify and validate tags against expected outputs.

        :return: A sorted list of results with match ratios and file names.
        """
        self.logger.debug("Identifying tags...")
        if len(self.ALLOWED_TAGS['html']) == 0:
            self.check_allowed_tags()
        self.check_allowed_attrs()
        self.check_depth()
        arr = self.DEFAULT_SANITIZER.checks
        res = self.call_handler([tag.payload for tag in arr])
        for i in range(len(res)):
            all_tags_allowed = all([self.check_tag_allowed(tag) for tag in arr[i].tags])
            if  all_tags_allowed and  not(arr[i].check(Template(res[i]).safe_substitute(self.TEMPLATE_VARS))):
                self.logger.debug("Found incorrect parsing logic: %s, but %s is expected", res[i], arr[i].expected_output)
                self.INCORRECT_PARSED.append({"output": res[i].strip(), "expected": arr[i].expected_output})
                

        json_files = [f for f in importlib.resources.files('hui.results_parsers').iterdir() if f.name.endswith('.json')]

        result = []
        for json_file in json_files:
            with open(json_file) as f:
                data = json.load(f)

            # Count the number of matches in the JSON file
            matches = sum([1 for i in range(len(res)) if Template(data[i]).substitute(self.TEMPLATE_VARS).strip() in res[i].strip()])
            result.append([matches / len(data), matches, json_file.name.split('.')[0]])

        result = sorted(result, reverse=True)
        self.logger.debug("Identification results: %s", result)
        return result

    def check_namespace_supported(self, namespace: str) -> bool:
        """
        Check if the specified namespace is supported.

        :param namespace: The namespace to check.
        :raises Exception: If the namespace is invalid or not supported.
        :return: True if the namespace is supported, False otherwise.
        """
        if not self.ALLOWED_TAGS_CHECKED:
            self.check_allowed_tags()
        if namespace not in self.ALLOWED_TAGS:
            raise Exception('Invalid namespace name')
        return len(self.ALLOWED_TAGS[namespace]) > 0
    
    def check_attr_allowed(self, attr: str, tag: str = None, attr_value: str = "https://github.com/Slonser/hui") -> bool:
        """
        Checks if a given attribute is allowed for a specified tag.

        This method checks if a given attribute is allowed for a specified tag by simulating the parsing of HTML elements with the attribute and then checking if the attribute is present in the parsed attributes.

        :param attr: The attribute to check.
        :param tag: The tag to check the attribute for. Defaults to None, which means the first allowed HTML tag will be used.
        :param attr_value: The value to assign to the attribute for testing. Defaults to "https://github.com/Slonser/hui".
        :return: True if the attribute is allowed, False otherwise.
        """
        if tag is None:
            assert self.check_namespace_supported("html"), "No tags allowed"
            tag = self.ALLOWED_TAGS['html'][0]
        
        # Simulate parsing of HTML elements with the attribute to check
        res = self.call_handler([f'<{tag} {attr}="{attr_value}"></{tag}>',
                                 f'<{tag}/{attr}="{attr_value}"></{tag}>']) # In some situations, the attribute might only be parsed with a / symbol
        self.parser.check(res[0]+res[1])
        # Check if the attribute is present in the parsed attributes
        return attr in [attr_parsed[0] for attr_parsed in self.parser.found_attrs]
    
    def check_allowed_attrs(self):
        """
        Check and validate allowed attributes for HTML tags.

        This method checks if global attributes, event attributes, and default attributes are allowed.
        It updates the ATTRIBUTES dictionary with the allowed attributes and logs the results.

        :return: A dictionary containing the allowed attributes categorized by global, event, and specific tags.
        """
        for attr in GLOBAL_ATTRS:
            is_allowed = self.check_attr_allowed(attr)
            if is_allowed:
                self.ATTRIBUTES["attrs_allowed"]["global"].append(attr)
        

        for attr in EVENT_ATTRS:
            is_allowed = self.check_attr_allowed(attr)
            if is_allowed:
                self.ATTRIBUTES["events"]["events"].append(attr)

        for tag in DEFAULT_ATTRS:
            self.ATTRIBUTES["attrs_allowed"][tag] = []
            for attr in DEFAULT_ATTRS[tag]:
                is_allowed = self.check_attr_allowed(attr,tag=tag)
                if is_allowed:
                    self.ATTRIBUTES["attrs_allowed"][tag].append(attr)
 
        self.ATTRIBUTES["data_attributes"] = self.check_attr_allowed("data-hui")
        if self.ATTRIBUTES["data_attributes"]:
            self.logger.debug("data attributes allowed")
        
        self.ATTRIBUTES["custom_attribute"] = self.check_attr_allowed("custom")

        if self.ATTRIBUTES["custom_attribute"]:
            self.logger.debug("Custom attributes allowed")
        
        self.ATTRIBUTES["event_attributes_blocked"] = not(self.check_attr_allowed("onhui"))
        
        if self.ATTRIBUTES["custom_attribute"] and self.ATTRIBUTES["event_attributes_blocked"]:
            self.logger.debug("Event attributes directly blocked")
        
        return self.ATTRIBUTES
    
    def check_depth(self):
        """
        Check and validate the depth of HTML tags.

        This method checks if the depth of HTML tags exceeds the limit and updates the DEPTH_LIMITS accordingly.

        :return: DEPTH_LIMITS
        """
        assert self.check_namespace_supported("html"), "No tags allowed"
        tag = self.ALLOWED_TAGS['html'][0]
        res = self.call_handler([f'<div>'*514+f'</div>'])
        self.parser.check(res[0])
        if self.parser.max_depth > 512:
            self.DEPTH_LIMITS = (self.parser.max_depth, 'No max tags limit')
        elif self.parser.start_tags > 512:
            self.DEPTH_LIMITS = (self.parser.max_depth, 'Flattening')
        else:
            self.DEPTH_LIMITS = (self.parser.max_depth, 'Removing')
        return self.DEPTH_LIMITS
