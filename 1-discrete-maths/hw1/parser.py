import itertools

tokens = (
    'NAME', 'BOOLEAN',
    'DISJUNCTION', 'CONJUNCTION', 'IMPLICATION', 'EQUALITY',
    'NEGATION', 'EQUALS',
    'LPAREN', 'RPAREN')

# Tokens
t_DISJUNCTION = r'∨'
t_CONJUNCTION = r'&'
t_IMPLICATION = r'=>'
t_EQUALITY = r'~'
t_NEGATION = r'!'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_BOOLEAN(t):
    r'[0|1]'
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

print("\nHi! Consider using following symbols: & ∨ ~ ! => 0 1\n")

def process_formula(name):
    try:
        str = input('boolean expression %s > ' % name)
    except EOFError:
        return
    formula = "%s = %s" % (name, str)
    yacc.parse(formula)
    vars = list(names.keys())
    vars.remove(name)
    names.clear()
    return vars, formula

name1 = 'expression_A'
name2 = 'expression_B'

vars1, form1 = process_formula(name1)
vars2, form2 = process_formula(name2)

all_vars = list(set(vars1).union(vars2))
all_vars.sort()
print("\nvariables from both formulas:", all_vars)

def do():
    ans_0 = ""
    ans = ""

    all_bin_combinations = list(map(list, itertools.product([False, True], repeat=len(all_vars))))
    for comb in all_bin_combinations:
        for i in range(len(all_vars)):
            names[all_vars[i]] = comb[i]
        yacc.parse(form1)
        value1 = names[name1]
        yacc.parse(form2)
        value2 = names[name2]
        if value1 == True and value2 == False:
            print("\nC does not exist for given A and B.\n")
            return
        elif value1 == True and value2 == True:
            if len(ans) != 0:
                ans += " | "
            ans += "("
            for i in range(len(all_vars)):
                if comb[i] == 0:
                    ans += "!"
                ans += all_vars[i]
                if i != len(all_vars) - 1:
                    ans += " & "
            ans += ")"
        elif value1 == False and value2 == False:
            if len(ans_0) != 0:
                ans_0 += " | "
            ans_0 += "("
            for i in range(len(all_vars)):
                if comb[i] == 0:
                    ans_0 += "!"
                ans_0 += all_vars[i]
                if i != len(all_vars) - 1:
                    ans_0 += " & "
            ans_0 += ")"

    if ans_0 != "":
        ans += "!( %s )" % ans_0

    if ans == "":
        random_formula = "1"
        for var in all_vars:
            random_formula += " => %s" % var
        print("\nany boolean formula is a valid C, for example: %s\n" % random_formula)

    else:
        print("\nan example of valid C: %s\n" % ans)

do()
