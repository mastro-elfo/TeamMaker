from Players import Players


def make_pairs(players):
    """Each step give the weaker team the stronger player"""
    players_ = sorted(players, key=lambda x: x.rating, reverse=True)
    left_team = Players()
    right_team = Players()
    while len(players_) > 1:
        left_team_strength = left_team.strength()
        right_team_strength = right_team.strength()
        if left_team_strength > right_team_strength:
            right_team.append(players_.pop(0))
            left_team.append(players_.pop(0))
        else:
            left_team.append(players_.pop(0))
            right_team.append(players_.pop(0))
    while len(players_) > 0:
        left_team_strength = left_team.strength()
        right_team_strength = right_team.strength()
        if left_team_strength > right_team_strength:
            right_team.append(players_.pop(0))
        else:
            left_team.append(players_.pop(0))
    return left_team, right_team
