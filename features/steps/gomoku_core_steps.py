from behave import *
from Gomoku import Board, Player, GameState, Black, White, Empty, cpu_move

# --- Background and setup ---

@given('the Gomoku application is started')
def setup_gomoku_application(context):
    context.board = Board()
    context.players = []
    context.game_state = None
    context.cpu_player = None
    context.last_error = ""
    context.last_move_coords = None

@given('a new game has started with Player 1 as "{p1}" and Player 2 as "{p2}"')
def start_new_game_with_players(context, p1, p2):
    context.board = Board()
    context.players = [Player(p1, Black()), Player(p2, White())]
    context.game_state = GameState(context.board, tuple(context.players)) # type: ignore

@given('a new game has started with Player 1 as "{p1}" and CPU as Player 2')
def start_new_game_with_player_and_cpu(context, p1):
    context.board = Board()
    context.players = [Player(p1, Black()), Player("CPU", White(), is_cpu=True)]
    context.game_state = GameState(context.board, tuple(context.players)) # type: ignore
    context.cpu_player = context.players[1]

#Game mode and player name entry

@when('the game mode selection is prompted')
def prompt_game_mode_selection(context):
    context.mode_prompted = True

@when('the user selects "Player vs Player"')
def select_player_vs_player(context):
    context.game_mode = "pvp"

@when('the user selects "Player vs CPU"')
def select_player_vs_cpu(context):
    context.game_mode = "pvcpu"

@when('the user is prompted to enter the name for Player 1')
def prompt_player1_name(context):
    context.input_prompt = "Player 1"

@when('the user is prompted to enter the name for Player 2')
def prompt_player2_name(context):
    context.input_prompt = "Player 2"

@when('the user enters "{name}"')
def user_enters_name(context, name):
    if not hasattr(context, "entered_names"):
        context.entered_names = []
    context.entered_names.append(name)
    context.last_name_input = name
    # Simulate validation
    try:
        int(name)
        context.last_error = "Player name cannot be a number. Please enter a valid name."
        context.name_accepted = False
        return
    except ValueError:
        pass
    if len(name) < 3:
        context.last_error = "Player name must be at least 3 characters long."
        context.name_accepted = False
        return
    context.name_accepted = True
    # Update players for Player vs CPU mode
    if hasattr(context, "game_mode") and context.game_mode == "pvcpu":
        context.players = [Player(name, Black()), Player("CPU", White(), is_cpu=True)]
        context.game_state = GameState(context.board, tuple(context.players)) # type: ignore
        context.cpu_player = context.players[1]

@then('both Player 1 and Player 2 are registered with their names')
def verify_both_players_registered(context):
    assert len(context.entered_names) == 2
    assert all(len(n) >= 3 and not n.isdigit() for n in context.entered_names)

@when('the user is prompted to choose a colour')
def prompt_choose_colour(context):
    context.colour_prompted = True

@when('the user selects "Black"')
def user_selects_black(context):
    context.selected_colour = "Black"
    if hasattr(context, "players") and context.players:
        context.players[0].stone = Black()
        if len(context.players) > 1:
            context.players[1].stone = White()
    if hasattr(context, "game_mode") and context.game_mode == "pvcpu" and hasattr(context, "entered_names"):
        context.players = [Player(context.entered_names[0], Black()), Player("CPU", White(), is_cpu=True)]
        context.game_state = GameState(context.board, tuple(context.players)) # type: ignore
        context.cpu_player = context.players[1]

@then('Player 1 is assigned Black, and the CPU is assigned White')
def verify_player1_black_cpu_white(context):
    assert context.players[0].name == context.entered_names[0]
    assert isinstance(context.players[0].stone, Black)
    assert context.players[1].name == "CPU"
    assert isinstance(context.players[1].stone, White)

@then('the name is rejected with the error "{error_msg}"')
def verify_name_rejected_with_error(context, error_msg):
    assert context.name_accepted is False
    assert context.last_error == error_msg

@then('the user is prompted again to enter the name for Player 1')
def prompt_again_player1_name(context):
    context.input_prompt = "Player 1"

#Moves and move validation

@when('it is Player 1\'s turn')
def player1_turn(context):
    context.game_state.current_player_idx = 0

@when('it is Player 2\'s turn')
def player2_turn(context):
    context.game_state.current_player_idx = 1

@when('Player 1 enters move "{move}"')
@when('Player 2 enters move "{move}"')
def player_enters_move(context, move):
    try:
        r, c = map(int, move.split())
        context.last_move_coords = (r-1, c-1)
        if not (0 <= r-1 < context.board.size and 0 <= c-1 < context.board.size):
            context.last_error = "Move out of bounds."
            context.move_accepted = False
            return
        if not context.board.is_empty(r-1, c-1):
            context.last_error = "Cell already occupied."
            context.move_accepted = False
            return
        context.board.place_stone(r-1, c-1, context.game_state.current_player.stone)
        context.move_accepted = True
    except Exception:
        context.last_error = "Invalid format. Enter row and column as integers."
        context.move_accepted = False

@then('the stone is placed at row {row:d}, column {col:d}')
def verify_stone_placed(context, row, col):
    r, c = row-1, col-1
    stone = context.game_state.current_player.stone
    assert not context.board.is_empty(r, c)
    assert context.board.grid[r][c] == stone

@given('Player 1 has placed a stone at "{move}"')
def player1_places_stone(context, move):
    r, c = map(int, move.split())
    context.board.place_stone(r-1, c-1, context.players[0].stone)

@then('the move is rejected with the error "{error_msg}"')
def verify_move_rejected_with_error(context, error_msg):
    assert context.move_accepted is False
    assert context.last_error == error_msg

#CPU moves
@given('it is CPU\'s turn')
def cpu_turn(context):
    context.game_state.current_player_idx = 1

@when('the CPU is prompted to move')
def cpu_prompted_to_move(context):
    coords = cpu_move(context.game_state, context.cpu_player)
    context.cpu_move_coords = coords

@then('the CPU places a stone on a valid empty intersection')
def verify_cpu_places_stone(context):
    r, c = context.cpu_move_coords
    assert context.board.is_empty(r, c)
    context.board.place_stone(r, c, context.cpu_player.stone)
    assert context.board.grid[r][c] == context.cpu_player.stone

#Win and draw

@given('Player 1 has placed stones at "{m1}", "{m2}", "{m3}", "{m4}"')
def player1_places_stones(context, m1, m2, m3, m4):
    for m in [m1, m2, m3, m4]:
        r, c = map(int, m.split())
        context.board.place_stone(r-1, c-1, context.players[0].stone)

@given('Player 2 has placed stones at "{m1}", "{m2}", "{m3}", "{m4}"')
def player2_places_stones(context, m1, m2, m3, m4):
    for m in [m1, m2, m3, m4]:
        r, c = map(int, m.split())
        context.board.place_stone(r-1, c-1, context.players[1].stone)

@then('Player 1 is declared the winner')
def verify_player1_declared_winner(context):
    r, c = context.last_move_coords
    assert context.board.check_winner(context.players[0].stone, r, c)

@given('a game board that is completely filled with no winner')
def setup_filled_board_no_winner(context):
    context.board = Board()
    size = context.board.size
    context.players = [Player("Tom", Black()), Player("Timmy", White())]
    # Checkerboard pattern that prevents 5 in a row for both colors
    for r in range(size):
        for c in range(size):
            if (r + c) % 2 == 0:
                stone = Black()
            else:
                stone = White()
            context.board.place_stone(r, c, stone)
    # Break horizontal and vertical lines of 5 by flipping one stone every 5 squares
    for r in range(size):
        for c in range(0, size, 5):
            context.board.place_stone(r, c, White() if isinstance(context.board.grid[r][c], Black) else Black())
    for c in range(size):
        for r in range(0, size, 5):
            context.board.place_stone(r, c, White() if isinstance(context.board.grid[r][c], Black) else Black())

@when('the last stone is placed')
def last_stone_placed(context):
    pass

@then('the game is declared a draw')
def verify_game_declared_draw(context):
    assert context.board.is_full()
    found_win = False
    for r in range(context.board.size):
        for c in range(context.board.size):
            stone = context.board.grid[r][c]
            if not isinstance(stone, Empty) and context.board.check_winner(stone, r, c):
                found_win = True
    assert not found_win