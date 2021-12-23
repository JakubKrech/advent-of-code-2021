from utils.timer import timer_decorator

players_dirac_wins = [0, 0]
possible_spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@timer_decorator
def Part1(p1_pos, p2_pos):

    game_ending_score = 1000
    dice_size = 100
    current_roll = 0

    players_results = [0, 0]
    player_spaces = [p1_pos, p2_pos]
    current_player = 0

    while True:
        roll_1 = current_roll % dice_size + 1
        current_roll += 1
        roll_2 = current_roll % dice_size + 1
        current_roll += 1
        roll_3 = current_roll % dice_size + 1
        current_roll += 1

        total_roll = roll_1 + roll_2 + roll_3
        spaces_moved = total_roll % dice_size
        
        player_spaces[current_player] = possible_spaces[(player_spaces[current_player] + spaces_moved) % 10 - 1]
        players_results[current_player] += player_spaces[current_player]

        if players_results[current_player] >= game_ending_score:
            break

        current_player = 1 if current_player == 0 else 0

    losing_player_score = players_results[0] if players_results[0] < game_ending_score else players_results[1]

    return losing_player_score * current_roll

def DiracDice(p1_pos, p2_pos, p1_result, p2_result, curr_player, total_roll, multiplier, firstTurn=False):
    game_ending_score = 21

    players_results = [p1_result, p2_result]
    player_spaces = [p1_pos, p2_pos]
    current_player = curr_player

    if not firstTurn:

        player_spaces[current_player] = possible_spaces[(player_spaces[current_player] + total_roll) % 10 - 1]
        players_results[current_player] += player_spaces[current_player]

        if players_results[current_player] >= game_ending_score:
            players_dirac_wins[current_player] += multiplier
            return

        current_player = 1 if current_player == 0 else 0

    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 3, multiplier * 1)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 4, multiplier * 3)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 5, multiplier * 6)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 6, multiplier * 7)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 7, multiplier * 6)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 8, multiplier * 3)
    DiracDice(player_spaces[0], player_spaces[1], players_results[0], players_results[1], current_player, 9, multiplier * 1)

    return players_dirac_wins

@timer_decorator
def Part2(p1_pos, p2_pos):
    DiracDice(p1_pos, p2_pos, 0, 0, 0, 0, 1, True)
    return max(players_dirac_wins)

if __name__ == "__main__":
    with open("input/day_21.txt") as file:    
        data = [s.rstrip() for s in file]

        p1_pos = int(data[0].split(':')[1])
        p2_pos = int(data[1].split(':')[1])

        print("Part 1:", Part1(p1_pos, p2_pos))
        print("Part 2:", Part2(p1_pos, p2_pos))
