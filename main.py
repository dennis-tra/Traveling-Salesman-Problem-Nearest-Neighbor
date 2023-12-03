import numpy as np
import routingpy as rp


coordinates = (
                [10.1228, 54.3233],  # Kiel
                [10.6866, 53.8655],  # HL
                [9.0601, 54.4838],  # Husum
                [9.9920, 53.5502],  # HH
                [9.4470, 54.7937],  # Flensburg
                [8.651111, 54.304167],  # St.Peter
                [9.6607, 54.3081],  # Rendsburg
                [9.1019, 54.1952],  # Heide
                [10.6095, 54.1330])  # Eutin


# create matrix with all the distances between the cities
def get_distances():
    api_key = 'Graphhopper-API-key'
    api = rp.Graphhopper(api_key=api_key)
    matrix = api.matrix(locations=coordinates, profile='car')
    distances = np.matrix(matrix.distances)
    return distances


# create symmetrical matrix
def create_sym_matrix(distances):
    m_bar = distances.copy()
    np.fill_diagonal(m_bar, 0)
    u = np.matrix(np.ones(distances.shape) * round(10*distances.max()))
    np.fill_diagonal(u, 0)
    m_symm_top = np.concatenate((u, np.transpose(m_bar)), axis=1)
    m_symm_bottom = np.concatenate((m_bar, u), axis=1)
    sym_distances = np.concatenate((m_symm_top, m_symm_bottom), axis=0)
    print(sym_distances)
    return sym_distances.astype(int)


# find nearest_neighbor from staring point (Kiel)
def nearest_neighbor(sym_distances):
    number_of_cities = len(coordinates)
    start = sym_distances[0]
    tour = []
    total_distance = 0
    next_city = start
    tour.append(next_city)
    print(next_city)
    print(number_of_cities)

    for i in range(number_of_cities):
        if i not in tour:
            current_city = np.min(next_city[np.nonzero(next_city)])
            total_distance += next_city
            tour.append(current_city)
            next_city = current_city

        print(tour)
        print(total_distance)


print(create_sym_matrix(get_distances()))
nearest_neighbor(get_distances())
