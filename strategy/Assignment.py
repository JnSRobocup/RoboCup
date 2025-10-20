import numpy as np
from typing import Dict, List, Tuple

def role_assignment(teammate_positions: List[Tuple[float, float]],
                    formation_positions: List[Tuple[float, float]]) -> Dict[int, Tuple[float, float]]:
    def distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        dx, dy =a[0]-b[0],a[1]-b[1]
        return np.sqrt(dx * dx + dy * dy)
    def build_preference_lists(players: List[Tuple[float,float]],
                               roles: List[Tuple[float,float]]):
        n = len(players)
        player_prefs: Dict[int, List[int]] ={}
        for i in range(n):
            dists =[]
            for j in range(n):
                dists.append((distance(players[i],roles[j]),j))
            dists.sort(key=lambda x: x[0])
            player_prefs[i] =[idx for _, idx in dists]
        role_prefs: Dict[int, List[int]] ={}
        for j in range(n):
            dists =[]
            for i in range(n):
                dists.append((distance(roles[j], players[i]), i))
            dists.sort(key=lambda x: x[0])
            role_prefs[j] =[idx for _, idx in dists]
        return player_prefs, role_prefs

    def gale(player_prefs: Dict[int, List[int]],
                     role_prefs: Dict[int, List[int]]) -> Dict[int, int]:
        n = len(player_prefs)
        role_match: Dict[int, int | None] = {r: None for r in range(n)}
        next_proposal_idx: Dict[int, int] = {p: 0 for p in range(n)}
        free_players: List[int] = list(range(n))

        while free_players:
            p =free_players.pop(0)  
            if next_proposal_idx[p]<n:
                r =player_prefs[p][next_proposal_idx[p]]
                next_proposal_idx[p] += 1
                if role_match[r] is None:
                    role_match[r]=p
                else:
                    current =role_match[r]
                    curr_rank =role_prefs[r].index(current)
                    new_rank =role_prefs[r].index(p)
                    if new_rank<curr_rank:
                        role_match[r] =p
                        free_players.append(current) 
                    else:
                        free_players.append(p)
            else:
                break
        player_to_role: Dict[int, int] ={}
        for r, p in role_match.items():
            if p is not None:
                player_to_role[p] =r
        return player_to_role
    n = len(teammate_positions)
    player_prefs, role_prefs =build_preference_lists(teammate_positions, formation_positions)
    assignment =gale(player_prefs, role_prefs)
    result: Dict[int, Tuple[float, float]] = {}
    for player_idx in range(n):
        unum =player_idx + 1
        role_idx =assignment[player_idx]
        result[unum] =formation_positions[role_idx]
    return result
