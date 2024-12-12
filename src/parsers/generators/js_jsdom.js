const fs = require('fs');
const { JSDOM } = require('jsdom');

function generate() {
    const arr = JSON.parse(fs.readFileSync("generated_payloads.json"));
    const res = [];
    for(let payload of arr){
        try{
            const html_content = `${payload}`;
            const dom = new JSDOM();
            dom.window.document.body.innerHTML = html_content;
            const body_inner_html = dom.window.document.body.innerHTML;
            res.push(body_inner_html);
        }catch(e){
            res.push("");
        }
    }
    fs.writeFileSync("results_parsers/JSDOM_HTML.json", JSON.stringify(res));
}

if (require.main === module) {
    generate();
}