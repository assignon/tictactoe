import sys
import os
import argparse
import random
import time


class TicTacToe:
    def __init__(self):
        self.board = ['', '1', '2', '3',
                      '4', '5', '6', '7', '8', '9']
        self.player_turn_list = []  # players symbol
        self.player_registry = []  # {'player': playername, 'symb': 0}
        self.players_combinations = {'player1': [], 'player2': []}
        self.win_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [3, 6, 9], [2, 5, 8],
            [1, 5, 9], [3, 5, 7]
        ]
        # use by computer in solo mode to pick position
        self.position_left = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def score_board(self):
        # fetch data from scores file and display it when <--scoreboard> args give
        try:
            if os.stat('scores.txt').st_size == 0:
                print('No score register yet')

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

    def clear_scoreboard():
        try:
            open('scores.txt', 'w').close()
            print('Game board cleared')
        except FileNotFoundError as fe:
            raise FileNotFoundError(f'File scores.txt not found')

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

    def reinitialize_board(self, new_players=False):
        """clear game data

        Args:
            new_players (bool, optional): [determine if players wanna choose another name and symbol or not]. Defaults to False.
        """
        self.player_turn_list = []
        if not new_players:
            self.player_registry = []
        self.players_combinations = {'player1': [], 'player2': []}
        self.board = self.board = ['', '1', '2', '3',
                                   '4', '5', '6', '7', '8', '9']
        self.position_left = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def print_board(self):
        print("\n")
        print("{}  |  {}  |  {} ".format(
            self.board[1], self.board[2], self.board[3]))
        print("---------------")
        print("{}  |  {}  |  {} ".format(
            self.board[4], self.board[5], self.board[6]))
        print("---------------")
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
        return len(self.player_turn_list) > 9

    def update_board(self, index, current_player):
        """update the game board list after each round base on 
        game board list index representing position in game

        Args:
            index (int): [board list index]
            current_player (str): [player symbol]
        """
        self.board[index] = current_player
        # update position_left list by removing theposition selected
        self.position_left.remove(index)

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
        else:
            player1 = self.user_input('Player 1 Choose symbol')
            self.register_player('player1', player1)

            player2 = self.user_input('player2 Choose symbol')

            while str(player1.lower()) == str(player2.lower()):
                print('symbol already in use, player 2 choose another one')
                player2 = self.user_input('player2 Choose symbol')
            else:
                self.register_player('player2', player2)

    def validate_position_input(self, position):
        """check if the game board list given key(position in board) is type int,
        is not empty and is not present in the game board

        Args:
            position (int): [game boars list index]

        Returns:
            [int]: [game board list index]
        """

        if position in self.players_combinations['player1'] or position in self.players_combinations['player2']:
            print('position already take')
            return False

        if position < 1 or position > 9:
            print('position must between 1 and 9')
            return False

        return True

    def register_player_combination(self, current_player, position_input):
        """by the 3rd round of player, player combination are store in a list

        Args:
            current_player (str): [player name]
            position_input (int): [game board position key in list]
        """
        self.players_combinations[current_player].append(position_input)

    def computer_mvement(self):
        """computer random mouvement base on the current state of the game board

        Args:
            position (int): [list index representing the position on the game board]

        Returns:
            [int]: [game board list index]
        """
        print('Computer is choosing...')
        time.sleep(2)
        position = random.choice(self.position_left)
        print(f'Computer chose {position}')

        return position

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
                    print(
                        f'player 1 [{self.get_player("symb", "player", "player1")}] win')
                    self.save_result(self.game_round(
                    ), f'player 1 => {self.get_player("symb", "player", "player1")}')
                    return True

        if len(player2_combinations) >= 3:
            for win_combination in self.win_combinations:
                combination_correct = all(
                    combination in player2_combinations for combination in win_combination)
                if combination_correct:
                    self.print_board()
                    print(
                        f'player 2 [{self.get_player("symb", "player", "player2")}] win')
                    self.save_result(
                        self.game_round(), f'player 2 => f{self.get_player("symb", "player", "player2")}')
                    return True

    def play(self, solo=False):

        while not self.winner():
            # print board
            self.print_board()
            current_player = self.turn_of()

            if solo and current_player['player'] == 'player1':
                position_input = self.computer_mvement()
            else:
                position_input = int(self.user_input(
                    f'choose number {current_player["player"]}'))

            position_validated = self.validate_position_input(position_input)
            while not position_validated:
                position_input = int(self.user_input(
                    f'choose number {current_player["player"]}'))
                position_validated = self.validate_position_input(
                    position_input)
            else:
                self.manage_player_turns(current_player['symb'])
                self.register_player_combination(
                    current_player['player'], position_input)
                self.update_board(position_input, current_player['symb'])
        else:
            self.replay()

    def solo_mode(self, add_player=True):
        # register player
        if add_player:
            self.add_player_to_game(solo=True)
        self.play(solo=True)

    def dual_mode(self, add_player=True):
        # register player
        if add_player:
            self.add_player_to_game()
        self.play()

    def reinit_player_symbols(self):
        # reset the player registry list if players want to choose another symbols
        new_players = input("Choose new symbols?[y/n - Y/N]")
        while new_players.lower() not in ['n', 'y']:
            new_players = input("Choose new symbols?[y/n - Y/N]")

        if new_players.lower() == 'y':
            self.reinitialize_board()
            return True
        else:
            self.reinitialize_board(new_players=True)
            return False

    def replay(self):
        replay = input("Replay?[y/n - Y/N]")
        while replay.lower() not in ['n', 'y']:
            replay = input("Replay?[y/n - Y/N]")

        if replay.lower() == 'y':
            mode = input("solo or dual mode?[s = solo/d = dual]")
            while mode.lower() not in ['s', 'd']:
                mode = input("solo or dual mode?[s = solo/d = dual]")

            if mode == 's':
                reinit = self.reinit_player_symbols()
                if reinit:
                    # reinitialize game with new player symbols
                    self.solo_mode()
                else:
                    self.solo_mode(add_player=False)
            else:
                reinit = self.reinit_player_symbols()
                if reinit:
                    # reinitialize game with new player symbols
                    self.dual_mode()
                else:
                    self.dual_mode(add_player=False)
        else:
            sys.exit()


if __name__ == "__main__":
    # print score board if arg given
    parser = argparse.ArgumentParser(description='Use game extra features')
    parser.add_argument(
        '--scoreboard', action='store_true', help='score board')
    parser.add_argument(
        '--solo', action='store_true', help='solo mode')
    parser.add_argument(
        '--clear', action='store_true', help='clear score board')

    args = parser.parse_args()
    if args.scoreboard:
        TicTacToe().score_board()
        sys.exit()

    if args.clear:
        TicTacToe.clear_scoreboard()
        sys.exit()

    if args.solo:
        TicTacToe().solo_mode()

    TicTacToe().dual_mode()
