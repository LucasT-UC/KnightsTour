import params

class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Reset to default color

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.view = "O"
        self.n_jumps = 0
        self.has_knight = False


    def prediction(self, n_jumps):
        self.view = f"{n_jumps}"
        self.n_jumps = n_jumps
        
    def arrived_knight(self):
        self.has_knight = True
        self.visited = True
        self.view = "K"
    
    def left_knight(self):
        self.has_knight = False
        self.view = "X"
        
    def reset(self):
        self.view = "O"


class Game:
    def __init__(self):
        self.size = (params.TABLE_SIZE, params.TABLE_SIZE)
        self.table = self.create_table()
        self.knight_x = params.STARTING_POSITION_X
        self.knight_y = params.STARTING_POSITION_Y

    def create_table(self):
        table = []
        for i in range(self.size[0]):
            line = []
            for j in range(self.size[1]):
                t = Tile(i, j)
                if i == params.STARTING_POSITION_X and j == params.STARTING_POSITION_Y:
                    t.arrived_knight()
                line.append(t)
            table.append(line)
        return table

    def show_table(self):
        for i in range(self.size[0]):
            to_show = "|"
            for j in range(self.size[1]):
                piece = self.table[i][j].view
                if piece == 'X':
                    to_show += f" {Color.RED}{piece}{Color.RESET} |"
                elif piece == 'O':
                    to_show += f" {Color.GREEN}{piece}{Color.RESET} |"
                elif piece == 'K':
                    to_show += f" {Color.BLUE}{piece}{Color.RESET} |"
                elif isinstance(piece, int):
                    to_show += f" {Color.YELLOW}{piece}{Color.RESET} |"
                else:
                    to_show += f" {piece} |"
            print(to_show)


    def retrieve_jumps(self, x, y):
        jumps = []  # List of tuples positions
        tile = self.table[x][y]
        
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.table[i][j].visited:
                    continue
                if (i == tile.x + 1) and (j == tile.y + 2 or j == tile.y - 2):
                    jumps.append((i, j))
                elif (i == tile.x - 1) and (j == tile.y + 2 or j == tile.y - 2):
                    jumps.append((i, j))
                elif (i == tile.x + 2) and (j == tile.y + 1 or j == tile.y - 1):
                    jumps.append((i, j))
                elif (i == tile.x - 2) and (j == tile.y + 1 or j == tile.y - 1):
                    jumps.append((i, j))

        return jumps




    def hamiltonian(self):
        ended = False
        n = 1
        while not ended:
            knight_jumps = self.retrieve_jumps(self.knight_x, self.knight_y)
            most_efficient = None
            efficient_tile = None
    
            for (x, y) in knight_jumps:
                jumps = self.retrieve_jumps(x, y)
                self.table[x][y].prediction(len(jumps))
    
                if most_efficient is None or len(jumps) < most_efficient:
                    most_efficient = len(jumps)
                    efficient_tile = self.table[x][y]
            
            if most_efficient is None:
                ended = True
                continue

            self.show_table()
            print("\n ---------------------------------------")
            
            for (x, y) in knight_jumps:
                self.table[x][y].reset()
            
            self.table[self.knight_x][self.knight_y].left_knight()
            efficient_tile.arrived_knight()
            self.knight_x = efficient_tile.x
            self.knight_y = efficient_tile.y
            n += 1
        
        self.show_table()
        print(f"Number of knight jumps: {n}")
    

def main():
    game = Game()
    game.hamiltonian()


if __name__ == '__main__':
    main()
