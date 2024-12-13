# Html Universal Identifier
This is an alpha version of an application for identifying a server-side HTML parser.


# Example
```python
from hui.identify import Identifier
import requests

def handler(payload):
    return requests.get("http://localhost:3005/sanitize",params={"html":payload}).text

a = Identifier(handler=handler)
print(a.identify())
print(a.ALLOWED_TAGS)
```

# Install 
```
pip install hui
```