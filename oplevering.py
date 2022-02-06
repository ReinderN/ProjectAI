import random
import hashlib
import time
import colorama


def tetrisPrint():
    """Prints an animated text that spells Tetris!, in the colors of the games logo"""
    print(colorama.Fore.RED + 'T', end='\r')
    time.sleep(.2)
    print(colorama.Fore.GREEN + 'Te', end='\r')
    time.sleep(.2)
    print(colorama.Fore.LIGHTRED_EX + 'Tet', end='\r')
    time.sleep(.2)
    print(colorama.Fore.MAGENTA + 'Tetr', end='\r')
    time.sleep(.2)
    print(colorama.Fore.CYAN + 'Tetri', end='\r')
    time.sleep(.2)
    print(colorama.Fore.YELLOW + 'Tetris', end='\r')
    time.sleep(.2)
    print(colorama.Fore.WHITE + 'Tetris!', end='\r')


def in_a_row_n_east(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going east"""
    if r_start < 0 or r_start >= len(a) or \
            c_start < 0 or c_start >= len(a[0]) - n+1:
        return False
    for i in range(0, n):
        if a[r_start][c_start+i] != ch:
            return False
    return True


def in_a_row_n_south(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going south"""
    if r_start < 0 or r_start >= len(a) - n+1 or \
            c_start < 0 or c_start >= len(a[0]):
        return False
    for i in range(0, n):
        if a[r_start+i][c_start] != ch:
            return False
    return True


def in_a_row_n_southeast(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going southeast"""
    if r_start < 0 or r_start >= len(a) - n+1 or \
            c_start < 0 or c_start >= len(a[0]) - n+1:
        return False
    for i in range(0, n):
        if a[r_start+i][c_start+i] != ch:
            return False
    return True


def in_a_row_n_northeast(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going northeast"""
    if r_start < n-1 or r_start >= len(a) or \
            c_start < 0 or c_start >= len(a[0]) - n+1:
        return False
    for i in range(0, n):
        if a[r_start-i][c_start+i] != ch:
            return False
    return True


class Board:
    """A data type representing a Connect-4 board
    with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height, alternatief=False):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.alt = alternatief
        self.data = [[' ']*width for row in range(height)]

        # We hoeven niets terug te geven vanuit een constructor!

    def __repr__(self):
        """This method returns a string representation for an object of type Board."""
        s = ''                          # de string om terug te geven
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                text = self.data[row][col]
                if text == 'X':
                    text = colorama.Fore.RED + text + colorama.Fore.RESET + '|'
                else:
                    text = colorama.Fore.YELLOW + text + colorama.Fore.RESET + '|'

                s += text
            s += '\n'

        s += (2*self.width + 1) * '-'   # onderkant van het bord

        # hier moeten de nummers nog onder gezet worden
        s += '\n'
        for i in range(self.width):
            s += ' ' + str(i % 10)

        return s       # het bord is compleet, geef het terug

    def add_move(self, col, ox):
        """Adds a stone for player ox to column col"""
        i = 0
        while i < self.height and self.data[i][col] == ' ':
            i += 1
        self.data[i-1][col] = ox

    def clear(self):
        """Clears the board"""
        self.data = [[' ']*self.width for _ in range(self.height)]

    def set_board(self, move_string):
        """Accepts a string of columns and places
        alternating checkers in those columns,
        starting with 'X'.
        For example, call b.set_board('012345')
        to see 'X's and 'O's alternate on the
        bottom row, or b.set_board('000000') to
        see them alternate in the left column.
        move_string must be a string of one-digit integers.
        """
        next_checker = 'X'  # we starten door een 'X' te spelen
        for col_char in move_string:
            col = int(col_char)
            if 0 <= col <= self.width:
                self.add_move(col, next_checker)
            if next_checker == 'X':
                next_checker = 'O'
            else:
                next_checker = 'X'

    def allows_move(self, col):
        """Checks whether column col can be played"""
        return 0 <= col < self.width and self.data[0][col] == ' '

    def is_full(self):
        """Checks whether the board is full"""
        return all(not self.allows_move(col) for col in range(self.width))

    def del_move(self, col):
        """Removes a stone from column col"""
        i = 0
        while i < self.height and self.data[i][col] == ' ':
            i += 1
        if i < self.height:
            self.data[i][col] = ' '

    def wins_for(self, ox):
        """Checks whether player ox wins the game"""
        for y in range(self.height):
            for x in range(self.width):
                if in_a_row_n_east(ox, y, x, self.data, 4) or \
                        in_a_row_n_south(ox, y, x, self.data, 4) or \
                        in_a_row_n_southeast(ox, y, x, self.data, 4) or \
                        in_a_row_n_northeast(ox, y, x, self.data, 4):
                    return True
        return False

    def host_game(self):
        """Plays a game of Connect Four"""
        ox = 'O'
        while True:
            # druk het bord af
            print(self)

            # controleer of het spel afgelopen is
            if self.wins_for(ox):
                print(ox, 'heeft gewonnen!')
                break
            if self.is_full():
                print('Gelijkspel!')
                break

            # verander de huidige speler
            if ox == 'O':
                ox = 'X'
            else:
                ox = 'O'

            # laat de speler een kolom kiezen
            col = -1
            while not self.allows_move(col):
                col = int(input('Kolom voor '+ox+': '))

            # voer de zet uit
            self.add_move(col, ox)

    def tetris(self):
        """
        Checks if there is a full row on the board,
        clears it and adds a new clean row on the top.
        """
        if self.alt:
            if ' ' not in self.data[self.height-1]:
                tetrisPrint()
                self.data = [[' ']*self.width] + self.data[0:self.height-1]

    def play_game(self, px, po, show_scores=False):
        """
        Plays a game of Connect Four between players px and po.
        If show_scores is True, the player's board evaluations are printed each turn.
        """
        ox = 'O'
        while True:
            # druk het bord af
            print(self)

            # controleer of het spel afgelopen is
            if self.wins_for(ox):
                print(f'{ox} heeft gewonnen!')
                break
            if self.is_full():
                print('Gelijkspel!')
                break

            self.tetris()

            # verander de huidige speler
            if ox == 'O':
                ox = 'X'
                player = px
            else:
                ox = 'O'
                player = po

            if player == 'human':
                # laat de menselijke speler een kolom kiezen
                col = -1
                while not self.allows_move(col):
                    col = int(input('Kolom voor ' + ox + ': '))
            else:
                hash_dict.clear()
                # de computerspeler berekent een zet
                if show_scores:
                    scores = player.scores_for(self)
                    print('Scores voor ', ox, ':', [int(sc) for sc in scores])
                    col = player.tiebreak_move(scores)
                else:
                    col = player.next_move(self)

            # voer de zet uit
            self.add_move(col, ox)


class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type, and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply
        self.Cply = ply

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player: ox = " + self.ox + ", "
        s += "tbt = " + self.tbt + ", "
        s += "ply = " + str(self.ply)
        return s

    def opp_ch(self):
        """Deze functie geeft de vijandige speler terug"""
        return 'X' if self.ox == 'O' else 'O'

    def score_board(self, b):
        """Deze functie geeft een score terug van hoe goed de speler er voor staat
        100 is een win
        50 is gelijk voor beide speler
        0 is een verlies
        """
        if b.wins_for(self.ox):
            return 100.0
        if not b.wins_for(self.opp_ch()) and not b.wins_for(self.ox):
            return 50.0
        return 0.0

    def tiebreak_move(self, scores):
        """Chooses a column for a move during a tiebreaker,
        using the chosen direction given by the player.
        """
        max_indices = []
        ms = max(scores)
        for i, x in enumerate(scores):
            if x == ms:
                max_indices.append(i)

        if self.tbt == "RIGHT":
            return max_indices[-1]
        if self.tbt == "LEFT":
            return max_indices[0]
        return random.choice(max_indices)

    def scores_for(self, b):
        """Neemt een bord en kijkt naar wat de beste zet zal zijn voor een speler
        met de regels die al gedetermineerd waren voor de speler.
        """
        LString = str(b.data)

        x = hashlib.md5((LString + self.ox + str(self.ply)
                         ).encode('utf-8')).digest()

        if x in hash_dict:
            return hash_dict[x]

        scores = [50] * b.width

        for col in range(b.width):
            if not b.allows_move(col):
                scores[col] = -1
            elif b.wins_for(self.ox):
                scores[col] = 100
            elif b.wins_for(self.opp_ch()):
                scores[col] = 0
            elif self.ply == 0:
                scores[col] = 50
            else:
                b.add_move(col, self.ox)
                other_player = Player(
                    self.opp_ch(), self.tbt, self.ply-1)
                other_scores = other_player.scores_for(b)
                if max(other_scores) == 0:
                    scores[col] = 100
                elif max(other_scores) == 100:
                    scores[col] = 0
                elif max(other_scores) == 50:
                    scores[col] = 50
                b.del_move(col)

        hash_dict[x] = scores
        return scores

    def next_move(self, b):
        """Geeft de volgende zet terug"""
        return self.tiebreak_move(self.scores_for(b))


hash_dict = {}
p1 = Player('X', 'RANDOM', 4)
p2 = Player('O', 'RANDOM', 4)

state = input(
    'Wil je tegen een AI spelen of tegen een persoon? \
    \nDe default waarde bij niks invullen is AIvAI \
    \n[AI/Persoon/AIvAI]==>')
alt = input('Wil je het in tetris modes spelen? \n[Ja/Nee]==>')

bord = Board(7, 6)
bord.set_board('0152512542')

if alt in ['Ja', 'ja', 'JA', 'J', 'j', 'Y', 'y']:
    bord.alt = True

if state == 'AI':
    bord.play_game('human', p1)
elif state == 'Persoon':
    bord.play_game('human', 'human')
else:
    bord.play_game(p2, p1)
