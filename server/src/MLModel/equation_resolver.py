import sys
from PIL import Image
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
from rnp.reverse_polish_notation_algo import ReversePolishNotation


class EquationSolver:

    def __init__(self, expression) -> None:
        self._expression = expression

    def __is_equation(self):
        if self._expression.find('=') != -1:
            return True

    def __is_inequation(self):
        if self._expression.find('>') != -1 or self._expression.find('<') != -1:
            return True

    def __solve_equation(self):
        splitted_expression = self._expression.split(' ')
        a = float(splitted_expression[0].replace("H", " H").split(" ")[0])
        b = float(
            splitted_expression[2]) if splitted_expression[1] == "+" else -1 * float(splitted_expression[2])
        c = float(splitted_expression[-1])
        step1 = self._expression
        step2 = splitted_expression[0] + " = " + splitted_expression[-1] + (
            " - " + splitted_expression[2] if splitted_expression[1] == '+' else (" + " + splitted_expression[2]))
        step3 = splitted_expression[0].replace("H", " H").split(
            " ")[1] + " = " + str(c-b) + " / " + str(a)
        step4 = splitted_expression[0].replace("H", " H").split(" ")[
            1] + " = " + str((c-b)/a)
        return step1+"\n"+step2+"\n"+step3+"\n"+step4

    def __solve_inequation(self):
        splitted_expression = self._expression.split(' ')
        a = float(splitted_expression[0].replace("H", " H").split(" ")[0])
        b = float(
            splitted_expression[2]) if splitted_expression[1] == "+" else -1 * float(splitted_expression[2])
        c = float(splitted_expression[-1])
        label = str(a)+"*"+"H"+str(b)+splitted_expression[3]+str(c)
        H = H = np.linspace(-5, 5, 100)
        y = a * H + b
        if splitted_expression[3] == '<':
            mask = y < c
        elif splitted_expression[3] == '<=':
            mask = y <= c
        elif splitted_expression[3] == '>':
            mask = y > c
        elif splitted_expression[3] == '>=':
            mask = y >= c
        else:
            raise Exception("Not a valid inequality")
        plt.plot(H, y, 'r-', label=label)
        plt.fill_between(H, y, where=mask, color='green', alpha=0.5)

        plt.xlabel('H')
        plt.ylabel('y')
        plt.title('Linear Inequality')
        plt.legend()
        plt.grid(True)

        # plt.savefig('inequality_plot.png')
        plt.show()

    def __solve_expression_operation(self):
        rnp = ReversePolishNotation(self._expression)
        return rnp.solve_expression()

    def solve(self):
        if self.__is_equation():
            return self.__solve_equation()
        elif self.__is_inequation():
            return self.__solve_inequation()
        else:
            return self.__solve_expression_operation()


if __name__ == "__main__":
    equation_solver = EquationSolver(sys.argv[1])
    print(equation_solver.solve())
