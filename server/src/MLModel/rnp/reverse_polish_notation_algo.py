from .operation import Operation
from .parentheses import Parentheses


class ReversePolishNotation:

    def __init__(self, expression, parentheses: 'Parentheses' = Parentheses()):
        self._expression = expression.replace(" ", "")
        self._operation = Operation()
        self._parentheses = parentheses
        if not self._is_valid_expression():
            raise Exception("Invalid expression. Please check the syntax.")

    ## METHODS SECTION ##
    def _is_valid_expression(self):
        return self._has_valid_parentheses()  # and self._is_valid_operators()

    def _has_valid_parentheses(self):
        p = 0
        for i in range(len(self._expression)):
            if self._parentheses.is_opening_parenthesis(self._expression[i]):
                p = p + 1
            elif self._parentheses.is_closing_parenthesis(self._expression[i]):
                p = p - 1
            if p < 0:
                return False
        return p == 0

    # to change

    def _is_valid_operators(self):
        return not self._operation.is_operator(self._expression[0]) and not self._operation.is_operator(self._expression[1])

    def _find_closing_parenthesis(self, opening_parenthesis_index):
        p = 1
        for i in range(opening_parenthesis_index + 1, len(self._expression), 1):
            if self._parentheses.is_opening_parenthesis(self._expression[i]):
                p = p + 1
            elif self._parentheses.is_closing_parenthesis(self._expression[i]):
                p = p - 1
            if p == 0:
                return i

    def _get_lambda_expression(self):
        lambda_expression = []
        operators_stack = []
        for character in self._expression:

            # if opening_parenthesis
            if self._parentheses.is_opening_parenthesis(character):
                operators_stack.append(character)

            # if number
            elif not self._operation.is_operator(character) and not self._parentheses.is_parenthesis(character):
                lambda_expression.append(character)

            # if operator
            elif self._operation.is_operator(character):
                operator = self._operation.get_operator_by_symbol(character)

                # + or -
                # those operators have less priority
                # so any operator pending in the operator stack are instantly popped to the result
                if operator._precedence == 2:
                    if len(operators_stack) > 0 and self._operation.is_operator(operators_stack[-1]):
                        lambda_expression.append(operators_stack.pop())

                # * or /
                # top operator on the operator stack are popped to the result
                # only if they have greater or equal priority than the current operator
                elif operator._precedence == 3:
                    if len(operators_stack) > 0 and self._operation.is_operator(operators_stack[-1]):
                        top_stack_operator = self._operation.get_operator_by_symbol(
                            operators_stack[-1])
                        if operator <= top_stack_operator:
                            lambda_expression.append(operators_stack.pop())

                # ^
                # top operator popped if it is the same operator
                else:
                    if len(operators_stack) > 0 and self._operation.is_operator(operators_stack[-1]):
                        top_stack_operator = self._operation.get_operator_by_symbol(
                            operators_stack[-1])
                        if operator == top_stack_operator:
                            lambda_expression.append(operators_stack.pop())

                operators_stack.append(character)

            # if closing_parenthesis
            elif self._parentheses.is_closing_parenthesis(character):
                i = len(operators_stack) - 1
                while i >= 0 and not self._parentheses.is_opening_parenthesis(operators_stack[i]):
                    popped_element = operators_stack.pop()
                    if self._operation.is_operator(popped_element):
                        lambda_expression.append(popped_element)
                    i = i - 1
                operators_stack.pop()

        for i in range(len(operators_stack)):
            lambda_expression.append(operators_stack.pop())
        return lambda_expression

    def solve_expression(self):
        lambda_expression = self._get_lambda_expression()
        operation_stack = []
        for character in lambda_expression:
            if self._operation.is_operator(character):
                operand_2 = float(operation_stack.pop())
                operand_1 = float(operation_stack.pop())
                operation_stack.append(self._operation.calculate(
                    operand_1, operand_2, character))

            else:
                operation_stack.append(character)

        return operation_stack.pop()
