from lxml import etree
import json

def generate():
    arr = json.load(open("generated_payloads.json"))
    res = []
    for payload in arr:
        html_content = f"<html><body>{payload}</body></html>"

        parser = etree.HTMLParser()
        tree = etree.fromstring(html_content, parser)

        body_inner_html = etree.tostring(tree.find('.//body'), encoding='unicode')
        res.append(body_inner_html)
    json.dump(res, open("results_parsers/PYTHON_LXML_HTML.json", "w"))

if __name__ == "__main__":
    generate()