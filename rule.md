variable type: integer, float, boolean, list
- integer: 1, 2, 3, 4, 5, 6, n, n+1, ...
- float: 1.1, 1.2, 1.3, ...
- boolean: true, false
- list: [<items>]

comparison:
- equal: "="
- greater than: ">"
- lower than: "<"
- greater or equal: ">="
- lower or equal: "<="
- not: "!"

condition:
- if <condition> {<action>} else {<action>}
- example: if score >= 10 {print "Good work!!"}

function:
- fn <name>(<args>) {<action>}

built-in:
- print, len, range

Note:
- If a variable is being created inside a function, it only exist inside that function
- To do a math operation, we required two variable to be same type (e.g. `1 + 2` will return `3`, `1 + "2"` will return error)

Lexer recognition:
- numbers (int and float)
- identifiers (var)
- keywords (reserved keywords like while, if, else, let, ...)
- simple operator (such as + - * /)
- string and punctuation (text in double quote, symbol like `()`, `,`, `;`)

Rule when collecting chars
- First char must be a letter or _
- The remaining char can be either letters, digits or _
- example: total, my_var, score2, _priv, ....
- invalid: 2score, my-var

AST (abstract syntax tree)
- expression -> num
  - expression + expression
  - expression - expression
  - expression * expression
  - expression / expression
  - ( expression )

environment to store variables