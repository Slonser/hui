const fs = require('fs');
const sanitizeHtml = require('sanitize-html');

function generate() {
    const arr = JSON.parse(fs.readFileSync("generated_payloads.json"));
    const res = [];
    arr.forEach(payload => {
        try{
            const html_content = `${payload}`;
            const sanitized_html = sanitizeHtml(html_content);
            res.push(sanitized_html);
        }catch{
            res.push("");
        }
    });
    fs.writeFileSync("results_parsers/JS_SANITIZE_HTML.json", JSON.stringify(res));
}

if (require.main === module) {
    generate();
}