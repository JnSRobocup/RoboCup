import numpy as np

def role_assignment(teammate_positions, formation_positions): 

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#
    
    def euclidean_distance(pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def create_preference_lists(teammate_positions, formation_positions):
        n = len(teammate_positions)
        player_preferences = {}
        for i in range(n):
            distances = []
            for j in range(n):
                distance = euclidean_distance(teammate_positions[i], formation_positions[j])
                distances.append((distance, j))
            distances.sort(key=lambda x: x[0])
            player_preferences[i] = [idx for _, idx in distances]
        
        role_preferences = {}
        for j in range(n):
            distances = []
            for i in range(n):
                distance = euclidean_distance(formation_positions[j], teammate_positions[i])
                distances.append((distance, i))
            distances.sort(key=lambda x: x[0])
            role_preferences[j] = [idx for _, idx in distances]
        
        return player_preferences, role_preferences
    
    def gale_shapley_algorithm(player_preferences, role_preferences):
        n = len(player_preferences)
        unmatched_players = list(range(n))
        current_matches = {role: None for role in range(n)}  
        player_next_proposal = {player: 0 for player in range(n)}  
        
        while unmatched_players:
            player = unmatched_players.pop(0)
            if player_next_proposal[player] < n:
                role = player_preferences[player][player_next_proposal[player]]
                player_next_proposal[player] += 1
                if current_matches[role] is None:
                    current_matches[role] = player
                else:
                    current_partner = current_matches[role]
                    current_partner_rank = role_preferences[role].index(current_partner)
                    new_proposer_rank = role_preferences[role].index(player)
                    
                    if new_proposer_rank < current_partner_rank:
                        current_matches[role] = player
                        unmatched_players.append(current_partner)  # Previous partner becomes unmatched
                    else:
                        unmatched_players.append(player)
            else:
                break
        
        player_to_role = {}
        for role, player in current_matches.items():
            if player is not None:
                player_to_role[player] = role
        
        return player_to_role
    n = len(teammate_positions)
    player_preferences, role_preferences = create_preference_lists(teammate_positions, formation_positions)
    player_to_role_mapping = gale_shapley_algorithm(player_preferences, role_preferences)
    point_preferences = {}
    for player_idx in range(n):
        unum = player_idx + 1  # Convert 0-based to 1-based indexing
        assigned_role = player_to_role_mapping[player_idx]
        point_preferences[unum] = formation_positions[assigned_role]
    
    return point_preferences