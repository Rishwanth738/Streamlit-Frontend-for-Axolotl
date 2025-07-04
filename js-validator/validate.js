// validate.js
const esprima = require('esprima');

let input = '';

process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const [code1, code2] = input.split('<<<SPLIT>>>');
    try {
        const ast1 = JSON.stringify(esprima.parseScript(code1));
        const ast2 = JSON.stringify(esprima.parseScript(code2));

        if (ast1 === ast2) {
            console.log("ASTs match.");
            process.exit(0);
        } else {
            console.log("ASTs differ.");
            process.exit(1);
        }
    } catch (err) {
        console.error("Parse error:", err.message);
        process.exit(2);
    }
});
