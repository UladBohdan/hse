import itertools

tokens = (
    'NAME', 'BOOLEAN',
    'DISJUNCTION', 'CONJUNCTION', 'IMPLICATION', 'EQUALITY',
    'NEGATION', 'EQUALS',
    'LPAREN', 'RPAREN')

# Tokens
t_DISJUNCTION = r'v'
t_CONJUNCTION = r'&'
t_IMPLICATION = r'=>'
t_EQUALITY = r'~'
t_NEGATION = r'!'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME = r'[a-uw-zA-Z_][a-uw-zA-Z0-9_]*'

def t_BOOLEAN(t):
    r'[01]{1}'
    t.value = bool(int(t.value))
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left','CONJUNCTION','DISJUNCTION'),
    ('left','IMPLICATION','EQUALITY'),
    ('right','NEGATION'),
)

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression CONJUNCTION expression
                  | expression DISJUNCTION expression
                  | expression IMPLICATION expression
                  | expression EQUALITY expression'''
    if p[2] == t_CONJUNCTION: p[0] = p[1] and p[3]
    elif p[2] == t_DISJUNCTION: p[0] = p[1] or p[3]
    elif p[2] == t_IMPLICATION: p[0] = (not p[1]) or p[3]
    elif p[2] == t_EQUALITY: p[0] = (p[1] == p[3])

def p_expression_negation(p):
    'expression : NEGATION expression'
    p[0] = not p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = bool(p[1])

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        # New variable found.
        names[p[1]] = False
        p[0] = False

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

print("\nConsider using following symbols: & v ~ ! => 0 1\n")

def process_formula(name):
    try:
        str = input('%s > ' % name)
    except EOFError:
        return
    formula = "%s = %s" % (name, str)
    yacc.parse(formula)
    vars = list(names.keys())
    vars.remove(name)
    names.clear()
    return vars, formula

name1 = 'boolean_expression_A'
name2 = 'boolean_expression_B'

vars1, form1 = process_formula(name1)
vars2, form2 = process_formula(name2)

common_vars = list(set(vars1).intersection(vars2))
common_vars.sort()

uniq_vars1 = list(set(vars1).difference(common_vars))
uniq_vars1.sort()

uniq_vars2 = list(set(vars2).difference(common_vars))
uniq_vars2.sort()

def check_formula_independence(name, formula, uniq_vars):
    value = False
    value_computed = False
    bin_combinations = list(map(list, itertools.product([False, True], repeat=len(uniq_vars))))
    for comb in bin_combinations:
        for i in range(len(uniq_vars)):
            names[uniq_vars[i]] = comb[i]
        yacc.parse(formula)
        if not value_computed:
            value = names[name]
            value_computed = True
        else:
            if value != names[name]:
                # The formula DOES depend on uncommon vars. C does not exist.
                print("\nC does not exist for given A and B.\n")
                return False, False
    # The formula really IS independent from any uncommon variables.
    return True, value

def do():
    ans = ""
    ans_0 = ""

    all_common_bin_combinations = list(map(list, itertools.product([False, True], repeat=len(common_vars))))
    for common_comb in all_common_bin_combinations:
        for i in range(len(common_vars)):
            names[common_vars[i]] = common_comb[i]

        # Working with formula A first - it should not depend on uncommon vars.
        ok, value1 = check_formula_independence(name1, form1, uniq_vars1)
        if not ok:
            return
        # We've checked all the combinations - we're ok to go with A.

        # Now to do exactly the same with B.
        ok, value2 = check_formula_independence(name2, form2, uniq_vars2)
        if not ok:
            return

        # If A and B both independent from uncommon variables on given common_comb - we should add it into the output.
        if value1 == True and value2 == False:
            print("\nC does not exist for given A and B.\n")
            return
        elif len(common_vars) > 0:
            if value1 == True and value2 == True:
                if len(ans) != 0:
                    ans += " | "
                ans += "("
                for i in range(len(common_vars)):
                    if common_comb[i] == 0:
                        ans += "!"
                    ans += common_vars[i]
                    if i != len(common_vars) - 1:
                        ans += " & "
                ans += ")"
            elif value1 == False and value2 == False:
                if len(ans_0) != 0:
                    ans_0 += " | "
                ans_0 += "("
                for i in range(len(common_vars)):
                    if common_comb[i] == 0:
                        ans_0 += "!"
                    ans_0 += common_vars[i]
                    if i != len(common_vars) - 1:
                        ans_0 += " & "
                ans_0 += ")"

    if ans_0 != "":
        if ans != "":
            ans += " | "
        ans += "!( %s )" % ans_0

    if ans == "":
        # No common variables - answer is a boolean value.
        if value1 == False and value2 == False:
            ans = "0"
        else:
            ans = "1"

    print("\nan example of valid C: %s\n" % ans)

do()
