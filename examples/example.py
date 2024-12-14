from hui.identify import Identifier
import requests

def handler(payload):
    return requests.get("http://localhost:3005/sanitize",params={"html":payload}).text

a = Identifier(handler=handler, buffer_enabled=False, buffer_limit=64, debug_mode=False)
print(a.identify())
print(a.check_attr_allowed("href",tag="a"))
print(a.INCORRECT_PARSED)
print(a.ALLOWED_TAGS)
print(a.ATTRIBUTES)