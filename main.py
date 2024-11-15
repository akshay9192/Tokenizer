import enum
import pathlib
import sys
from typing import Any
from prometheus_client import start_http_server, Counter
import time
import threading

# Prometheus metrics setup
TOKENIZATION_REQUESTS = Counter('tokenization_requests_total', 'Total number of tokenization requests')

class TokenType(enum.Enum):
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    STAR = "STAR"
    DOT = "DOT"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    SEMICOLON = "SEMICOLON"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    SLASH = "SLASH"
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    EOF = "EOF"

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any | None, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str:
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type.value} {self.lexeme} {literal_str}"

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errors: list[str] = []

    def scan_tokens(self) -> tuple[list[Token], list[str]]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.errors

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        char = self.advance()
        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case "*":
                self.add_token(TokenType.STAR)
            case ".":
                self.add_token(TokenType.DOT)
            case ",":
                self.add_token(TokenType.COMMA)
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "!":
                self.add_token(TokenType.BANG_EQUAL) if self.match("=") else self.add_token(TokenType.BANG)
            case "=":
                self.add_token(TokenType.EQUAL_EQUAL) if self.match("=") else self.add_token(TokenType.EQUAL)
            case "<":
                self.add_token(TokenType.LESS_EQUAL) if self.match("=") else self.add_token(TokenType.LESS)
            case ">":
                self.add_token(TokenType.GREATER_EQUAL) if self.match("=") else self.add_token(TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                ...
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha_numeric(char):
                    self.identifier()
                else:
                    self.error(f"Unexpected character: {char}")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Any | None = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.errors.append(f"[line {self.line}] Error: Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
        while self.is_digit(self.peek()):
            self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def is_alpha(self, char: str) -> bool:
        return char >= "a" and char <= "z" or char >= "A" and char <= "Z" or char == "_"

    def is_alpha_numeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        token_type = self.identifier_type(text)
        self.add_token(token_type)

    def identifier_type(self, text: str) -> TokenType:
        """Check if the identifier matches any reserved words."""
        reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
        return reserved_words.get(text, TokenType.IDENTIFIER)

    def error(self, char: str) -> None:
        self.errors.append(f"[line {self.line}] Error: {char}")

# Prometheus metrics monitoring
def monitor_tokenization(file_contents: str):
    # Track the number of tokenizations using the counter metric
    TOKENIZATION_REQUESTS.inc()  # Increment the request counter after processing the file

    # Simulate the tokenization process
    scanner = Scanner(file_contents)
    tokens, errors = scanner.scan_tokens()
    for token in tokens:
        print(token)

# Start Prometheus server
def start_prometheus_server():
    print("Starting Prometheus server on port 8000...")
    start_http_server(8000)
    print("Prometheus server started on port 8000.")

def main():
    # Start Prometheus server in a separate thread
    prometheus_thread = threading.Thread(target=start_prometheus_server)
    prometheus_thread.daemon = True
    prometheus_thread.start()

    # File path from command line argument
    if len(sys.argv) < 3:
        print("Usage: python main.py tokenize <file_path>")
        exit(1)

    if sys.argv[1] != "tokenize":
        print("Invalid command. Use 'tokenize' as the first argument.")
        exit(1)

    file_path = pathlib.Path(sys.argv[2])
    if not file_path.exists():
        print(f"File {file_path} does not exist!", file=sys.stderr)
        exit(1)

    # Read the content of the file
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # Monitor tokenization and process the file
    monitor_tokenization(file_contents)

    # Keep the main program running so that Prometheus server continues in the background
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
