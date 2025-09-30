from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class NodeType(Enum):
    Program = "Program"

    # Statements
    ExpressionStatement = "ExpressionStatement"

    # Expressions
    InfixExpression = "InfixExpression"

    # Literals
    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"


# -------------------------------
# Base Node
# -------------------------------
class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass


# -------------------------------
# Abstract categories
# -------------------------------
class Statement(Node):
    pass

class Expression(Node):
    pass


# -------------------------------
# Root Program Node
# -------------------------------
class Program(Node):
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [stmt.json() for stmt in self.statements]
        }


# -------------------------------
# Statements
# -------------------------------
class ExpressionStatement(Statement):
    def __init__(self, expr: Optional[Expression] = None) -> None:
        self.expr: Optional[Expression] = expr

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.expr.json() if self.expr else None
        }


# -------------------------------
# Expressions
# -------------------------------
class InfixExpression(Expression):
    def __init__(self, left_node: Expression, operator: str, right_node: Expression) -> None:
        self.left_node: Expression = left_node
        self.operator: str = operator
        self.right_node: Expression = right_node

    def type(self) -> NodeType:
        return NodeType.InfixExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.json(),
            "operator": self.operator,
            "right_node": self.right_node.json()
        }


# -------------------------------
# Literals
# -------------------------------
class IntegerLiteral(Expression):
    def __init__(self, value: int) -> None:
        self.value: int = value
        
    def type(self) -> NodeType:
        return NodeType.IntegerLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
    

class FloatLiteral(Expression):
    def __init__(self, value: float) -> None:
        self.value: float = value
        
    def type(self) -> NodeType:
        return NodeType.FloatLiteral   # ✅ fixed bug
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
