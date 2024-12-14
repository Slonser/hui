# Html Universal Identifier

Html Universal Identifier is an alpha version of an application designed for identifying server-side HTML parsers. This package provides a way to determine which HTML, SVG, and MathML tags are allowed, helps to find parser features (incorrectly implemented tags), and can also help to guess which parser is used on the backend.

Primarily, this library relies on the incorrectness of HTML parsing, for example, here are some classic examples:
- `<form><form>text</form></form>` should be transformed to `<form>text</form>`
- `<h1><h2>text</h2></h1>` should be transformed to `<h1><h2>text</h2></h1>`

There are several reasons why you don't want to rely entirely on allowed tags:
- It won't help you determine which parser your custom sanitization is based on
- Allowed tags can be changed
  
## Features

- Identify allowed HTML, SVG, and MathML tags.
- Identify allowed attributes.
- Identify incorrect parsing
- Use a customizable handler function to process HTML payloads.
- Load and compare results against predefined Parser outputs.

## Installation

To install the package, use pip:

```
pip install hui
```

## Usage

Here is a basic example of how to use the `Identifier` class from the package:

```python
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
```

## Identifier Class

The `Identifier` class is the core of this package. It is responsible for identifying allowed HTML, SVG, and MathML tags based on a handler function that processes HTML payloads.

The class also maintains an `INCORRECT_PARSED` list, which contains payloads that were incorrectly parsed by the handler. For example, this may include cases where the parser fails to remove nested forms and similar issues.

## Current Parsers

The following parsers are currently supported in the project:

- **DOMpurify with JSDOM (JS)**
- **JSDOM (JS)**
- **sanitize_html (JS)**
- **htmlparser2 (JS)**
- **html (python)**
- **lxml (python)**
- **html_sanitizer (python)**
- **net/html (go)**
- **bluemonday (go)**

If you believe a new parser/sanitizer should be added, please create an issue, and I will be happy to include it.
### Constructor Parameters

- **`handler`**: A function that takes a payload and returns an HTML response. Example:
  ```python
  lambda payload: requests.get(f"http://localhost:3000?payload={payload}").text
  ```

- **`buffer_enabled`** (optional, default=False): A boolean flag to enable or disable buffering of payloads before sending them to the handler. By default, buffering is disabled, as it can sometimes lead to incorrect results. For example, some sanitizers may simply remove all input if it contains a dangerous tag. Use buffering only if the server you are interacting with has strict rate limits.

- **`buffer_delimeter`** (optional, default=`<div>TEXTTEXT</div>`): A string used to delimit buffered payloads when sending them to the handler.

- **`buffer_limit`** (optional, default=32): An integer that specifies the maximum number of payloads to buffer before sending them to the handler.

- **`template_vars`** (optional, default=None): A dictionary of template variables to use for substitution in payloads.

- **`debug_mode`** (optional, default=False): A boolean flag to enable or disable debug logging.

### Methods

- **`check_allowed_tags()`**: Checks and populates the `ALLOWED_TAGS` dictionary with allowed tags for HTML, SVG, and MathML.
- **`call_handler(template_payloads: list[str])`**: Calls the handler function with a list of template payloads and returns the processed results.
- **`check_namespace(namespace: str)`**: Checks for allowed tags in the specified namespace (SVG or MathML).
- **`identify()`**: Identifies the best matching Parser based on generated payloads and returns a list of matches.
- **`check_allowed_attrs()`**: Checks and validates allowed attributes for HTML tags.

### identify() Method

The `identify()` method checks if allowed tags have been determined. If not, it calls `check_allowed_tags()` to populate the `ALLOWED_TAGS`. It then loads a list of generated payloads from a JSON file and calls the handler for each payload. Finally, it compares the results against all JSON files in the `results_parsers` directory to count matches and returns a sorted list of results.

- **Returns**: A list of tuples, each containing:
  - The match ratio (float)
  - The number of matches (int)
  - The name of the Parser (str)

### Attributes

- **`ATTRIBUTES`**: A dictionary that holds information about allowed attributes for HTML tags, including:
  - `custom_attribute`: Indicates if custom attributes are allowed.
  - `event_attributes_blocked`: Indicates if event attributes are directly blocked.
  - `data_attributes`: Indicates if data attributes are allowed.
  - `attrs_allowed`: A nested dictionary categorizing allowed attributes into global, event and specific tags attributes.

### Allowed Tags

- **`ALLOWED_TAGS`**: A dictionary that holds information about allowed tags for HTML, SVG, and MathML, including:
  - `html`: A list of allowed HTML tags.
  - `svg`: A list of allowed SVG tags.
  - `math`: A list of allowed MathML tags.

### Incorrectly Parsed Tags

- **`INCORRECT_PARSED`**: A dictionary that holds information about incorrectly parsed tags for HTML, SVG, and MathML, including:
  - `html`: A list of incorrectly parsed HTML tags.
  - `svg`: A list of incorrectly parsed SVG tags.
  - `math`: A list of incorrectly parsed MathML tags.

### DEPTH_LIMITS
**DEPTH_LIMITS**: A tuple that holds information about the depth limits of HTML tags, including:
  - `max_depth`: The maximum depth of HTML tags.
  - `limit_strategy`: The strategy used to handle tags exceeding the depth limit, which can be 'No max tags limit', 'Flattening', or 'Removing'.
