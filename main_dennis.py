import numpy as np
import routingpy as rp
import pickle
import os

# index of the city in the matrix
city_idx = {
    0: "Kiel",
    1: "Lübeck",
    2: "Husum",
    3: "Hamburg",
    4: "Flensburg",
    5: "St.Peter",
    6: "Rendsburg",
    7: "Heide",
    8: "Eutin",
}

coordinates = [
    [10.1228, 54.3233],  # Kiel
    [10.6866, 53.8655],  # Lübeck
    [9.0601, 54.4838],  # Husum
    [9.9920, 53.5502],  # Hamburg
    [9.4470, 54.7937],  # Flensburg
    [8.651111, 54.304167],  # St.Peter
    [9.6607, 54.3081],  # Rendsburg
    [9.1019, 54.1952],  # Heide
    [10.6095, 54.1330]  # Eutin
]


def get_distances():
    """
    create matrix with all the distances between the cities
    """
    api_key = '7f0b7eda-f08e-4126-aff4-f29f270549bb'
    api = rp.Graphhopper(api_key=api_key)
    matrix = api.matrix(locations=coordinates, profile='car')
    return matrix.distances


# cache API response
cache_file_name = "distances.p"
if os.path.isfile(cache_file_name):
    with open(cache_file_name, "rb") as f:
        distances = pickle.load(f)
else:
    distances = get_distances()
    with open(cache_file_name, "wb") as f:
        pickle.dump(distances, f)


def find_nearest_neighbor(city_idx, visited):
    """
    finds the nearest neighbor to the given city_idx. It skips all city indexes that are in the visited set.
    """
    smallest_distance = None
    smallest_distance_city_idx = None

    # loop through all distances from that given city and determine the smallest. We skip visited cities
    # note, this can probably be done with numpy. When using numpy, I'm not sure how to exclude indexes, though
    for idx, distance in enumerate(distances[city_idx]):

        # skip already visited cities
        if idx in visited:
            continue

        # if we don't know a smallest distance yet or the current distance is even smaller
        # than the currently known smallest distance -> overwrite the variables
        if smallest_distance is None or smallest_distance > distance:
            smallest_distance = distance
            smallest_distance_city_idx = idx

    # return the smallest distance and city index. Both can be None, in which case we're done!
    return smallest_distance, smallest_distance_city_idx


# we start at city 0
start_city_idx = 0

# init a set that keeps track of cities we've visited
visited = set({})

# add our start point to the list of visited cities
visited.add(start_city_idx)

# tour will keep track of the order in which we visited the cities
tour = [start_city_idx]

# tour_distances will keep track of the individual travelled distances between cities
tour_distances = [0]

# total_distance will keep track of the total distance covered
total_distance = 0

# find the nearest neighbor to our starting city
next_distance, next_city_idx = find_nearest_neighbor(start_city_idx, visited)

# now continue to find the nearest neighbor as long as we find a next city to visit
while next_city_idx is not None:

    # tally the total_distance
    total_distance += next_distance

    # add the city to our tour
    tour += [next_city_idx]

    # add individual distance travelled to our list
    tour_distances += [next_distance]

    # keep note that we visited that city!
    visited.add(next_city_idx)

    # find the next nearest neighbor
    next_distance, next_city_idx = find_nearest_neighbor(next_city_idx, visited)

print("Tour:")
for i, stop in enumerate(tour):
    print(f"{i}. {city_idx[stop]} ({tour_distances[i]/1000}km)")
print(f"Total distance {total_distance/1000}km")