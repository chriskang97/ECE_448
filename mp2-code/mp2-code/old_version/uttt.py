from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

        self.move = (0,0)

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        # Offensive Player
        # 1st Rule: 3 in a row = 10000
        # 2nd Rule: For each local board, count the number of two-in-a-row without the third spot taken by the opposing player (unblocked two-in-a-row).
        # For each unblocked two-in-a-row, increment the utility score by 500. For each local board, count the number of places in which you have prevented the
        # opponent player forming two-in-a-row (two-in-a-row of opponent player but with the third spot taken by offensive agent).
        # For each prevention, increment the utility score by 100.
        # 3rd rule: For each corner taken by the offensive agent, increment the utility score by 30.

        score=0
        current_board = self.globalIdx[self.startBoardIdx]


        local = self.board


        if ( isMax ) :
            sign = 1
            char = self.maxPlayer
            opp_char = self.minPlayer
        else :
            sign = -1
            char = self.minPlayer
            opp_char = self.maxPlayer

        # First Rule Condition

        row = current_board[0]
        col = current_board[1]

        move_row = self.move[0]
        move_col = self.move[1]

        local[move_row][move_col] = char

        # Diagonal can only be at (0,0) (0,2) (1,1) (2,0) (2,2)
        # Check only the same Column and Row
        diag_1 = []
        diag_2 = []

        diag_1.extend( (local[row][col], local[row+1][col+1], local[row+2][col+2]) )
        diag_2.extend( (local[row][col+2], local[row+1][col+1], local[row+2][col]) )


        ## Rule #1 : 3 in a row = You Win
        # Checking for Row/Cols Victories
        if ( [local[i][move_col] for i in range(row,row+3)]  == [char,char,char] or local[move_row][col:col+3] == [char,char,char] ) :
            return sign * 10000

        # Checking for Diagonal Victories
        elif ( diag_1 == [char, char, char] or diag_2 == [char, char, char] ) :
            return sign * 10000

        ## Rule #2 : Checking for Next Win
        num_char_col = sum( indiv == char for indiv in [ local[i][move_col] for i in range(row,row+3) ]  )
        num_char_row = sum( indiv == char for indiv in local[move_row][col:col+3]  )
        num_char_diag_1 = sum( indiv == char for indiv in diag_1 )
        num_char_diag_2 = sum( indiv == char for indiv in diag_2 )

        # Checking Potential Win Positions
        if ( num_char_col == 2 and '_' in [ local[i][move_col] for i in range(row, row+3)] ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_row == 2 and '_' in local[move_row][col:col+3] ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_diag_1 == 2 and '_' in diag_1 ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_diag_2 == 2 and '_' in diag_2 ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        # Checking if Blocked
        num_char_col = sum( indiv == opp_char for indiv in [local[i][move_col] for i in range(row, row+3)]  )
        num_char_row = sum( indiv == opp_char for indiv in local[move_row][col:col+3]  )
        num_char_diag_1 = sum( indiv == opp_char for indiv in diag_1 )
        num_char_diag_2 = sum( indiv == opp_char for indiv in diag_2 )

        # Checking Potential Win Positions
        if ( num_char_col == 2 and char in [ local[i][move_col] for i in range(row, row+3)] ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_row == 2 and char in local[move_row][col:col+3] ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_diag_1 == 2 and char in diag_1 ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_diag_2 == 2 and char in diag_2 ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        for tic_tac_toe in range (9) :
            local_ttt = self.globalIdx[tic_tac_toe]

            if ( local_ttt == current_board ) :
                continue

            row = local_ttt[0]
            col = local_ttt[1]
            diag_1 = []
            diag_2 = []

            diag_1.extend( (local[row][col], local[row+1][col+1], local[row+2][col+2]) )
            diag_2.extend( (local[row][col+2], local[row+1][col+1], local[row+2][col]) )

            num_char_col =   sum( indiv == char for indiv in [local[i][col]   for i in range(row, row+3)] )
            num_char_col_2 = sum( indiv == char for indiv in [local[i][col+1] for i in range(row, row+3)] )
            num_char_col_3 = sum( indiv == char for indiv in [local[i][col+2] for i in range(row, row+3)] )

            num_char_row = sum( indiv == char for indiv in local[row][col:col+3]  )
            num_char_row_2 = sum( indiv == char for indiv in local[row+1][col:col+3]  )
            num_char_row_3 = sum( indiv == char for indiv in local[row+2][col:col+3]  )

            num_char_diag_1 = sum( indiv == char for indiv in diag_1 )
            num_char_diag_2 = sum( indiv == char for indiv in diag_2 )

            # Checking all 3 Potential Wins for Columns
            if ( num_char_col == 2 and '_' in [local[i][col] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_col_2 == 2 and '_' in [local[i][col+1] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_col_3 == 2 and '_' in [local[i][col+2] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checking all 3 Potential Wins for Rows
            if ( num_char_row == 2 and '_' in local[row][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_row_2 == 2 and '_' in local[row+1][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_row_2 == 2 and '_' in local[row+2][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checkin all 2 Potential Wins for Diagonals
            if ( num_char_diag_1 == 2 and '_' in diag_1 ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_diag_2 == 2 and '_' in diag_2 ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checking if Blocked
            num_char_col   = sum( indiv == opp_char for indiv in [local[i][col]   for i in range(row, row+3)]  )
            num_char_col_2 = sum( indiv == opp_char for indiv in [local[i][col+1] for i in range(row, row+3)]  )
            num_char_col_3 = sum( indiv == opp_char for indiv in [local[i][col+2] for i in range(row, row+3)]  )

            num_char_row = sum( indiv == opp_char for indiv in local[row][col:col+3]  )
            num_char_row_2 = sum( indiv == opp_char for indiv in local[row+1][col:col+3]  )
            num_char_row_3 = sum( indiv == opp_char for indiv in local[row+2][col:col+3]  )

            num_char_diag_1 = sum( indiv == opp_char for indiv in diag_1 )
            num_char_diag_2 = sum( indiv == opp_char for indiv in diag_2 )

            # Checking Potential Blocked Position for Columns
            if ( num_char_col == 2 and char in [local[i][col] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_col_2 == 2 and char in [local[i][col+1] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_col_3 == 2 and char in [local[i][col+2] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            # Checking Potential Blocked Position for Rows
            if ( num_char_row == 2 and char in local[row][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_row_2 == 2 and char in local[row+1][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_row_3 == 2 and char in local[row+2][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            # Checking Potential Blocked Position for Diag
            if ( num_char_diag_1 == 2 and char in diag_1 ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_diag_2 == 2 and char in diag_2 ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

        if ( score != 0 ) :
            return score

         ## Rule 3
        for tic_tac_toe in range (9) :
            local_ttt = self.globalIdx[tic_tac_toe]

            row = local_ttt[0]
            col = local_ttt[1]

            corner_1 = local[row][col]
            corner_2 = local[row][col+2]
            corner_3 = local[row+2][col]
            corner_4 = local[row+2][col+2]

            corners = []
            corners.extend( (corner_1, corner_2, corner_3, corner_4) )

            multiplier = sum( indiv == char for indiv in corners  )
            score += sign * multiplier * 30

        return score


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE

        # If we end up having a move that causes the other play to win and we choose based on some random decision, we should
        # prevent that from happening.

        score=0
        current_board = self.globalIdx[self.startBoardIdx]


        local = self.board


        if ( isMax ) :
            sign = 1
            char = self.maxPlayer
            opp_char = self.minPlayer
        else :
            sign = -1
            char = self.minPlayer
            opp_char = self.maxPlayer

        # First Rule Condition

        row = current_board[0]
        col = current_board[1]

        move_row = self.move[0]
        move_col = self.move[1]

        local[move_row][move_col] = char

        # Diagonal can only be at (0,0) (0,2) (1,1) (2,0) (2,2)
        # Check only the same Column and Row
        diag_1 = []
        diag_2 = []

        diag_1.extend( (local[row][col], local[row+1][col+1], local[row+2][col+2]) )
        diag_2.extend( (local[row][col+2], local[row+1][col+1], local[row+2][col]) )


        ## Rule #1 : 3 in a row = You Win
        # Checking for Row/Cols Victories
        if ( [local[i][move_col] for i in range(row,row+3)]  == [char,char,char] or local[move_row][col:col+3] == [char,char,char] ) :
            return sign * 10000

        # Checking for Diagonal Victories
        elif ( diag_1 == [char, char, char] or diag_2 == [char, char, char] ) :
            return sign * 10000

        ## Rule #2 : Checking for Next Win
        num_char_col = sum( indiv == char for indiv in [ local[i][move_col] for i in range(row,row+3) ]  )
        num_char_row = sum( indiv == char for indiv in local[move_row][col:col+3]  )
        num_char_diag_1 = sum( indiv == char for indiv in diag_1 )
        num_char_diag_2 = sum( indiv == char for indiv in diag_2 )

        # Checking Potential Win Positions
        if ( num_char_col == 2 and '_' in [ local[i][move_col] for i in range(row, row+3)] ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_row == 2 and '_' in local[move_row][col:col+3] ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_diag_1 == 2 and '_' in diag_1 ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        if ( num_char_diag_2 == 2 and '_' in diag_2 ) :
            if (isMax):
                score += sign * 500
            else:
                score += sign * 100

        # Checking if Blocked
        num_char_col = sum( indiv == opp_char for indiv in [local[i][move_col] for i in range(row, row+3)]  )
        num_char_row = sum( indiv == opp_char for indiv in local[move_row][col:col+3]  )
        num_char_diag_1 = sum( indiv == opp_char for indiv in diag_1 )
        num_char_diag_2 = sum( indiv == opp_char for indiv in diag_2 )

        # Checking Potential Win Positions
        if ( num_char_col == 2 and char in [ local[i][move_col] for i in range(row, row+3)] ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_row == 2 and char in local[move_row][col:col+3] ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_diag_1 == 2 and char in diag_1 ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        if ( num_char_diag_2 == 2 and char in diag_2 ) :
            if (isMax):
                score += sign * 100
            else:
                score += sign * 500

        for tic_tac_toe in range (9) :
            local_ttt = self.globalIdx[tic_tac_toe]

            if ( local_ttt == current_board ) :
                continue

            row = local_ttt[0]
            col = local_ttt[1]
            diag_1 = []
            diag_2 = []

            diag_1.extend( (local[row][col], local[row+1][col+1], local[row+2][col+2]) )
            diag_2.extend( (local[row][col+2], local[row+1][col+1], local[row+2][col]) )

            num_char_col =   sum( indiv == char for indiv in [local[i][col]   for i in range(row, row+3)] )
            num_char_col_2 = sum( indiv == char for indiv in [local[i][col+1] for i in range(row, row+3)] )
            num_char_col_3 = sum( indiv == char for indiv in [local[i][col+2] for i in range(row, row+3)] )

            num_char_row = sum( indiv == char for indiv in local[row][col:col+3]  )
            num_char_row_2 = sum( indiv == char for indiv in local[row+1][col:col+3]  )
            num_char_row_3 = sum( indiv == char for indiv in local[row+2][col:col+3]  )

            num_char_diag_1 = sum( indiv == char for indiv in diag_1 )
            num_char_diag_2 = sum( indiv == char for indiv in diag_2 )

            # Checking all 3 Potential Wins for Columns
            if ( num_char_col == 2 and '_' in [local[i][col] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_col_2 == 2 and '_' in [local[i][col+1] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_col_3 == 2 and '_' in [local[i][col+2] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checking all 3 Potential Wins for Rows
            if ( num_char_row == 2 and '_' in local[row][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_row_2 == 2 and '_' in local[row+1][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_row_2 == 2 and '_' in local[row+2][col:col+3] ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checkin all 2 Potential Wins for Diagonals
            if ( num_char_diag_1 == 2 and '_' in diag_1 ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            if ( num_char_diag_2 == 2 and '_' in diag_2 ) :
                if (isMax):
                    score += sign * 500
                else:
                    score += sign * 100

            # Checking if Blocked
            num_char_col   = sum( indiv == opp_char for indiv in [local[i][col]   for i in range(row, row+3)]  )
            num_char_col_2 = sum( indiv == opp_char for indiv in [local[i][col+1] for i in range(row, row+3)]  )
            num_char_col_3 = sum( indiv == opp_char for indiv in [local[i][col+2] for i in range(row, row+3)]  )

            num_char_row = sum( indiv == opp_char for indiv in local[row][col:col+3]  )
            num_char_row_2 = sum( indiv == opp_char for indiv in local[row+1][col:col+3]  )
            num_char_row_3 = sum( indiv == opp_char for indiv in local[row+2][col:col+3]  )

            num_char_diag_1 = sum( indiv == opp_char for indiv in diag_1 )
            num_char_diag_2 = sum( indiv == opp_char for indiv in diag_2 )

            # Checking Potential Blocked Position for Columns
            if ( num_char_col == 2 and char in [local[i][col] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_col_2 == 2 and char in [local[i][col+1] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_col_3 == 2 and char in [local[i][col+2] for i in range(row, row+3)] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            # Checking Potential Blocked Position for Rows
            if ( num_char_row == 2 and char in local[row][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_row_2 == 2 and char in local[row+1][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_row_3 == 2 and char in local[row+2][col:col+3] ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            # Checking Potential Blocked Position for Diag
            if ( num_char_diag_1 == 2 and char in diag_1 ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

            if ( num_char_diag_2 == 2 and char in diag_2 ) :
                if (isMax):
                    score += sign * 100
                else:
                    score += sign * 500

        if ( score != 0 ) :
            return score

         ## Rule 3
        for tic_tac_toe in range (9) :
            local_ttt = self.globalIdx[tic_tac_toe]

            row = local_ttt[0]
            col = local_ttt[1]

            corner_1 = local[row][col]
            corner_2 = local[row][col+2]
            corner_3 = local[row+2][col]
            corner_4 = local[row+2][col+2]

            corners = []
            corners.extend( (corner_1, corner_2, corner_3, corner_4) )

            multiplier = sum( indiv == char for indiv in corners  )
            score += sign * multiplier * 30

        next_board_index = 3 * (move_row % 3) + (move_col % 3)
        current_board = self.globalIdx[next_board_index]
        check_row = current_board[0]
        check_col = current_board[1]

        check_diag_1 = []
        check_diag_2 = []

        check_diag_1.extend( (local[check_row][check_col], local[check_row+1][check_col+1], local[check_row+2][check_col+2]) )
        check_diag_2.extend( (local[check_row][check_col+2], local[check_row+1][check_col+1], local[check_row+2][check_col]) )

        check_num_char_col = sum( indiv == opp_char for indiv in [local[i][check_col] for i in range(check_row, check_row+3)]  )
        check_num_char_row = sum( indiv == opp_char for indiv in local[check_row][check_col:check_col+3]  )
        check_num_char_diag_1 = sum( indiv == opp_char for indiv in check_diag_1 )
        check_num_char_diag_2 = sum( indiv == opp_char for indiv in check_diag_2 )

        if ( check_num_char_col == 2 and '_' in [ local[i][check_col] for i in range(check_row, check_row+3)] ) :
            score += sign * -5000


        if ( check_num_char_row == 2 and '_' in local[check_row][check_col:check_col+3] ) :
            score += sign * -5000


        if (check_ num_char_diag_1 == 2 and '_' in check_diag_1 ) :
            score += sign * -5000


        if ( check_num_char_diag_2 == 2 and '_' in check_diag_2 ) :
            score += sign * -5000

        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        current_index = self.startBoardIdx
        current_tile = self.globalIdx[current_index]

        row_index = current_tile[0]
        column_index = current_tile[1]


        if ( '_' in [self.board[i][column_index:column_index+3 ] for i in range(row_index, row_index+3)] ) :
            movesLeft = False
        else :
            movesLeft=True

        return movesLeft

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        current_index = self.startBoardIdx
        current_tile = self.globalIdx[current_index]

        row_index = current_tile[0]
        column_index = current_tile[1]

        winner=0

        #print([self.board[i][column_index:column_index+3] for i in range (row_index,row_index+3)] )

        # HORIZONTAL CASE
        for i in range(3) :
            horizontal = self.board[row_index + i][column_index:column_index+3]

            if ( horizontal[0] == horizontal[1] == horizontal[2] and horizontal[0] != '_') :
                if ( horizontal[0] == self.maxPlayer ) :
                    return 1
                else :
                    return -1

        # VERTICAL CASE
        for i in range(3) :
            vertical = [self.board[row][column_index + i] for row in range (row_index, row_index+3) ]

            if ( vertical[0] == vertical[1] == vertical[2] and vertical[0] != '_' ) :
                if ( vertical[0] == self.maxPlayer ) :
                    return 1
                else :
                    return -1

        # DIAGONAL CASE
        diagonal_1 = []
        # diagonal_1.append( self.board[row_index][column_index] )
        # diagonal_1.append( self.board[row_index+1][column_index+1])
        # diagonal_1.append( self.board[row_index+2][column_index+2])
        diagonal_1.extend((self.board[row_index][column_index],self.board[row_index+1][column_index+1], self.board[row_index+2][column_index+2]))

        diagonal_2 = []
        diagonal_2.extend((self.board[row_index][column_index+2],self.board[row_index+1][column_index+1], self.board[row_index+2][column_index]))
        # diagonal_2.append( self.board[row_index][column_index+2] )
        # diagonal_2.append( self.board[row_index+1][column_index+1])
        # diagonal_2.append( self.board[row_index+2][column_index])

        # First Diagonal Check
        if ( diagonal_1[0] == diagonal_1[1] == diagonal_1[2] and  diagonal_1[0] != '_') :
            if ( diagonal_1[0] == self.maxPlayer ) :
                return 1
            else :
                return -1

        # Second Diagonal Check
        if ( diagonal_2[0] == diagonal_2[1] == diagonal_2[2] and  diagonal_2[0] != '_') :
            if ( diagonal_2[0] == self.maxPlayer ) :
                return 1
            else :
                return -1

        return 0

#### ADDED FUNCTION HERE #######################################################
    def compute_move(self, char, isMax, temp, current_index, path_row, path_col ) :
        # Given a specific tile within a specific tie, calculates the utility score and
        # sets the next position.
        # Returns: New Updated Board and Updated Utility Score

        score = 0
        current_tile = self.globalIdx[current_index]
        row_index = current_tile[0]
        column_index = current_tile[1]

        local = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        for i in range (9) :
            for j in range (9) :
                local[i][j] = temp[i][j]



        if ( local[row_index + path_row][column_index + path_col] == '_' ) :
            self.move = (row_index + path_row, column_index + path_col )
            local[row_index + path_row][column_index + path_col] = char


            self.startBoardIdx = current_index
            self.board = local
            score = self.evaluatePredifined(isMax)

            current_index = 3 * (self.move[0] % 3) + (self.move[1] % 3 )
            self.startBoardIdx = current_index


        return local, score


################################################################################

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        bestValue=0.0
        local = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        board_1 = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        board_2 = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        # COPYING VALUES TO BOARD
        for i in range (9) :
            for j in range (9) :
                local[i][j] = self.board[i][j]

        # Initialize Variables
        current_index = self.startBoardIdx
        original_index = self.startBoardIdx
        best_move = (0,0)
        best_move_2 = (0,0)
        best_move_3 = (0,0)

        if ( isMax ) :
            char = self.maxPlayer
            char_2 = self.minPlayer
        else :
            char = self.minPlayer
            char_2 = self.maxPlayer

        # Looking 3 Moves Ahead Procedures
        # 1) Obtain Current Tile Location
        # 2) See if there are any given moves to take
        # 3) Store local board into self and obtain score


        ### OBSERVING FIRST MOVE NOW ###########################################
        ########################################################################
        for path_1_row in range (3) :
            for path_1_col in range (3) :

                current_index = original_index
                local_1, score_1 = self.compute_move(char, isMax, list(local), current_index, path_1_row, path_1_col )

                # print(score_1)
                # print("ROW ", path_1_row)
                # print("COL ", path_1_col)
                if isMax :
                    if score_1 > alpha :
                        alpha = score_1
                        best_move = self.move
                else :
                    if score_1 < beta :
                        beta = score_1
                        best_move = self.move


        # COPYING VALUES TO BOARD
        for i in range (9) :
            for j in range (9) :
                board_1[i][j] = local[i][j]

        board_1[best_move[0]][best_move[1] ] = char
        # print(current_index)
        ### OBSERVING SECOND MOVE NOW ##########################################
        ########################################################################
        if  depth >= 1 :

            for path_2_row in range (3) :
                for path_2_col in range (3) :

                    current_index_2 =  3 * (best_move[0] % 3) + (best_move[1] % 3 )
                    local_2, score_2 = self.compute_move(char, not isMax, list(board_1), current_index_2, path_2_row, path_2_col )


                    if isMax :
                        if score_2 < beta :
                            beta = score_2
                            best_move_2 = self.move
                    else :
                        if score_1 > alpha :
                            alpha = score_2
                            best_move_2 = self.move

        # COPYING VALUES TO BOARD
        for i in range (9) :
            for j in range (9) :
                board_2[i][j] = board_1[i][j]

        board_2[best_move_2[0]][best_move_2[1]] = char_2
        print(current_index_2)
        ### OBSERVING THIRD MOVE NOW ###########################################
        ########################################################################

        best_score_3 = 0 ;

        if depth >= 2  :

            for path_3_row in range (3) :
                for path_3_col in range (3) :

                    current_index_3 = 3 * (best_move_2[0] % 3) + (best_move_2[1] % 3 )
                    local_3, score_3 = self.compute_move(char, isMax, list(board_2), current_index_3, path_3_row, path_3_col )

                    if abs(score_3) > abs(best_score_3) :
                        best_score_3 = score_3
                        best_move_3 = self.move


        print(alpha)
        print(beta)
        print(best_score_3)
        if isMax :
            bestValue = best_score_3 + alpha
        else :
            bestValue = best_score_3 + beta

        # Reset to original state of board
        self.board = local
        self.startBoardIdx = original_index
        self.move = best_move

        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        # Dict: Key = (Path1, Path2, Path3)
        #       Value = (Utility Value)

        bestValue=0.0

        local = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        # COPYING VALUES TO BOARD
        for i in range (9) :
            for j in range (9) :
                local[i][j] = self.board[i][j]

        # Initialize Variables
        current_index = self.startBoardIdx
        original_index = self.startBoardIdx
        best_move = (0,0) ;

        if ( isMax ) :
            char = self.maxPlayer
        else :
            char = self.minPlayer

        # Looking 3 Moves Ahead Procedures
        # 1) Obtain Current Tile Location
        # 2) See if there are any given moves to take
        # 3) Store local board into self and obtain score


        ### OBSERVING FIRST MOVE NOW ###########################################
        ########################################################################
        for path_1_row in range (3) :
            for path_1_col in range (3) :

                score_1 = 0
                score_2 = 0
                score_3 = 0

                last_utility = []

                current_index = self.startBoardIdx
                local_1, score_1 = self.compute_move(char, isMax, list(local), current_index, path_1_row, path_1_col )

        ### OBSERVING SECOND MOVE NOW ##########################################
        ########################################################################
                if score_1 != 0 and depth >= 1 :
                    for path_2_row in range (3) :
                        for path_2_col in range (3) :

                            current_index_2 = self.startBoardIdx
                            local_2, score_2 = self.compute_move(char, not isMax, list(local_1), current_index_2, path_2_row, path_2_col )

        ### OBSERVING THIRD MOVE NOW ###########################################
        ########################################################################
                            if score_2 != 0 and depth >= 2 :
                                for path_3_row in range (3) :
                                    for path_3_col in range (3) :

                                        current_index_3 = self.startBoardIdx
                                        local_3, score_3 = self.compute_move(char, isMax, list(local_2), current_index_3, path_3_row, path_3_col )


                # Reset to original state of board
                self.board = local
                self.startBoardIdx = original_index

                # Calculate Utility Score
                new_score = score_1 + score_3

                # Determine if move was best move so far
                if (abs(new_score) > abs(bestValue) ) :
                    bestValue = new_score
                    best_move = (self.globalIdx[current_index][0] + path_1_row, self.globalIdx[current_index][1]  + path_1_col )


        self.move = best_move
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes = 0

        # HOW THE GAME WILL BE PLAYED OUT
        # 1) Check Valid Moves
        # 2) Call out algorithm for that player and pick move
        # 3) Update Board
        # 4) Check Winner
        # 5) Hand Off

        # Current Player Indicates whether its MaxPlayer or MinPlayer turn.
        if maxFirst :
            current_player = 1 # MaxPlayer
        else :
            current_player = 0 # MinPlayer

        curr_board = self.board

        while self.checkMovesLeft() :

            currBoardIdx = self.startBoardIdx

            # Check Algorithm
            if current_player == 1 and isMinimaxOffensive :
                score_move = self.minimax(3, currBoardIdx, current_player )
            elif current_player == 1 and not isMinimaxOffensive :
                score_move = self.alphabeta(3,currBoardIdx,-999,999,current_player )

            elif current_player == 0 and isMinimaxDefensive :
                score_move = self.minimax(3, currBoardIdx, current_player )
            elif current_player == 0 and not isMinimaxDefensive:
                score_move = self.alphabeta(3,currBoardIdx,-999,999,current_player )

            # Make Move and Update Score
            if current_player :
                curr_board[self.move[0]] [self.move[1]] = 'X'
            else :
                curr_board[self.move[0]] [self.move[1]] = 'O'


            bestMove.append(self.move)
            bestValue.append(score_move)
            gameBoards.append(curr_board)

            # Update Board to be Current Played Board
            self.board = curr_board
            self.printGameBoard()

            # Checks for Winner
            winner = self.checkWinner()

            if winner != 0 :
                return gameBoards, bestMove, expandedNodes, bestValue, winner


            # Passes off to Next Player
            self.startBoardIdx = 3 * (self.move[0] % 3 ) + (self.move[1] % 3)
            current_player = not current_player

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        # Current Player Indicates whether its MaxPlayer or MinPlayer turn.

        current_player = 1 # MaxPlayer


        curr_board = self.board

        while self.checkMovesLeft() :

            currBoardIdx = self.startBoardIdx

            # Check Algorithm
            if current_player == 1 :
                score_move = self.alphabeta(3,currBoardIdx,-999,999,current_player )

            elif current_player == 0  :
                score_move = self.alphabeta(3,currBoardIdx,-999,999,current_player )

            # Make Move and Update Score
            if current_player :
                curr_board[self.move[0]] [self.move[1]] = 'X'
            else :
                curr_board[self.move[0]] [self.move[1]] = 'O'


            bestMove.append(self.move)
            bestValue.append(score_move)
            gameBoards.append(curr_board)

            # Update Board to be Current Played Board
            self.board = curr_board
            self.printGameBoard()

            # Checks for Winner
            winner = self.checkWinner()

            if winner != 0 :
                return gameBoards, bestMove, expandedNodes, bestValue, winner


            # Passes off to Next Player
            self.startBoardIdx = 3 * (self.move[0] % 3 ) + (self.move[1] % 3)
            current_player = not current_player
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
