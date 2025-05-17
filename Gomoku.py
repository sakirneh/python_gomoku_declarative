# -*- coding: utf-8 -*-
"""
Created on Sat May 17 16:13:43 2025

@author: henrikas
"""
from dataclasses import dataclass
from typing import TypeAlias
from typing import Optional

@dataclass(eq=True, frozen=True)
class B:
 def __str__(self):
     return "B"
# O
@dataclass(eq=True, frozen=True)
class W:
 def __str__(self):
     return "W"
# Let Token = {B} U {W}
# Let Token = {B, W}

Stone: TypeAlias = B | W


@dataclass(eq=True, frozen=True)
class StartvsCPU:
    pass
@dataclass(eq=True, frozen=True)
class StartvsPlayer:
    pass
@dataclass(eq=True, frozen=True)
class QuitGame:
    pass

class Player:
 def __init__(self):
     self.stone = "Unknown"
 def set_Stone(self, new_stone):
     self.stone = new_stone
 def get_Stone(self):
     return self.stone
 def __repr__(self) -> str:
     return self.stone
 
MainMenuOptions: TypeAlias = StartvsCPU | StartvsPlayer |  QuitGame 

# parse_token : String -> Token option
def parse_token(s:str)->Optional[Stone]:
 # match the String input with each case
 match s:
 # String matched X
     case "B" | "b":
     # Return the X class
         return B()
     # String matches O
     case "W" | "w":
     # Return the O class
         return W()
     # Any other case
     case _ :
     # Return None
         return None
