from html.parser import HTMLParser

class CustomParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.customattr_found = False
        self.found_attrs = []
        self.found_tags = []
        self.current_depth = 0
        self.max_depth = 0
        self.start_tags = 0

    def handle_starttag(self, tag, attrs):
        self.found_tags.append(tag)
        self.found_attrs.extend(attrs)
        self.current_depth += 1
        self.start_tags += 1
        self.max_depth = max(self.max_depth, self.current_depth)

    def handle_endtag(self, tag):
        self.current_depth -= 1

    def check(self, payload):
        self.found_attrs = []
        self.found_tags = []
        self.current_depth = 0
        self.max_depth = 0
        self.start_tags = 0

        self.feed(payload)
         # Need to close parser to clear buffer
        # TODO: Is this best solution?
        self.close()
        return self.max_depth