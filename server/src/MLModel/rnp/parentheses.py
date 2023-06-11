class Parentheses:

    def __init__(self, opening_parenthesis="(", closing_parenthesis=")") -> None:
        self._opening_parenthesis = opening_parenthesis
        self._closing_parenthesis = closing_parenthesis

    ## METHODS SECTION ##
    def is_parenthesis(self, character):
        return self.is_opening_parenthesis(character) or self.is_closing_parenthesis(character)

    def is_opening_parenthesis(self, character):
        return character == self._opening_parenthesis

    def is_closing_parenthesis(self, character):
        return character == self._closing_parenthesis
