from hui.identify import Identifier
import requests
from time import sleep

def handler(payload):
    return requests.get("http://localhost:3005/sanitize",params={"html":payload}).text

a = Identifier(handler=handler, buffer_enabled=True, buffer_limit=64)
print(a.identify())
print(a.ALLOWED_TAGS)
print(a.INCORRECT_PARSED)