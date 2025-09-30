from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType
from typing import Any, Callable, Optional
from enum import Enum, auto

# Precendence Types

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

# Precedence Mapping
PRECEDENCES: dict[TokenType, PrecedenceType] = {
    # Arithmetic
    TokenType.PLUS: PrecedenceType.P_SUM,
    TokenType.MINUS: PrecedenceType.P_SUM,
    TokenType.ASTERISK: PrecedenceType.P_PRODUCT,
    TokenType.SLASH: PrecedenceType.P_PRODUCT,
    TokenType.MODULUS: PrecedenceType.P_PRODUCT,
    TokenType.POW: PrecedenceType.P_EXPONENT,
}

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer

        self.errors: list[str] = []

        self.current_token: Optional[Token] = None
        self.peek_token: Optional[Token] = None

        # Prefix and Infix parse function maps
        self.prefix_parse_fns: dict[TokenType, Callable[[], Any]] = {}  # -1, like -x
        self.infix_parse_fns: dict[TokenType, Callable[[Any], Any]] = {}  # 5 + 5

        # Initialize current and peek tokens
        self.__next_token()
        self.__next_token()

    # Region Parser helpers --
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

    def __peek_error(self, tt: TokenType) -> None:
        got = self.peek_token.type if self.peek_token else "None"
        self.errors.append(f"Expected next token to be {tt}, got {got} instead")

    def __no_prefix_parse_fn_error(self, tt: TokenType) -> None:
        self.errors.append(f"No prefix parse function for {tt} found")
    # End Region Parser Helpers --

    def parse_program(self) -> None:
        pass

