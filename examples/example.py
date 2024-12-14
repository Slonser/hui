from hui.identify import Identifier
import requests

def handler(payload):
    return requests.get("http://localhost:3005/sanitize",params={"html":payload}).text

a = Identifier(handler=handler, buffer_enabled=False, buffer_limit=64, debug_mode=False)
print(a.identify())
# run all
print(a.check_attr_allowed("href",tag="a"))
# True or False
print(a.INCORRECT_PARSED)
# Example output
# [{'output': '<h5><h6>govnoed</h6></h5>', 'expected': '<h5></h5><h6>$text</h6>'}, .. ]
print(a.ALLOWED_TAGS)
# print allowed tags
print(a.ATTRIBUTES)
# Prints ATTRIBUTES info
print(a.DEPTH_LIMITS)
# Example Outputs:
# (514, 'No max tags limit')
# (512, 'Flattening')
# (255, 'Removing')