from utils.timer import timer_decorator
import re

def CountCuboidElements(cuboids):
    sum = 0

    for c in cuboids:
        sum += (c[1] - c[0] + 1) * (c[3] - c[2] + 1) * (c[5] - c[4] + 1)

    return sum

def SliceCuboid(c1, c2, sliceMode):

    # overlap cuboid coordinates
    x_overlapped, y_overlapped, z_overlapped = False, False, False

    overlap_happened = False
    overlapCuboid = None
    childCuboids = []

    # Check whether the cuboids overlap
    if c1[1] >= c2[0] and c1[1] <= c2[1] or c2[1] >= c1[0] and c2[1] <= c1[1]:
        x_overlapped = True

    if c1[3] >= c2[2] and c1[3] <= c2[3] or c2[3] >= c1[2] and c2[3] <= c1[3]:
        y_overlapped = True

    if c1[5] >= c2[4] and c1[5] <= c2[5] or c2[5] >= c1[4] and c2[5] <= c1[5]:
        z_overlapped = True

    if x_overlapped and y_overlapped and z_overlapped:
        overlap_happened = True

    # Calculate coordinates of cuboid representing overlapped area
    if overlap_happened:

        # check if the cuboid fully contains the other cuboid on the x axis
        if c1[0] <= c2[0] and c1[1] >= c2[1]:
            x_min = c2[0]
            x_max = c2[1]
        elif c2[0] <= c1[0] and c2[1] >= c1[1]:
            x_min = c1[0]
            x_max = c1[1]
        else: # only part of cuboids overlap
            if c1[0] < c2[0]:
                x_min = c2[0]
                x_max = c1[1]
            elif c1[0] > c2[0]:
                x_min = c1[0]
                x_max = c2[1]
            else:
                x_min = c1[0]
                x_max = c1[0]

        # check if the cuboid fully contains the other cuboid on the y axis
        if c1[2] <= c2[2] and c1[3] >= c2[3]:
            y_min = c2[2]
            y_max = c2[3]
        elif c2[2] <= c1[2] and c2[3] >= c1[3]:
            y_min = c1[2]
            y_max = c1[3]
        else: # only part of cuboids overlap
            if c1[2] < c2[2]:
                y_min = c2[2]
                y_max = c1[3]
            elif c1[2] > c2[2]:
                y_min = c1[2]
                y_max = c2[3]
            else:
                y_min = c1[2]
                y_max = c1[2]

        # check if the cuboid fully contains the other cuboid on the z axis
        if c1[4] <= c2[4] and c1[5] >= c2[5]:
            z_min = c2[4]
            z_max = c2[5]
        elif c2[4] <= c1[4] and c2[5] >= c1[5]:
            z_min = c1[4]
            z_max = c1[5]
        else: # only part of cuboids overlap
            if c1[4] < c2[4]:
                z_min = c2[4]
                z_max = c1[5]
            elif c1[4] > c2[4]:
                z_min = c1[4]
                z_max = c2[5]
            else:
                z_min = c1[4]
                z_max = c1[4]

        overlapCuboid = (x_min, x_max, y_min, y_max, z_min, z_max)

    # Generate child cuboids that contain the entire area of the father cuboid except the overlapping area
    if overlap_happened:

        sliceTarget = c1 if sliceMode == "on" else c2

        # element: x_min, x_max, y_min, y_max, z_min, z_max
        # index:     0      1      2      3      4      5

        # Cut slice on left side of x axis
        if sliceTarget[0] < overlapCuboid[0]:
            newCub = (sliceTarget[0], overlapCuboid[0] - 1, sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (overlapCuboid[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])

        # Cut slice on right side of x axis
        if sliceTarget[1] > overlapCuboid[1]:
            newCub = (overlapCuboid[1] + 1, sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], overlapCuboid[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])

        # Cut slice on top side of y axis
        if sliceTarget[2] < overlapCuboid[2]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], overlapCuboid[2] - 1, sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], overlapCuboid[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])

        # Cut slice on bottom side of y axis
        if sliceTarget[3] > overlapCuboid[3]:
            newCub = (sliceTarget[0], sliceTarget[1], overlapCuboid[3] + 1, sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], overlapCuboid[3], sliceTarget[4], sliceTarget[5])
        
        # Cut slice on upper side of z axis
        if sliceTarget[4] < overlapCuboid[4]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], overlapCuboid[4] - 1)
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], overlapCuboid[4], sliceTarget[5])
        
        # Cut slice on lower side of z axis
        if sliceTarget[5] > overlapCuboid[5]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], overlapCuboid[5] + 1, sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], overlapCuboid[5])

    return overlap_happened, childCuboids

@timer_decorator
def CalculateCuboids(data):
    
    cuboids = [data[0][1:]]

    for x in data[1:]:
        newCuboids = []
        
        if x[0] == 'on':
            current_candidates = [x[1:]]
            
            index = 0
            while index < len(cuboids):
                new_candidates = []

                for candidate in current_candidates:
                    overlap_happened, childCuboids = SliceCuboid(candidate, cuboids[index], 'on')

                    if overlap_happened:
                        new_candidates += childCuboids
                    else:
                        new_candidates.append(candidate)

                if not new_candidates:
                    break

                current_candidates = new_candidates[:]
                index += 1
            
            if new_candidates:
                newCuboids += new_candidates
                
        elif x[0] == 'off':
            index = 0
            while index < len(cuboids):
                overlap_happened, childCuboids = SliceCuboid(x[1:], cuboids[index], 'off')

                if overlap_happened:
                    cuboids.remove(cuboids[index])
                    newCuboids += childCuboids
                else:
                    index += 1                

        if newCuboids:
            cuboids += newCuboids

    return CountCuboidElements(cuboids)

if __name__ == "__main__":
    with open("input/day_22.txt") as file:    
        data = [s.rstrip() for s in file]
        parsed_data = []
        
        for line in data:
            result = re.search("(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line)
            
            operation = result.group(1)

            x1 = min(int(result.group(2)), int(result.group(3)))
            x2 = max(int(result.group(2)), int(result.group(3)))

            y1 = min(int(result.group(4)), int(result.group(5)))
            y2 = max(int(result.group(4)), int(result.group(5)))

            z1 = min(int(result.group(6)), int(result.group(7)))
            z2 = max(int(result.group(6)), int(result.group(7)))

            parsed_data.append((operation, x1, x2, y1, y2, z1, z2))

        print("Part 1:", CalculateCuboids(parsed_data[:20]))
        print("Part 2:", CalculateCuboids(parsed_data))
