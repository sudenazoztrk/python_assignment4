import sys
def get_input(input_file):
    # Get inputs from input file and categorize into numbers and letters.
    # The first four lines contain numbers, and the subsequent lines contain letters.
    number_list = []
    domino_list = []
    counter = 0
    for line in input_file:
        if counter < 4:
            lines = list(map(str, line.split()))
            number_list.append(lines)
            counter += 1
        else:
            lines2 = list(map(str, line.split()))
            domino_list.append(lines2)

    # Creates a full null board to fill with H-B
    board = [domino_list[0].copy() for row in range(len(domino_list))]
    for row in range(len(board)):
        for col in range(len(board[0])):
            board[row][col] = "0"

    return number_list,domino_list,board
def neighbour_control(number_list,domino_list,board,row,col,i,j):
    # Check adjacent cells to avoid placing H-B next to each other.
    # 'i' and 'j' represents the current domino that we check before placing.
    # Returns True if placement is valid, False otherwise.

    if i == "N":
        return True
    elif domino_list[row][col] == "L":
        if 0 <= row - 1 < len(board) and i == board[row-1][col]: #Up control for L cell
            return False
        if 0 <= row + 1 < len(board) and i == board[row + 1][col]:  # Down control for L cell
            return False
        if 0 <= col + 1 < len(board[0]) and i == board[row][col + 1]:  # Right control for L cell
            return False
        if 0 <= col - 1 < len(board[0]) and i == board[row][col - 1]:  # Left control for L cell
            return False
        if 0<= row - 1 < len(board) and j == board[row-1][col+1]: #Up control for R cell
            return False
        if 0 <= row + 1 < len(board) and j == board[row + 1][col+1]:  # Down control for R cell
            return False
        if 0 <= col + 2 < len(board[0]) and j == board[row][col + 2]:  # Right control for  R cell
            return False
        if 0 <= col  < len(board[0]) and j == board[row][col]:  # Left control for R cell
            return False
        return True
    elif domino_list[row][col] == "U":
        if 0 <= row - 1 < len(board) and i == board[row-1][col]: #Up control for U cell
            return False
        if 0 <= row + 1 < len(board) and i == board[row + 1][col]:  # Down control for U cell
            return False
        if 0 <= col + 1 < len(board[0]) and i == board[row][col + 1]:  # Right control for U cell
            return False
        if 0 <= col - 1 < len(board[0]) and i == board[row][col - 1]:  # Left control for U cell
            return False
        if 0<= row < len(board) and j == board[row][col]: #Up control for D cell
            return False
        if 0 <= row + 2 < len(board) and j == board[row + 2][col]:  # Down control for D cell
            return False
        if 0 <= col + 1 < len(board[0]) and j == board[row+1][col + 1]:  # Right control for D cell
            return False
        if 0 <= col - 1 < len(board[0]) and j == board[row+1][col - 1]:  # Left control for D cell
            return False
        return True
def constraint_control(number_list, board):
    # Constraints include the number of H and B in each row and column.
    # The function checks the compatibility between the constraints and the table

    # High row check
    def high_row_check(board):
        for i in range(len(board)):
            counter = 0
            for cell in board[i]:
                if cell == "H":
                    counter += 1
            if number_list[0][i] != "-1" and int(number_list[0][i]) != counter:
                return False
        return True

    # High column check
    def high_col_check(board):
        for i in range(len(board[0])):
            counter = 0
            for j in range(len(board)):
                if board[j][i] == "H":
                    counter += 1
            if number_list[2][i] != "-1" and int(number_list[2][i]) != counter:
                return False
        return True

    # Base row check
    def base_row_check(board):
        for i in range(len(board)):
            counter = 0
            for cell in board[i]:
                if cell == "B":
                    counter += 1
            if number_list[1][i] != "-1" and int(number_list[1][i]) != counter:
                return False
        return True

    # Base column check
    def base_col_check(board):
        for i in range(len(board[0])):
            counter = 0
            for j in range(len(board)):
                if board[j][i] == "B":
                    counter += 1
            if number_list[3][i] != "-1" and int(number_list[3][i]) != counter:
                return False
        return True

    return high_row_check(board) and high_col_check(board) and base_row_check(board) and base_col_check(board)
def solve(number_list, domino_list, board,row,col):
    # Recursive function to solve the board by using backtracking
    # Returns True if a solution is found, False otherwise

    # Base case
    if all('0' not in row for row in board):
        if constraint_control(number_list, board):
            return True
        else:
            return False

    if row >= len(board):
        return False

    if board[row][col] != "0":
        new_row, new_col = row, col+ 1
        if col + 2 > len(board[0]) - 1:
            new_row,new_col = row + 1, 0
        return solve(number_list,domino_list,board,new_row,new_col)


    high_base_list=[("H","B"),("B","H"),("N","N")]

    if board[row][col] == "0":
        if domino_list[row][col] == "L":
            for i, j in high_base_list:
                if neighbour_control(number_list, domino_list, board, row, col, i, j):
                    board[row][col], board[row][col + 1] = i, j
                    new_row,new_col = row, col + 2
                    if col + 2 > len(board[0]) - 1:
                        new_row, new_col = row + 1, 0

                    if solve(number_list, domino_list, board,new_row,new_col):
                        return True
                    board[row][col], board[row][col + 1] = "0", "0"


        elif domino_list[row][col] == "U":
            for i, j in high_base_list:
                if neighbour_control(number_list, domino_list, board, row, col, i, j):
                    board[row][col],board[row + 1][col] = i,j

                    new_row, new_col = row, col + 1

                    if col + 1 > len(board[0])-1:
                        new_row, new_col = row + 1, 0

                    if solve(number_list, domino_list, board,new_row,new_col):
                        return True
                    board[row][col], board[row + 1][col] = "0", "0"

    return False
def print_output(number_list,domino_list,board,output_file):
    # Write the final board state to an output file.
    # If a solution is found, prints the board; otherwise, prints "No solution!".

    if solve(number_list,domino_list,board,0,0):
        for row in board:
            for item in row:
                output_file.write(item + " ")
            output_file.write('\n')
    else:
        output_file.write("No solution!")

def main():
    input_file = open(sys.argv[1],'r')
    output_file = open(sys.argv[2],'w')
    number_list, domino_list, board = get_input(input_file)
    print_output(number_list,domino_list,board, output_file)

if __name__ == "__main__":
    main()
