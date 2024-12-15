const fs = require('fs');
const xss = require('xss');

function generate() {
    const arr = JSON.parse(fs.readFileSync("generated_payloads.json"));
    const res = [];
    for(let payload of arr){
        try{
            const html_content = `${payload}`;
            console.log(html_content)
            const sanitized_html = xss(html_content);
            res.push(sanitized_html);
        }catch(e){
            res.push("");
        }
    }
    fs.writeFileSync("results_parsers/JS_JSXSS.json", JSON.stringify(res));
}

if (require.main === module) {
    generate();
}