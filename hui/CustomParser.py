from html.parser import HTMLParser

class CustomParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.customattr_found = False
        self.found_attrs = []
        self.found_tags = []

    def handle_starttag(self, tag, attrs):
        self.found_tags.append(tag)
        self.found_attrs.extend(attrs)

    def check(self, payload):
        self.found_attrs = []
        self.found_tags = []
        self.feed(payload)
        # Need to close parser to clear buffer
        # TODO: Is this best solution?
        self.close()