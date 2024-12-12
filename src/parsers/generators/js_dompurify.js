const fs = require('fs');
const { JSDOM } = require('jsdom');
const DOMPurify = require('dompurify');

function generate() {
    const arr = JSON.parse(fs.readFileSync("generated_payloads.json"));
    const res = [];
    arr.forEach(payload => {
        try{
            const html_content = `${payload}`;
            const window = new JSDOM('').window;
            const purify = DOMPurify(window);
            const sanitized_html = purify.sanitize(html_content);
            res.push(sanitized_html);
        }catch{
            res.push("");
        }
    });
    fs.writeFileSync("results_parsers/JS_DOMPURIFY.json", JSON.stringify(res));
}

if (require.main === module) {
    generate();
}