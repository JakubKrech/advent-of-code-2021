from utils.timer import timer_decorator
from collections import defaultdict

def TravelNodes_Part1(connections, total_paths, from_node, path):
    for to_node in connections[from_node]:
        
        if to_node == 'end':
            total_paths += 1
        elif to_node not in path or to_node.isupper():
            pathCopy = path[:]
            pathCopy.append(to_node)
            
            total_paths = TravelNodes_Part1(connections, total_paths, to_node, pathCopy)

    return total_paths

def TravelNodes_Part2(connections, total_paths, curr_node, path, double_visit_done):
    for to_node in connections[curr_node]:
        
        if to_node == 'end':
            total_paths += 1
        elif to_node not in path or to_node.isupper() or double_visit_done == False:
            double_visit_done_Copy = double_visit_done

            if double_visit_done == False:
                if to_node.islower() and to_node in path:
                    double_visit_done_Copy = True

            pathCopy = path[:]
            pathCopy.append(to_node)
            
            total_paths =  TravelNodes_Part2(connections, total_paths, to_node, pathCopy, double_visit_done_Copy)

    return total_paths

@timer_decorator
def Part1(connections):
    return TravelNodes_Part1(connections, 0, 'start', ['start'])

@timer_decorator
def Part2(connections):
    return TravelNodes_Part2(connections, 0, 'start', ['start'], False)

if __name__ == "__main__":
    
    connections = defaultdict(list)

    with open("input/day_12.txt") as file:    
        
        data = [line.rstrip() for line in file]
        for connection in data:
            c1, c2 = connection.split('-')
        
            if c2 != 'start':
                connections[c1] += [c2]
            if c1 != 'start':
                connections[c2] += [c1]

        print("Part 1:", Part1(connections))
        print("Part 2:", Part2(connections))
