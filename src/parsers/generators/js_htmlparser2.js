const fs = require('fs');
const { parseDocument } = require('htmlparser2');
const cheerio = require('cheerio');

function generate() {
    const arr = JSON.parse(fs.readFileSync("generated_payloads.json"));
    const res = [];
    arr.forEach(payload => {
        const html_content = `<html><body>${payload}</body></html>`;
        const dom = parseDocument(html_content);
        const $ = cheerio.load(dom);
        const body_inner_html = $('body').html();
        res.push(body_inner_html);
    });
    fs.writeFileSync("results_parsers/JS_HTMLPARSER2.json", JSON.stringify(res));
}

if (require.main === module) {
    generate();
}