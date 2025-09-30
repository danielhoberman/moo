# -------------------------------
# Grammar (BNF-style)
# -------------------------------
# <program>       ::= <statement>*
# <statement>     ::= <expression> ";"
# <expression>    ::= <prefix_expr> ( <infix_op> <expression> )*
# <prefix_expr>   ::= INT | FLOAT | "(" <expression> ")"
# <infix_op>      ::= "+" | "-" | "*" | "/" | "%" | "^"

from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType
from typing import Any, Callable, Optional
from enum import Enum, auto

from .ast import Statement, Expression, Program
from .ast import ExpressionStatement
from .ast import InfixExpression
from .ast import IntegerLiteral, FloatLiteral


# -------------------------------
# Precedence Types
# -------------------------------
class PrecedenceType(Enum):
    P_LOWEST = 0
    P_EQUALS = auto()       # ==, != (not used yet, but good for future)
    P_LESSGREATER = auto()  # <, >
    P_SUM = auto()          # +, -
    P_PRODUCT = auto()      # *, /, %
    P_EXPONENT = auto()     # ^
    P_PREFIX = auto()       # -X, !X
    P_CALL = auto()         # function calls
    P_INDEX = auto()        # array indexing


# -------------------------------
# Precedence Mapping
# -------------------------------
PRECEDENCES: dict[TokenType, PrecedenceType] = {
    TokenType.PLUS: PrecedenceType.P_SUM,
    TokenType.MINUS: PrecedenceType.P_SUM,
    TokenType.ASTERISK: PrecedenceType.P_PRODUCT,
    TokenType.SLASH: PrecedenceType.P_PRODUCT,
    TokenType.MODULUS: PrecedenceType.P_PRODUCT,
    TokenType.POW: PrecedenceType.P_EXPONENT,
}


# -------------------------------
# Parser
# -------------------------------
class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.errors: list[str] = []

        eof_token = Token(TokenType.EOF, "", 0, 0)
        self.current_token: Token = eof_token
        self.peek_token: Token = eof_token

        # Prefix parse functions (things that start expressions)
        self.prefix_parse_fns: dict[TokenType, Callable[[], Any]] = {
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_grouped_expression,
        }

        # Infix parse functions (things that appear between expressions)
        self.infix_parse_fns: dict[TokenType, Callable[[Any], Any]] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.SLASH: self.__parse_infix_expression,
            TokenType.ASTERISK: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.MODULUS: self.__parse_infix_expression,
        }

        # Initialize current and peek tokens
        self.__next_token()
        self.__next_token()

    # ---------------------------
    # Token Management
    # ---------------------------
    def __next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def __peek_token_is(self, tt: TokenType) -> bool:
        return self.peek_token is not None and self.peek_token.type == tt

    def __expect_peek(self, tt: TokenType) -> bool:
        if self.__peek_token_is(tt):
            self.__next_token()
            return True
        else:
            self.__peek_error(tt)
            return False

    def __current_precedence(self) -> PrecedenceType:
        if self.current_token is None:
            return PrecedenceType.P_LOWEST
        return PRECEDENCES.get(self.current_token.type, PrecedenceType.P_LOWEST)

    def __peek_precedence(self) -> PrecedenceType:
        if self.peek_token is None:
            return PrecedenceType.P_LOWEST
        return PRECEDENCES.get(self.peek_token.type, PrecedenceType.P_LOWEST)

    # ---------------------------
    # Error Helpers
    # ---------------------------
    def __peek_error(self, tt: TokenType) -> None:
        got = self.peek_token.type if self.peek_token else "None"
        self.errors.append(f"Expected next token to be {tt}, got {got} instead")

    def __no_prefix_parse_fn_error(self, tt: TokenType) -> None:
        self.errors.append(f"No prefix parse function for {tt} found")

    # ---------------------------
    # Program Parsing
    # ---------------------------
    def parse_program(self) -> Program:
        program: Program = Program()

        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            stmt: Statement = self.__parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.__next_token()

        return program

    # ---------------------------
    # Statement Parsing
    # ---------------------------
    def __parse_statement(self) -> Statement:
        return self.__parse_expression_statement()
    
    def __parse_expression_statement(self) -> ExpressionStatement:
        expr = self.__parse_expression(PrecedenceType.P_LOWEST)

        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()

        return ExpressionStatement(expr=expr)

    # ---------------------------
    # Expression Parsing
    # ---------------------------
    def __parse_expression(self, precedence: PrecedenceType) -> Optional[Expression]:
        prefix_fn: Callable | None = self.prefix_parse_fns.get(self.current_token.type)
        if prefix_fn is None:
            self.__no_prefix_parse_fn_error(self.current_token.type)
            return None
        
        left_expr: Expression = prefix_fn()

        while (
            self.peek_token is not None
            and not self.__peek_token_is(TokenType.SEMICOLON)
            and precedence.value < self.__peek_precedence().value
        ):
            infix_fn: Callable | None = self.infix_parse_fns.get(self.peek_token.type)
            if infix_fn is None:
                return left_expr
            
            self.__next_token()
            left_expr = infix_fn(left_expr)

        return left_expr

    from typing import Optional

    def __parse_infix_expression(self, left_node: Expression) -> Optional[Expression]:
        operator = self.current_token.literal
        precedence = self.__current_precedence()

        self.__next_token()
        right_expr: Optional[Expression] = self.__parse_expression(precedence)

        if right_expr is None:
            # Bail out gracefully if RHS couldn’t be parsed
            return None

        return InfixExpression(
            left_node=left_node,
            operator=operator,
            right_node=right_expr,
        )

    
    def __parse_grouped_expression(self) -> Optional[Expression]:
        self.__next_token()

        expr: Optional[Expression] = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.RPAREN):
            return None

        return expr

    # ---------------------------
    # Prefix Parse Methods
    # ---------------------------
    def __parse_int_literal(self) -> Optional[Expression]:
        """Parses an IntegerLiteral Node from the current token"""
        try:
            return IntegerLiteral(value=int(self.current_token.literal))
        except ValueError:
            self.errors.append(f"Could not parse {self.current_token.literal} as an integer.")
            return None
    
    def __parse_float_literal(self) -> Optional[Expression]:
        """Parses a FloatLiteral Node from the current token"""
        try:
            return FloatLiteral(value=float(self.current_token.literal))  # ✅ fixed (was int)
        except ValueError:
            self.errors.append(f"Could not parse {self.current_token.literal} as a float.")
            return None
