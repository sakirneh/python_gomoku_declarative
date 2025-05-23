Feature: Core Gomoku Game Flow

  As a user, I want to play a complete game of Gomoku, so that I can have a fair and interactive experience.

  Background:
    Given the Gomoku application is started

  Scenario: User selects Player vs Player mode and both players enter valid names
    When the game mode selection is prompted
    And the user selects "Player vs Player"
    And the user is prompted to enter the name for Player 1
    And the user enters "Tom"
    And the user is prompted to enter the name for Player 2
    And the user enters "Timmy"
    Then both Player 1 and Player 2 are registered with their names

  Scenario: User selects Player vs CPU mode, enters name, and selects Black
    When the game mode selection is prompted
    And the user selects "Player vs CPU"
    And the user is prompted to enter the name for Player 1
    And the user enters "Tom"
    And the user is prompted to choose a colour
    And the user selects "Black"
    Then Player 1 is assigned Black, and the CPU is assigned White

  Scenario: User enters an invalid name (too short)
    When the user is prompted to enter the name for Player 1
    And the user enters "To"
    Then the name is rejected with the error "Player name must be at least 3 characters long."
    And the user is prompted again to enter the name for Player 1

  Scenario: User tries to enter a numeric name
    When the user is prompted to enter the name for Player 1
    And the user enters "12345"
    Then the name is rejected with the error "Player name cannot be a number. Please enter a valid name."
    And the user is prompted again to enter the name for Player 1

  Scenario: Player makes a valid move on an empty intersection
    Given a new game has started with Player 1 as "Tom" and Player 2 as "Timmy"
    When it is Player 1's turn
    And Player 1 enters move "8 8"
    Then the stone is placed at row 8, column 8

  Scenario: Player tries to move to an occupied intersection
    Given a new game has started with Player 1 as "Tom" and Player 2 as "Timmy"
    And Player 1 has placed a stone at "8 8"
    When it is Player 2's turn
    And Player 2 enters move "8 8"
    Then the move is rejected with the error "Cell already occupied."

  Scenario: Player tries to move out of bounds
    Given a new game has started with Player 1 as "Tom" and Player 2 as "Timmy"
    When it is Player 1's turn
    And Player 1 enters move "0 1"
    Then the move is rejected with the error "Move out of bounds."

  Scenario: Player attempts to enter an invalid move format
    Given a new game has started with Player 1 as "Tom" and Player 2 as "Timmy"
    When it is Player 1's turn
    And Player 1 enters move "Eight 8"
    Then the move is rejected with the error "Invalid format. Enter row and column as integers."

  Scenario: CPU makes a valid move
    Given a new game has started with Player 1 as "Tom" and CPU as Player 2
    And it is CPU's turn
    When the CPU is prompted to move
    Then the CPU places a stone on a valid empty intersection

  Scenario: Player wins the game with five in a row horizontally
    Given a new game has started with Player 1 as "Tom" and Player 2 as "Timmy"
    And Player 1 has placed stones at "8 8", "8 9", "8 10", "8 11"
    And Player 2 has placed stones at "7 8", "7 9", "7 10", "7 11"
    When it is Player 1's turn
    And Player 1 enters move "8 12"
    Then Player 1 is declared the winner

  Scenario: The game ends in a draw
    Given a game board that is completely filled with no winner
    When the last stone is placed
    Then the game is declared a draw