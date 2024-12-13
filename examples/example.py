from hui.identify import Identifier
import requests

def handler(payload):
    return requests.get("http://localhost:3005/sanitize",params={"html":payload}).text

a = Identifier(handler=handler)
print(a.identify())
print(a.ALLOWED_TAGS)