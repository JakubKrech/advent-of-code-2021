from utils.timer import timer_decorator
import re

def CountCuboidElements(cuboid):
    # sum = 0

    # print(cuboid)

    # for cuboid in cuboids:
    #     sum += (cuboid[1] - cuboid[0] + 1) * (cuboid[3] - cuboid[2] + 1) * (cuboid[5] - cuboid[4] + 1)

    # print("TOTAL ELEMENTS:", sum)

    return (cuboid[1] - cuboid[0] + 1) * (cuboid[3] - cuboid[2] + 1) * (cuboid[5] - cuboid[4] + 1)

log = True

def CheckIfCuboidsOverlap(c1, c2):
    if log: print("Checking cuboids", c1, "and", c2)

    # overlap data
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    z_min, z_max = 0, 0

    x_overlapped = False
    y_overlapped = False
    z_overlapped = False

    overlap_happened = False

    if c1[1] >= c2[0] and c1[1] <= c2[1] or c2[1] >= c1[0] and c2[1] <= c1[1]:
        x_overlapped = True

    if c1[3] >= c2[2] and c1[3] <= c2[3] or c2[3] >= c1[2] and c2[3] <= c1[3]:
        y_overlapped = True

    if c1[5] >= c2[4] and c1[5] <= c2[5] or c2[5] >= c1[4] and c2[5] <= c1[5]:
        z_overlapped = True

    if (x_overlapped and y_overlapped and z_overlapped):
        # print("OVERLAP!")
        overlap_happened = True
        
        if c1[0] < c2[0]:
            x_min = c2[0]
            x_max = c1[1]
        elif c1[0] > c2[0]:
            x_min = c1[0]
            x_max = c2[1]
        else:
            x_min = c1[0]
            x_max = c1[0]

        if c1[2] < c2[2]:
            y_min = c2[2]
            y_max = c1[3]
        elif c1[2] > c2[2]:
            y_min = c1[2]
            y_max = c2[3]
        else:
            y_min = c1[2]
            y_max = c1[2]

        if c1[4] < c2[4]:
            z_min = c2[4]
            z_max = c1[5]
        elif c1[4] > c2[4]:
            z_min = c1[4]
            z_max = c2[5]
        else:
            z_min = c1[4]
            z_max = c1[4]

    # else:
    #     print("NO OVERLAP")

    return overlap_happened, (x_min, x_max, y_min, y_max, z_min, z_max)

def SliceCuboid(c1, c2, sliceMode):
    if log: print("Slicing cuboids", c1, "and", c2, "mode is:", sliceMode)

    # overlap data
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    z_min, z_max = 0, 0

    x_overlapped = False
    y_overlapped = False
    z_overlapped = False

    overlap_happened = False
    overlapCuboid = None

    if c1[1] >= c2[0] and c1[1] <= c2[1] or c2[1] >= c1[0] and c2[1] <= c1[1]:
        x_overlapped = True

    if c1[3] >= c2[2] and c1[3] <= c2[3] or c2[3] >= c1[2] and c2[3] <= c1[3]:
        y_overlapped = True

    if c1[5] >= c2[4] and c1[5] <= c2[5] or c2[5] >= c1[4] and c2[5] <= c1[5]:
        z_overlapped = True

    if (x_overlapped and y_overlapped and z_overlapped):
        overlap_happened = True
        
        print(c1[0], c2[0])

        # first cuboid contains the second on x axis
        if c1[0] <= c2[0] and c1[1] >= c2[1]:
            x_min = c2[0]
            x_max = c2[1]
        elif c2[0] <= c1[0] and c2[1] >= c1[1]:
            x_min = c1[0]
            x_max = c1[1]
        else:
            # only part of cuboids overlap
            if c1[0] < c2[0]:
                x_min = c2[0]
                x_max = c1[1]
            elif c1[0] > c2[0]:
                x_min = c1[0]
                x_max = c2[1]
            else:
                x_min = c1[0]
                x_max = c1[0]

        # first cuboid contains the second on y axis
        if c1[2] <= c2[2] and c1[3] >= c2[3]:
            y_min = c2[2]
            y_max = c2[3]
        elif c2[2] <= c1[2] and c2[3] >= c1[3]:
            y_min = c1[2]
            y_max = c1[3]
        else:
            # only part of cuboids overlap
            if c1[2] < c2[2]:
                y_min = c2[2]
                y_max = c1[3]
            elif c1[2] > c2[2]:
                y_min = c1[2]
                y_max = c2[3]
            else:
                y_min = c1[2]
                y_max = c1[2]

        # first cuboid contains the second on z axis
        if c1[4] <= c2[4] and c1[5] >= c2[5]:
            z_min = c2[4]
            z_max = c2[5]
        elif c2[4] <= c1[4] and c2[5] >= c1[5]:
            z_min = c1[4]
            z_max = c1[5]
        else:
            # only part of cuboids overlap
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
        print("OVERLAP:", overlapCuboid)

    childCuboids = []

    if overlap_happened:
        print("  Overlap detected, beggining slicing. New cuboids that contain everything but overlap will be created.")

        sliceTarget = None

        if sliceMode == "on":
            sliceTarget = c1
            print("    New cuboid", sliceTarget, "was being added, so we need all the area except overlap", overlapCuboid, " - it is already active.")
        elif sliceMode == "off":
            sliceTarget = c2
            print("    We delete area contained by overlap", overlapCuboid, "so some part of cuboid", sliceTarget, "will have to be cut. Remember to delete it and replace by new smaller cuboids.")

        print("    Begin slicing", overlapCuboid, "out of", sliceTarget)

        # element: x_min, x_max, y_min, y_max, z_min, z_max
        # index:     0      1      2      3      4      5

        # Cut slice on left side of x axis
        print(sliceTarget[0] < overlapCuboid[0], sliceTarget[0], overlapCuboid[0])
        if sliceTarget[0] < overlapCuboid[0]:
            newCub = (sliceTarget[0], overlapCuboid[0] - 1, sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (overlapCuboid[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            print("    Sliced left x side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)

        # Cut slice on right side of x axis
        print(sliceTarget[1] > overlapCuboid[1], sliceTarget[1], overlapCuboid[1])
        if sliceTarget[1] > overlapCuboid[1]:
            newCub = (overlapCuboid[1] + 1, sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], overlapCuboid[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            print("    Sliced right x side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)

        # Cut slice on top side of y axis
        print(sliceTarget[2] < overlapCuboid[2], sliceTarget[2], overlapCuboid[2])
        if sliceTarget[2] < overlapCuboid[2]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], overlapCuboid[2] - 1, sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], overlapCuboid[2], sliceTarget[3], sliceTarget[4], sliceTarget[5])
            print("    Sliced top y side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)

        # Cut slice on bottom side of y axis
        print(sliceTarget[3] > overlapCuboid[3], sliceTarget[3], overlapCuboid[3])
        if sliceTarget[3] > overlapCuboid[3]:
            newCub = (sliceTarget[0], sliceTarget[1], overlapCuboid[3] + 1, sliceTarget[3], sliceTarget[4], sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], overlapCuboid[3], sliceTarget[4], sliceTarget[5])
            print("    Sliced bottom y side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)
        
        # Cut slice on upper side of z axis
        print(sliceTarget[4] < overlapCuboid[4], sliceTarget[4], overlapCuboid[4])
        if sliceTarget[4] < overlapCuboid[4]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], overlapCuboid[4] - 1)
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], overlapCuboid[4], sliceTarget[5])
            print("    Sliced upper z side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)
        
        # Cut slice on lower side of z axis
        print(sliceTarget[5] > overlapCuboid[5], sliceTarget[5], overlapCuboid[5])
        if sliceTarget[5] > overlapCuboid[5]:
            newCub = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], overlapCuboid[5] + 1, sliceTarget[5])
            childCuboids.append(newCub)
            sliceTarget = (sliceTarget[0], sliceTarget[1], sliceTarget[2], sliceTarget[3], sliceTarget[4], overlapCuboid[5])
            print("    Sliced lower z side:", newCub)
            print("    Cuboid that is being sliced is now:", sliceTarget)
            print("    Child cuboids:", childCuboids)

    return overlap_happened, childCuboids


@timer_decorator
def Part1(data):
    
    # for x in data:
    #     print(x)

    cuboids = [data[0][1:]]

    sum_of_cuboids = 0
    for y in cuboids:
        sum_of_cuboids += CountCuboidElements(y)
    print("SUM OF CUBOIDS:", sum_of_cuboids)

    print("\nCuboids", len(cuboids))
    for y in cuboids:
        print(y, CountCuboidElements(y))

    for x in data[1:]:
        print("\n>>> Analizing line", x)
        
        newCuboids = []
        
        if x[0] == 'on':
            index = 0
            while index < len(cuboids):
                overlap_happened, childCuboids = SliceCuboid(x[1:], cuboids[index], 'on')

                if overlap_happened:
                    newCuboids += childCuboids
                    print("CUBOIDS:", cuboids)
                    print("newCuboids:", newCuboids)
                    
                
                index += 1
            newCuboids += childCuboids
                
        elif x[0] == 'off':
            index = 0
            while index < len(cuboids):
                overlap_happened, childCuboids = SliceCuboid(x[1:], cuboids[index], 'off')

                if overlap_happened:
                    cuboids.remove(cuboids[index])
                    newCuboids += childCuboids
                else:
                    index += 1

        cuboids += newCuboids
        print("====================== CUBOIDS:", cuboids)

        sum_of_cuboids = 0
        for y in cuboids:
            sum_of_cuboids += CountCuboidElements(y)
        print("SUM OF CUBOIDS:", sum_of_cuboids)
        # print("\nCuboids", len(cuboids))
        # for y in cuboids:
        #     print(y, CountCuboidElements(y))

        # print("Overlaps", len(overlaps))
        # for y in overlaps:
        #     print(y, CountCuboidElements(y))

        # print("Removed:", len(removed))
        # for y in removed:
        #     print(y, CountCuboidElements(y))

    print("\nCuboids", len(cuboids))

    sum_of_cuboids = 0
    for y in cuboids:
        sum_of_cuboids += CountCuboidElements(y)
        print(y, CountCuboidElements(y))
    print("SUM OF CUBOIDS:", sum_of_cuboids)


    return sum_of_cuboids

if __name__ == "__main__":
    with open("input/day_2222.txt") as file:    
        data = [s.rstrip() for s in file]
        
        parsed_data = []
        
        x_min, x_max = 1000000, 0
        y_min, y_max = 1000000, 0
        z_min, z_max = 1000000, 0
        
        for line in data:
            result = re.search("(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line)
            
            x1 = min(int(result.group(2)), int(result.group(3)))
            x2 = max(int(result.group(2)), int(result.group(3)))

            x_min = min(x_min, x1)
            x_max = max(x_max, x2)

            y1 = min(int(result.group(4)), int(result.group(5)))
            y2 = max(int(result.group(4)), int(result.group(5)))

            y_min = min(y_min, y1)
            y_max = max(y_max, y2)

            z1 = min(int(result.group(6)), int(result.group(7)))
            z2 = max(int(result.group(6)), int(result.group(7)))

            z_min = min(z_min, z1)
            z_max = max(z_max, z2)

            parsed_data.append((result.group(1), x1, x2, y1, y2, z1, z2)) # , x_min, x_max, y_min, y_max, z_min, z_max))
        
        
        # for x in parsed_data:
        #     print(x)

        print("Part 1:", Part1(parsed_data))