import sys
import os
import argparse
import random


class TicTacToe:
    def __init__(self):
        self.board = ['', '(1)', '(2)', '(3)',
                      '(4)', '(5)', '(6)', '(7)', '(8)', '(9)']
        self.player_turn_list = []  # players symbol
        self.player_registry = []  # {'player': playername, 'symb': 0}
        self.players_combinations = {'player1': [], 'player2': []}
        self.win_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [3, 6, 9], [2, 5, 8],
            [1, 5, 9], [3, 5, 7]
        ]

    def score_board(self):
        # fetch data from scores file and display it when <--scoreboard> args give
        try:
            with open('scores.txt', 'r') as f:
                for line in f.readlines():
                    print(line+'\n')
        except FileNotFoundError:
            print('file not fount')
        except Exception as e:
            print(e)

    def save_result(self, round, winner):
        try:
            with open('scores.txt', 'a+') as f:
                f.write('\n round '+str(round)+' - winner: '+winner)
        except FileNotFoundError:
            print('file not fount')
        except Exception as e:
            print(e)

    def game_round(self):
        # get the number of the last game round added to the file
        # check if file is empty
        if os.stat('scores.txt').st_size == 0:
            return '1'
        else:
            try:
                with open('scores.txt', 'r') as f:
                    last_lines = f.readlines()[-1].split('-')

                    round_number = int(last_lines[0].strip().split(' ')[1]) + 1

                    return round_number
            except FileNotFoundError:
                print('file not fount')
            except Exception:
                print('cannot save score, something went wrong')

    def reinitialize_board(self):
        self.player_turn_list = []
        self.player_registry = []
        self.players_combinations = {'player1': [], 'player2': []}
        self.board = self.board = ['', '(1)', '(2)', '(3)',
                                   '(4)', '(5)', '(6)', '(7)', '(8)', '(9)']

    def print_board(self):
        print("\n")
        print("{}  |  {}  |  {} ".format(
            self.board[1], self.board[2], self.board[3]))
        print("---------------------")
        print("{}  |  {}  |  {} ".format(
            self.board[4], self.board[5], self.board[6]))
        print("---------------------")
        print("{}  |  {}  |  {} ".format(
            self.board[7], self.board[8], self.board[9]))

    def register_player(self, player, symb):
        """add the players data

        Args:
            player (str): [player name]
            symb (str): [player chosen symbol]

        Returns:
            [bool/void]: [return false if more than 2 player is added]
        """
        if len(self.player_registry) <= 2:
            self.player_registry.append({'player': player, 'symb': symb})
        else:
            return False

    def get_player(self, resultkey, key, value):
        """loop through players list dictionary and return player data base on dict key given

        Args:
            resultkey (str): [dictionary key to get data from (player/symb)]
            key (str): [dict key use in condition]
            value (str): [value to compare to in condition]

        Returns:
            [dict]: [dictionnary of data wanted]
        """
        return next((data[resultkey] for data in self.player_registry if data[key] == value), None)

    def turn_of(self):
        # return the next player to play data (name, symbol, a message printing which player turn it is)
        if len(self.player_turn_list) == 0:
            return {'symb':  self.get_player("symb", "player", "player1"), 'msg': f'player1 => {self.get_player("symb", "player", "player1")}', 'player': 'player1'}

        last_player_name = self.get_player(
            'player', 'symb', self.player_turn_list[-1])
        if last_player_name == 'player1':
            return {'symb':  self.get_player("symb", "player", "player2"), 'msg': f'player2 => {self.get_player("symb", "player", "player2")}', 'player': 'player2'}
        else:
            return {'symb':  self.get_player("symb", "player", "player1"), 'msg': f'player1 => {self.get_player("symb", "player", "player1")}', 'player': 'player1'}

    def manage_player_turns(self, player):
        # add player data after each round to determine who is the next player
        self.player_turn_list.append(player)

    def game_finish(self):
        # status of game, after 9 rounds game end
        return len(self.player_turn_list) == 9

    def update_board(self, index, current_player):
        """update the game board list after each round base on 
        list key who represent position in game

        Args:
            index (int): [board list index]
            current_player (str): [player symbol]
        """
        if index not in self.players_combinations['player1'] or index not in self.players_combinations['player2']:
            self.board[index] = current_player
        else:
            print('position already take')

    def user_input(self, msg):
        u_input = str(input(msg))

        while u_input == '':
            u_input = str(input(msg))

        return u_input

    def add_player_to_game(self, solo=False):
        """ handel the players registry(check if players symbol are not the same,
        of player has give a symbol), add the players given data when gamew started to registry list
        solo mode => play against computer
        dual mode => plays against another player

        Args:
            solo (bool, optional): [determine if player wanna lay in solo mode or not]. Defaults to False.
        """

        if solo:
            self.register_player('player1', 'O')
            player2 = self.user_input('Player 2 Choose symbol')
            while str(player2.lower()) == 'o':
                print('symbol already in use, player 2 choose another one')
                player2 = self.user_input('player2 Choose symbol')
            else:
                self.register_player('player2', player2)

        player1 = self.user_input('Player 1 Choose symbol')
        self.register_player('player1', player1)

        player2 = self.user_input('player2 Choose symbol')

        while str(player1.lower()) == str(player2.lower()):
            print('symbol already in use, player 2 choose another one')
            player2 = self.user_input('player2 Choose symbol')
        else:
            self.register_player('player2', player2)

    def validate_position_input(self, current_player):
        """check if the game board list given key(position in board) is type int,
        is not empty and is not present in the game board

        Args:
            current_player (str): [player symbol]

        Returns:
            [int]: [game board list index]
        """
        try:
            position = int(self.user_input(f'choose number {current_player}'))
        except ValueError:
            return False

        if position == None:
            print('please enter a number')
            return False

        if position < 1 or position > 9:
            print('position must between 1 and 9')
            return False

        return position

    def register_player_combination(self, current_player, position_input):
        """by the 3rd round of player, player combination are store in a list

        Args:
            current_player (str): [player name]
            position_input (int): [game board position key in list]
        """
        self.players_combinations[current_player].append(position_input)

    def winner(self):
        # if 9 turns passed and no winner
        if self.game_finish():
            print('no winner')
            self.save_result(self.game_round(), 'no winner')
            return True

        # check pattern in game board if recognize return True
        player1_combinations = self.players_combinations['player1']
        player2_combinations = self.players_combinations['player2']

        if len(player1_combinations) >= 3:
            for win_combination in self.win_combinations:
                combination_correct = all(
                    combination in player1_combinations for combination in win_combination)
                if combination_correct:
                    self.print_board()
                    print('player 1 win')
                    self.save_result(self.game_round(), 'player 1')
                    return True

        if len(player2_combinations) >= 3:
            for win_combination in self.win_combinations:
                combination_correct = all(
                    combination in player2_combinations for combination in win_combination)
                if combination_correct:
                    self.print_board()
                    print('player 2 win')
                    self.save_result(self.game_round(), 'player 2')
                    return True

    def play(self, solo=False):
        # register player
        self.add_player_to_game()

        while not self.winner():
            # print board
            self.print_board()

            current_player = self.turn_of()

            if solo and current_player['player'] == 'player1':
                position_input = self.computer_mvement()
            else:
                position_input = self.validate_position_input(
                    current_player['player'])

            while not position_input:
                if solo and current_player['player'] == 'player1':
                    position_input = self.computer_mvement()
                else:
                    position_input = self.validate_position_input(
                        current_player['player'])
            else:
                self.manage_player_turns(current_player['symb'])
                self.register_player_combination(
                    current_player['player'], position_input)
                self.update_board(position_input, current_player['symb'])
        else:
            self.replay()

    def computer_mvement(self):
        """computer random mouvement base on the current state of the game board

        Args:
            position (int): [list index representing the position on the game board]

        Returns:
            [int]: [game board list index]
        """
        pass

    def solo_mode(self):
        # register player
        self.add_player_to_game(solo=True)
        self.play(solo=True)

    def dual_mode(self):
        self.play()

    def replay(self):
        replay = input("Replay?[y/n - Y/N]")
        while replay.lower() not in ['n', 'y']:
            replay = input("Replay?[y/n - Y/N]")

        if replay.lower() == 'y':
            self.reinitialize_board()
            self.play()
        else:
            sys.exit()


if __name__ == "__main__":
    # print score board if arg given
    parser = argparse.ArgumentParser(description='Use game extra features')
    parser.add_argument(
        '--scoreboard', action='store_true', help='score board')
    parser.add_argument(
        '--solo', action='store_true', help='solo mode')

    args = parser.parse_args()
    if args.scoreboard:
        TicTacToe().score_board()

    if args.solo:
        TicTacToe().solo_mode()

    TicTacToe().dual_mode()
