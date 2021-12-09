# User input & game state
from chess import ChessEngine
import pygame as p

# Initializing pygame
p.init()

# Setting global variables
WIDTH = HEIGHT = 512 #could do 400 too but 512 is a power of 8 so it works well for square size
DIMENSION = 8 #8x8 chess board
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {} # Declaring a dictionary of images


# Initializes a global dictionary of images, will be called ONLY ONCE in main
# Setting this outside of main makes the program more flexible (in case for example we want to use different sets of pieces
def load_images():

    # Loading every piece image into the dictionary
    # "IMAGES['wK'] will return the wK.png image
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        # transform.scale scales the image, so it takes up the whole square
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE,SQUARE_SIZE))


def main():

    # Setting screen variable
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()

    #storing valid moves in the current game state in a list
    valid_moves = game_state.get_valid_moves()
    #flag variable for when a move is made (to make sure the valid moves are only checked AFTER the usesr played a valid move, and not after any move the user makes)
    move_made = False
    load_images()
    #tuple (row,col) that will store the location of the selected square (empty for now)
    sq_selected = ()
    #list that keeps track of player clicks (using two tuples for 1st and 2nd click coordinates : [(6,4), (5,4)])
    player_clicks = []
    game_over = False

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos() #returns (x,y) position of the mouse into a list
                    #for side panel make sure to keep track of the mouse location being relative to the new boundaries

                    #column and row number
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    if sq_selected == (row,col): #if the user clicked same square twice
                        sq_selected = () #deselect
                        player_clicks = [] #clear player clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected) #add both first and second clicks

                    if len(player_clicks) == 2: #if its the player's 2nd click, we need to move the piece
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)): #iterating through the valid moves to see if player's move is in it
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                if e.key == p.K_r: #reset the board when r is pressed (resetting variable)
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False
        draw_game_state(screen, game_state, valid_moves, sq_selected)

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                draw_text(screen, "CHECKMATE - BLACK WINS")
            else:
                draw_text(screen, "CHECKMATE - WHITE WINS")
        elif game_state.stale_mate:
            game_over = True
            draw_text(screen, "STALEMATE - DRAW")

        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

#highlights square selected and moves for piece selected
def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != ():
        r, c = square_selected
        if game_state.board[r][c][0] == ('w' if game_state.white_to_move else 'b'): #if its white's turn to move, set gs.board[r][c][0] to 'w', otherwise set it to 'b'
            #highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100) #the higher the value is (0-255), the more opaque
            s.fill(p.Color('gray'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

            #draw circle on valid moves squares
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    if game_state.board[move.end_row][move.end_col][0] == ('b' if game_state.white_to_move else 'w'): #if the square has an enemy piece
                        screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))
                    else: #if the square is empty
                        p.draw.circle(screen,'yellow', ((move.end_col * SQUARE_SIZE + 33), (move.end_row * SQUARE_SIZE + 33)), 10)

#end game text
def draw_text(screen, text):
    font = p.font.SysFont("consolas", 35, True, False)
    text_item = font.render(text, 0, p.Color('Dark Green'))
    text_location = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - text_item.get_width()/2, HEIGHT/2.5 - text_item.get_height()/2.5)
    screen.blit(text_item, text_location)

#handles all graphics in the current game state
def draw_game_state(screen, game_state, valid_moves, sq_selected):
    draw_board(screen)
    highlight_square(screen, game_state, valid_moves, sq_selected)
    draw_pieces(screen, game_state.board)



#draws squares on the board (before drawing the pieces)
def draw_board(screen):
    # due to the n*n structure of the board and the fact that the top left square is always light then when row+column/2 is even, its a white square
    #creating a list of two colors so its indices can be used to determine position of square on the board
    colors = [p.Color("white"), p.Color("pink")]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


#draws pieces on top of squares
# doing this as a separate function in case highlighting squares is added
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "**": #if the square isn't empty
                screen.blit(IMAGES[piece], p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == "__main__":
    main()


