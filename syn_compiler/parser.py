from cmath import pi
from ply import yacc
from .lexer import Lexer
from .nonTerminal import NonTerminal


class Parser:
    tokens = Lexer().tokens

    def __init__(self):
        self.dictTree_string = None
        self.dictTree = None

    def p_program(self, p):
        """program : entity"""
        p[0] = NonTerminal()
        p[0].value = p[1].value
        self.dictTree_string = p[0].__str__()
        self.dictTree = p[0].value

    def p_entity_enum(self, p):
        """entity : enum"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_entity_struct(self, p):
        """entity : struct"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_entity_array(self, p):
        """entity : array"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_entity_atomic(self, p):
        """entity : atomic"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_entity_list_entity(self, p):
        """entity_list : entity_list entity"""
        p[0] = NonTerminal()
        if p[1].value:
            if type(p[1].value) is not list:
                p[1].value = [p[1].value]
            if type(p[2].value) is not list:
                p[2].value = [p[2].value]
            p[0].value = p[1].value + p[2].value
        else:
            p[0].value = p[2].value
    
    def p_entity_list_lambda(self, p):
        """entity_list : """
        p[0] = NonTerminal()

    def p_field_list_field(self, p):
        """field_list : field_list field"""
        p[0] = NonTerminal()
        if p[1].value:
            p[1].value.update(p[2].value)
            p[0].value = p[1].value
        else:
            p[0].value = p[2].value
    
    def p_field_list_lambda(self, p):
        """field_list : """
        p[0] = NonTerminal()

    def p_field(self, p):
        """field : atomic COLON entity"""
        p[0] = NonTerminal()
        p[0].value = {p[1].value : p[3].value}

    def p_enum_atomic(self, p):
        """enum : atomic LRB entity_list RRB"""
        p[0] = NonTerminal()
        p[0].value = {p[1].value: p[3].value}

    def p_enum_no_atomic(self, p):
        """enum : LRB entity_list RRB"""
        p[0] = NonTerminal()
        p[0].value = p[2].value

    def p_struct_atomic(self, p):
        """struct : atomic LCB field_list RCB"""
        p[0] = NonTerminal()
        p[0].value = {p[1].value: p[3].value}

    def p_struct_no_atomic(self, p):
        """struct : LCB field_list RCB"""
        p[0] = NonTerminal()
        p[0].value = p[2].value
        
    def p_array_atomic(self, p):
        """array : atomic LSB entity_list RSB"""
        p[0] = NonTerminal()
        p[0].value = {p[1].value: p[3].value}

    def p_array_no_atomic(self, p):
        """array : LSB entity_list RSB"""
        p[0] = NonTerminal()
        p[0].value = p[2].value
    
    def p_atomic(self, p):
        """atomic : ID"""
        p[0] = NonTerminal()
        p[0].value = p[1]

    def p_error(self, p):
        raise Exception('ParsingError: invalid grammar at ', p)

    precedence = (

    )

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
