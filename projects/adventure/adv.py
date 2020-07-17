from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# # map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
total_moves = []
"""
#Understand
Choice an algorithim that fills traversal_path with paths to all rooms, total 500 rooms
need the least amount of steps possible, moving backwards counts.
Nodes are rooms
edges are exits to other rooms
each room with exits can have unexplored exists "?"
if room has no exits or unexplored exists, backtrack untill you find a room with unexplored exits...???

get_neighbors aka exits
explore each exit, add to visited

"""
def opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"
    else: 
        return None

# move through rooms

# def fisher_yates_shuffle(l):
#         for i in range(0, len(l)):
#             random_index = random.randint(i, len(l) - 1)
#             l[random_index], l[i] = l[i], l[random_index]
def explore_paths():
    # create stack
    stack = Stack()
    # keep track of visited nodes 
    visited = set()
    
    
    # while visited is less than total amount of rooms 
    while len(visited) < len(world.rooms):
        path= []
        # for every exit in current room
        for exits in player.current_room.get_exits():
            # if exits of players current room NOT in visited
            if player.current_room.get_room_in_direction(exits) not in visited:
                # append to paths
                path.append(exits)
        # add current_room to visited
        if player.current_room not in visited:
            visited.add(player.current_room)
        # if length of path is greater than zero
    
        if len(path) > 0:
            random_path_movement = random.randint(0, len(path) - 1)
            # print(random_path_movement)
            stack.push(path[random_path_movement])
            player.travel(path[random_path_movement])
            # print(path)
            traversal_path.append(path[random_path_movement])
            total_moves.append(path[random_path_movement])
        else:
            # return last from stack
            last = stack.pop()
            # backtrack
            player.travel(opposite_direction(last))
            total_moves.append(opposite_direction(last))
            # add to travel_path
            traversal_path.append(opposite_direction(last))




explore_paths()
traversal_path = total_moves
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
