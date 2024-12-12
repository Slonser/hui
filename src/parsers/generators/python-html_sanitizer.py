from html_sanitizer import Sanitizer
import json 

def generate():
    arr = json.load(open("generated_payloads.json"))
    res = []
    sanitizer = Sanitizer()
    for payload in arr:
        html_content = f"{payload}"
        sanitized_content = sanitizer.sanitize(html_content)
        res.append(sanitized_content)
    json.dump(res,open("results_parsers/PYTHON_HTML_SANITIZE.json","w"))

if __name__ == "__main__":
    generate()