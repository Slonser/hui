from .parsers import JS_DOM, JS_DOMPURIFY, JS_HTMLPARSER2, PYTHON_HTML, PYTHON_LXML_HTML,PYTHON_HTML_SANITIZER ,GO_HTML, JS_SANITIZE_HTML, GO_bluemonday

def generate():
    parsers_list = [
        JS_DOMPURIFY.SANITIZE_HTML(),
        JS_DOM.SANITIZE_HTML(),
        JS_HTMLPARSER2.SANITIZE_HTML(),
        PYTHON_HTML.SANITIZE_HTML(),
        PYTHON_LXML_HTML.SANITIZE_HTML(),
        GO_HTML.SANITIZE_HTML(),
        JS_SANITIZE_HTML.SANITIZE_HTML(),
        PYTHON_HTML_SANITIZER.SANITIZE_HTML(),
        GO_bluemonday.SANITIZE_HTML(),
    ]
    
    for parser in parsers_list:
        parser.get_results()

if __name__ == "__main__":
    generate()