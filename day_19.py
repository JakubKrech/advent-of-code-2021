from utils.timer import timer_decorator

def detect_rotation(scanner1, scanner2):

    # print("DETECTING ROTATION FOR SCANNERS OF LENGTH", len(scanner1), len(scanner2))

    x_sign, y_sign, z_sign = None, None, None
    ret_x, ret_y, ret_z = None, None, None
    found = False

    for sign_x in [-1, 1]:
            for sign_y in [-1, 1]:
                for sign_z in [-1, 1]:
                    for x in [0, 1, 2]:
                        for y in [0, 1, 2]:
                            for z in [0, 1, 2]:
                                if x == y or x == z or y == z:
                                    continue
                                rotated_data = []

                                for scan in scanner2:                    
                                    rotated_data.append((scan[x] * sign_x, scan[y] * sign_y, scan[z] * sign_z))

                                intersected_beacons = list(set(rotated_data).intersection(scanner1))
                                ammount_of_intersected = len(intersected_beacons) + 1
                                # print("THAT MANY ELEMENTS:", len(elements_intersection))

                                if ammount_of_intersected >= 12:
                                    print("FOUND!!!!!!!!! - ", ammount_of_intersected, "SAME ELEMENTS")
                                    
                                    # print(scanner1)
                                    # print(scanner2)
                                    # print(rotated_data)
                                    # print(intersected_beacons)

                                    letters = ['x', 'y', 'z']

                                    print("DEBUG SIGNS", sign_x, sign_y, sign_z)

                                    x_sign = '-' if sign_x == -1 else '+'
                                    y_sign = '-' if sign_y == -1 else '+'
                                    z_sign = '-' if sign_z == -1 else '+'

                                    ret_x = letters[x]
                                    ret_y = letters[y]
                                    ret_z = letters[z]

                                    print("DEBUG LETTERS", ret_x, ret_y, ret_z)

                                    print("FOUND parameters were:", x_sign + ret_x, y_sign + ret_y, z_sign + ret_z)

                                    found = True

                                    return found, x_sign, ret_x, y_sign, ret_y, z_sign, ret_z, intersected_beacons
    
    return found, x_sign, ret_x, y_sign, ret_y, z_sign, ret_z, intersected_beacons

def GetRelativeToBeacon(scanner, beacon_id):
    # print("ANALYZING:", scanner, "for beacon #", beacon_id)
    relative_to_beacon = []

    relative = scanner[beacon_id]

    for beac in scanner:
        if relative == beac:
            # print(beacon, beac, "SKIPPED")
            continue
        # print(beacon, beac)

        newww = (beac[0] - relative[0], beac[1] - relative[1], beac[2] - relative[2])
        relative_to_beacon.append(newww)
        # print(relative, beac)

        # print("REL:", relative)
        # print("BEC:", beac)

        # print("NEW:", newww)

        # olddd = (newww[0] + relative[0], newww[1] + relative[1], newww[2] + relative[2])

        # print("OLD:", olddd)

    # print(scanner)
    # print(relative_to_beacon)

    # for r in relative_to_beacon:
    #     print(r)

    # input()
    return relative_to_beacon

@timer_decorator
def Part1(scanners):

    scanner_locations = [(None, None, None)] * len(scanners)
    scanner_locations[0] = (0, 0, 0)
    # scanner_locations[1] = (68,-1246,-43) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ammount_of_scans_per_scanner = len(scanners[0])

    # for i, s in enumerate(scanners):
    #     print("--- SCANNER", i, "(", scanner_locations[i], ") ---")
    #     for ss in s:
    #         print(ss)

    all_existing_beacons = []

    identified_scanners = 1
    current_scanner_id = 0

    while identified_scanners < len(scanner_locations):

        scanner_identified = False

        for searched_scanner_id in range(len(scanner_locations)):
            if scanner_locations[searched_scanner_id] != (None, None, None) or searched_scanner_id == current_scanner_id:
                continue

            print("current_scanner_id =", current_scanner_id, "searched_scanner_id =", searched_scanner_id)

            for current_beacon_id in range(ammount_of_scans_per_scanner):
                # print("current_beacon_id =", current_beacon_id)
                relative_for_current_scanner = GetRelativeToBeacon(scanners[current_scanner_id], current_beacon_id)
                # print(relative_for_current_scanner)
                
                for searched_beacon_id in range(ammount_of_scans_per_scanner):
                    
        
                    relative_for_searched_scanner = GetRelativeToBeacon(scanners[searched_scanner_id], searched_beacon_id)
                    # print(relative_for_searched_scanner)

                    found, x_sign, ret_x, y_sign, ret_y, z_sign, ret_z, intersected_beacons = detect_rotation(relative_for_current_scanner, relative_for_searched_scanner)

                    if found == True:
                        print("MATCH FOUND!")
                        print("IT HAPPENED FOR ORIGINAL VALUES OF CURRENT: ", current_beacon_id, scanners[current_scanner_id][current_beacon_id])
                        print("IT HAPPENED FOR ORIGINAL VALUES OF SEARCHED:", searched_beacon_id, scanners[searched_scanner_id][searched_beacon_id], "AND THOSE ARE THE SAME BEACON")

                        relative_beacon = scanners[current_scanner_id][current_beacon_id]
                        searched_relative_beacon = scanners[searched_scanner_id][searched_beacon_id]

                        # if ret_x == 'x':
                        #     sign_x = 1 if x_sign == '+' else -1
                        # elif ret_x == 'y':
                        #     sign_x = 1 if y_sign == '+' else -1
                        # elif ret_x == 'z':
                        #     sign_x = 1 if z_sign == '+' else -1

                        # if ret_y == 'x':
                        #     sign_y = 1 if x_sign == '+' else -1
                        # elif ret_y == 'y':
                        #     sign_y = 1 if y_sign == '+' else -1
                        # elif ret_y == 'z':
                        #     sign_y = 1 if z_sign == '+' else -1

                        # if ret_z == 'x':
                        #     sign_z = 1 if x_sign == '+' else -1
                        # elif ret_z == 'y':
                        #     sign_z = 1 if y_sign == '+' else -1
                        # elif ret_z == 'z':
                        #     sign_z = 1 if z_sign == '+' else -1

                        sign_x = 1 if x_sign == '+' else -1
                        sign_y = 1 if y_sign == '+' else -1
                        sign_z = 1 if z_sign == '+' else -1

                        # get coordinates of identified scanner
                        print("CALCULATE NEW SCANNER:", relative_beacon, sign_x, sign_y, sign_z, searched_relative_beacon)
                        if ret_x == 'x':
                            ns_x = relative_beacon[0] - (sign_x *  searched_relative_beacon[0])
                        elif ret_x == 'y':
                            ns_x = relative_beacon[0] - (sign_x *  searched_relative_beacon[1])
                        elif ret_x == 'z':
                            ns_x = relative_beacon[0] - (sign_x *  searched_relative_beacon[2])

                        if ret_y == 'x':
                            ns_y = relative_beacon[1] - (sign_y *  searched_relative_beacon[0])
                        elif ret_y == 'y':
                            ns_y = relative_beacon[1] - (sign_y *  searched_relative_beacon[1])
                        elif ret_y == 'z':
                            ns_y = relative_beacon[1] - (sign_y *  searched_relative_beacon[2])

                        if ret_z == 'x':
                            ns_z = relative_beacon[2] - (sign_z *  searched_relative_beacon[0])
                        elif ret_z == 'y':
                            ns_z = relative_beacon[2] - (sign_z *  searched_relative_beacon[1])
                        elif ret_z == 'z':
                            ns_z = relative_beacon[2] - (sign_z *  searched_relative_beacon[2])

                        new_scanner_location = (ns_x, ns_y, ns_z)
                        print("NEW SCANNER #", searched_scanner_id, ":", new_scanner_location)

                        # add newly found beacons from perspective of current scanner
                        current_scanner_location = scanner_locations[current_scanner_id]
                        print("CURRENT SCANNER LOCATION:", current_scanner_location)

                        real_position_of_relative_beacon = (current_scanner_location[0] + relative_beacon[0], current_scanner_location[1] + relative_beacon[1], current_scanner_location[2] + relative_beacon[2])
                        print("REAL:", real_position_of_relative_beacon)

                        new_real = (new_scanner_location[0] - searched_relative_beacon[0], new_scanner_location[1] + searched_relative_beacon[1], new_scanner_location[2] - searched_relative_beacon[2])
                        print(new_scanner_location, searched_relative_beacon)
                        print("?????????", real_position_of_relative_beacon, new_real)

                        

                        print("POSITION OF CURRENT SCANER AND CURRENT RELATIVE:", current_scanner_location, relative_beacon)
                        print("RESULTS IN:", real_position_of_relative_beacon)

                        # add relative beacon, and beacons that intersected with other sensor
                        all_existing_beacons.append(relative_beacon)

                        for new_beac in intersected_beacons:
                            print("NEW BEKON:", new_beac)
                            new_xx = relative_beacon[0] + new_beac[0]
                            new_yy = relative_beacon[1] + new_beac[1]
                            new_zz = relative_beacon[2] + new_beac[2]

                            # print(new_beac, real_position_of_relative_beacon, "RESULT:", xx, yy, zz)

                            # xx = sign_x * new_beac[letters[ret_x]] + real_position_of_relative_beacon[0]
                            # yy = sign_y * new_beac[letters[ret_y]] + real_position_of_relative_beacon[1]
                            # zz = sign_z * new_beac[letters[ret_z]] + real_position_of_relative_beacon[2]

                            all_existing_beacons.append((new_xx, new_yy, new_zz))

                        print("ALL EXISTING BEACONS FOUND:")
                        for x in all_existing_beacons:
                            print(f"{x[0]},{x[1]},{x[2]}")

                        # update data of newly located scanner, so it is up to date with real location data
                        for index, beacon in enumerate(scanners[searched_scanner_id]):
                            
                            xx = sign_x * beacon[0] + new_scanner_location[0]
                            yy = sign_y * beacon[1] + new_scanner_location[1]
                            zz = sign_z * beacon[2] + new_scanner_location[2]
                            
                            print("UPDATED BEACON:", beacon, "->", xx, yy, zz)

                            scanners[searched_scanner_id][index] = (xx, yy, zz)

                        # print(relative_for_current_scanner)
                        # print(relative_for_searched_scanner)

                        scanner_locations[searched_scanner_id] = new_scanner_location
                        scanner_identified = True
                        current_scanner_id = searched_scanner_id

                        print("\n--- SCANNER", searched_scanner_id, "(", scanner_locations[searched_scanner_id], ") ---")
                        for ss in scanners[searched_scanner_id]:
                            print(ss)
                        print("-----------------------")

                        break

                if scanner_identified:
                    identified_scanners += 1
                    break

            if scanner_identified:
                break

        if scanner_identified == False:
            current_scanner_id += 1
            while scanner_locations[current_scanner_id] == (None, None, None):
                current_scanner_id += 1
                if current_scanner_id >= len(scanners):
                    current_scanner_id = 0

    print("\n\nSCANER LOCATIONS:")
    for sl in scanner_locations:
        print(sl)

    print("\nALL EXISTING BEACONS FOUND:")
    for x in sorted(set(all_existing_beacons)):
        print(f"{x[0]},{x[1]},{x[2]}")
            
    return len(set(all_existing_beacons))

@timer_decorator
def Part2(data):

    possibilities = []

    # for xx in ['-', '']:
    #         for yy in ['-', '']:
    #             for x in ['x', 'y']:
    #                     for y in ['x', 'y']:
    #                         if x == y:
    #                             continue
    #                         possibilities.append(xx + x + ', ' + yy + y)
    for sign_x in ['-', '']:
            for sign_y in ['-', '']:
                for sign_zz in ['-', '']:
                    for x in ['x', 'y', 'z']:
                        for y in ['x', 'y', 'z']:
                            for z in ['x', 'y', 'z']:
                                if x == y or x == z or y == z:
                                    continue
                                possibilities.append(sign_x + x + ', ' + sign_y + y + ', ' + sign_zz + z)

    for poss in set(possibilities):
        print(poss)

    print(len(set(possibilities)))



    return 1

if __name__ == "__main__":

    # with open("input/day_19.txt") as file:
    # with open("input/day_19_2d.txt") as file:
    # with open("input/day_19_orientation.txt") as file:
    with open("input/day_19_3d.txt") as file:
        data = [line.rstrip() for line in file]

        scanners = []
        
        index = 0
        while index < len(data):
            if '-' in data[index]:
                scanner = []
                index += 1
                while index < len(data) and ',' in data[index]:

                    # num1, num2 = data[index].split(',')
                    # scanner.append([int(num1), int(num2)])

                    num1, num2, num3 = data[index].split(',')
                    scanner.append((int(num1), int(num2), int(num3)))

                    index += 1

                scanners.append(scanner)
            index += 1

        print("Part 1: ", Part1(scanners))
        # print("Part 2: ", Part2(scanners))
