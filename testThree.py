# -*- coding: utf-8 -*-
"""
Created on Sun May 11 18:26:37 2025

@author: henrikas
"""

import sys, random

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, TypeAlias, Optional, NoReturn


# https://hakibenita.com/python-mypy-exhaustive-checking
# https://typing.readthedocs.io/en/latest/source/unreachable.html
def assert_never(value: NoReturn) -> NoReturn:
    assert False, f'Unhandled value: {value} ({type(value).__name__})'


eprint = lambda msg: print(msg, file=sys.stderr)


# We might choose to put helper functions / structures in a separate module
# in the future
class Infix:
    def __init__(self, function:Callable):
        self.function = function
    def __ror__(self, other) -> 'Infix':
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other) -> Any:
        return self.function(other)
    def __rlshift__(self, other) -> 'Infix':
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other) -> Any:
        return self.function(other)
    def __call__(self, value1, value2) -> Any:
        return self.function(value1, value2)

composerev : Infix = Infix(lambda f,g: lambda x: g(f(x)))
pipe : Infix = Infix(lambda x,f: f(x))



program_intro : str = """
----------------------------
Welcome to the Hangman game
Author name
2024
----------------------------
"""

main_menu : str ="""
Main Menu
-----------------------------------------------------
Please select one of the following menu options [1-2]:
1: StartGame
2: Exit
"""


hangman : list [str] = [
r""" 
____
|/   |
|   
|    
|    
|    
|
|_____
""",    
r"""
 ____
|/   |
|   (_)
|    |
|    |    
|    
|
|_____
""",    
r"""
 ____
|/   |
|   (_)
|   \|/
|    |
|    
|
|_____
""",
r"""
 ____
|/   |
|   (_)
|   \|/
|    |
|   / 
|
|_____
""",
r"""
 ____
|/   |
|   (_)
|   \|/
|    |
|   / \
|
|_____
""",
r"""
 ____
|/   |
|   (_)
|   /|\
|    |
|   | |
|
|_____
"""
]

# words : P (seq<str>)
#-------------------------------------------------
# let words = <"BASH", "GNU", "MAN", "LS", "GREP">
words: list[str] = ["BASH", "GNU", "MAN", "CAT", "LS", "GREP"]

# allowed_chars : P (seq<char>)
#--------------------------------------
# let allowed_chars = 
allowed_chars : list[str] = [chr(x) for x in range(ord('A'), ord('Z'))]



class MenuOption(Enum):
    StartGame = 1
    Exit = 2

    @staticmethod
    def parse(s:str) -> Optional['MenuOption']:
        '''MenuOption.parse is a function
            which parses an input string to an Optional MenuOption value

        Parameters:
            s (str) : An input string to try to parse into a MenuOption

        Returns:
            Optional[MenuOption] the function can either parse the input to a valid
                MenuOption value or return a None value upon failure
        '''
        match s.strip().upper():
            case "1" | "ONE" | "START" | "STARTGAME":
                return MenuOption.StartGame
            case "2" | "TWO" | "EXIT":
                return MenuOption.Exit
            case _:
                return None


#toPartialWord : str x set<char> - > str
def to_partial_word (word: str, used: set[str]) -> str:
    return "".join([c if c in used else '_' for c in word])

# isGuessValid : set<char> x char -> bool
def isGuessValid (used:set[str], guess:str, allowed_chars=allowed_chars) -> bool:
   return (guess in allowed_chars) and not (guess in used)

# readGuess : set<char> -> char
def readGuess (used:set[str]) -> str:
    while True:
        match \
        "Please input a single character for your guess: " \
        |pipe| input \
        |pipe| (lambda result:  map(str.upper, result)) \
        |pipe| "".join:
            case guess if len(guess) > 1:
                "ERROR: Invalid input, requires a single character to be specified" \
                |pipe| eprint
            case guess if isGuessValid(used, guess):
                return guess
            case _:
                "ERROR: This character has been guessed previously" \
                |pipe| eprint

# getGuess : set<char> -> char
def getGuess (used:set[str]) -> str:
   guess : str = used |pipe| readGuess
   ("Guess: %s" % guess) |pipe| print
   return guess
   
   
def play (word:str, used:set[str], tally:int):
   hangman[tally] |pipe| print
   word_partial : str = to_partial_word(word, used)
   "".join([c+" " for c in word_partial]) |pipe| print
   if word == word_partial: 
      "YOU WIN!" |pipe| print
   elif tally == len(hangman)-1: 
      "HANGMAN\nYOU LOSE!" |pipe| print
   else:
      "Getting guess" |pipe| print
      guess : str = used |pipe| getGuess
      used.add(guess)
      if guess in word: 
        play(word, used, tally)
      else:
        play(word, used, (tally+1))


def display_main_intro() -> None:
    program_intro |pipe| print
    return

def prompt_main_menu_input() -> MenuOption:
    while True:
        match main_menu |pipe| input |pipe| MenuOption.parse:
            case x if type(x) == MenuOption:
                return x
            case _:
                "ERROR: Not a valid menu option" |pipe| eprint

def branch_to_feature(opt:MenuOption):
    match opt:
        case MenuOption.StartGame:
            play(random.choice(words), set({}), 0)
        case MenuOption.Exit:
            "Exiting the Hangman game..." |pipe| print
            0 |pipe| sys.exit

def navigate_main_menu() -> None:
    display_main_intro()
    while True:
        prompt_main_menu_input() \
        |pipe| branch_to_feature 
   
if __name__=="__main__":
    navigate_main_menu()
