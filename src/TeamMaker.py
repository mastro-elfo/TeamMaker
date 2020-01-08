from Players import Players


def make_best(players):
    """Minimize the absolute value of the difference of strengths"""
    left_team, right_team = make_pairs(players)
    done = False
    i, j = 0, 0
    while not done:
        left_team_strength = left_team.strength()
        right_team_strength = right_team.strength()
        from_left = left_team.pop(i)
        from_right = right_team.pop(j)
        left_team.insert(i, from_right)
        right_team.insert(j, from_left)
        swap_left_team_strength = left_team.strength()
        swap_right_team_strength = right_team.strength()
        if abs(swap_left_team_strength - swap_right_team_strength) < abs(
            left_team_strength - right_team_strength
        ):
            # Swap is better
            i, j = 0, 0
        else:
            # Swap is worse
            from_left = left_team.pop(i)
            from_right = right_team.pop(j)
            left_team.insert(i, from_right)
            right_team.insert(j, from_left)
            j += 1
            if j >= len(right_team):
                j = 0
                i += 1
            if i >= len(left_team):
                done = True
    return left_team, right_team


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


def make_abba(players):
    """Each step give the weaker team the stronger player in ABBA order"""
    players_ = sorted(players, key=lambda x: x.rating, reverse=True)
    left_team = Players()
    right_team = Players()
    while len(players_) > 4:
        left_team_strength = left_team.strength()
        right_team_strength = right_team.strength()
        if left_team_strength > right_team_strength:
            right_team.append(players_.pop(0))
            left_team.append(players_.pop(0))
            left_team.append(players_.pop(0))
            right_team.append(players_.pop(0))
        else:
            left_team.append(players_.pop(0))
            right_team.append(players_.pop(0))
            right_team.append(players_.pop(0))
            left_team.append(players_.pop(0))
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
