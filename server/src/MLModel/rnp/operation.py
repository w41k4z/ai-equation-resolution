class Operation:

    def __init__(self) -> None:
        self._operators = [
            _Operator("+", 2, "left"),
            _Operator("-", 2, "left"),
            _Operator("*", 3, "left"),
            _Operator("/", 3, "left"),
            _Operator("^", 4, "right")
        ]

    ## METHODS SECTION ##
    def is_operator(self, character):
        for operator in self._operators:
            if character == operator._operator:
                return True
        return False

    def get_operator_by_symbol(self, character):
        for operator in self._operators:
            if character == operator._operator:
                return operator
        raise Exception("`"+character+"` is not a valid operator")

    def calculate(self, operand_1, operand_2, operator_char):
        operator = self.get_operator_by_symbol(operator_char)

        # +
        if operator._operator == self._operators[0]._operator:
            return operand_1 + operand_2
        # -
        if operator._operator == self._operators[1]._operator:
            return operand_1 - operand_2

        # *
        if operator._operator == self._operators[2]._operator:
            return operand_1 * operand_2

        # /
        if operator._operator == self._operators[3]._operator:
            return operand_1 / operand_2

        # ^
        if operator._operator == self._operators[4]._operator:
            return operand_1 ** operand_2


## PRIVATE CLASS ##
class _Operator:

    def __init__(self, operator, precedence, associativity):
        self._operator = operator
        self._precedence = precedence
        self._associativity = associativity

    ## METHODS SECTION ##
    def __lt__(self, obj: '_Operator'):
        return self._precedence < obj._precedence

    def __le__(self, obj: '_Operator'):
        return self._precedence <= obj._precedence

    def __gt__(self, obj: '_Operator'):
        return self._precedence > obj._precedence

    def __ge__(self, obj: '_Operator'):
        return self._precedence >= obj._precedence

    def __eq__(self, obj: '_Operator'):
        return self._precedence == obj._precedence

    def __ne__(self, obj: '_Operator') -> bool:
        return self._precedence != obj._precedence
