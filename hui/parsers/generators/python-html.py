from bs4 import BeautifulSoup
import json

def generate():
    arr = json.load(open("generated_payloads.json"))
    res = []
    for payload in arr:
        html_content = f"<html><body>{payload}</body></html>"

        soup = BeautifulSoup(html_content, 'html.parser')

        body_inner_html = str(soup.body)
        res.append(body_inner_html[6:-7])
    json.dump(res,open("results_parsers/PYTHON_HTML.json","w"))

if __name__ == "__main__":
    generate()