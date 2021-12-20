from utils.timer import timer_decorator

def DetectRotation(scanner1, scanner2):

    sign_x, sign_y, sign_z = None, None, None
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

                            if ammount_of_intersected >= 12:

                                letters = ['x', 'y', 'z']

                                ret_x = letters[x]
                                ret_y = letters[y]
                                ret_z = letters[z]

                                found = True

                                return found, sign_x, ret_x, sign_y, ret_y, sign_z, ret_z
    
    return found, sign_x, ret_x, sign_y, ret_y, sign_z, ret_z

def GetRelativeToBeacon(scanner, beacon_id):
    
    reference_beacon = scanner[beacon_id]
    beacons_relative_to_reference_beacon = []
    
    for beacon in scanner:
        if reference_beacon == beacon:
            continue

        relative_beacon = (beacon[0] - reference_beacon[0], beacon[1] - reference_beacon[1], beacon[2] - reference_beacon[2])
        beacons_relative_to_reference_beacon.append(relative_beacon)

    return beacons_relative_to_reference_beacon

@timer_decorator
def CalculateBeacons(scanners):

    scanner_locations = [(None, None, None)] * len(scanners)
    scanner_locations[0] = (0, 0, 0)
    ammount_of_scans_per_scanner = len(scanners[0])

    identified_scanners = 1
    current_scanner_id = 0

    while identified_scanners < len(scanner_locations):
        scanner_identified = False

        for searched_scanner_id in range(len(scanner_locations)):
            if scanner_locations[searched_scanner_id] != (None, None, None) or searched_scanner_id == current_scanner_id:
                continue

            for current_beacon_id in range(ammount_of_scans_per_scanner):
                relative_for_current_scanner = GetRelativeToBeacon(scanners[current_scanner_id], current_beacon_id)
                
                for searched_beacon_id in range(ammount_of_scans_per_scanner):
                    relative_for_searched_scanner = GetRelativeToBeacon(scanners[searched_scanner_id], searched_beacon_id)

                    found, sign_x, ret_x, sign_y, ret_y, sign_z, ret_z = DetectRotation(relative_for_current_scanner, relative_for_searched_scanner)

                    if found == True:

                        letters = {'x': 0, 'y': 1, 'z': 2}

                        relative_beacon = scanners[current_scanner_id][current_beacon_id]
                        searched_relative_beacon = scanners[searched_scanner_id][searched_beacon_id]

                        # get coordinates of identified scanner
                        ns_x = relative_beacon[0] - (sign_x *  searched_relative_beacon[letters[ret_x]])
                        ns_y = relative_beacon[1] - (sign_y *  searched_relative_beacon[letters[ret_y]])
                        ns_z = relative_beacon[2] - (sign_z *  searched_relative_beacon[letters[ret_z]])

                        new_scanner_location = (ns_x, ns_y, ns_z)
                        print("Location of scanner", searched_scanner_id, "found:", new_scanner_location)
                        scanner_locations[searched_scanner_id] = new_scanner_location

                        # update data of newly located scanner, so it is up to date with real location data
                        for index, beacon in enumerate(scanners[searched_scanner_id]):
                            
                            np_x = new_scanner_location[0] + (sign_x * beacon[letters[ret_x]])
                            np_y = new_scanner_location[1] + (sign_y * beacon[letters[ret_y]])
                            np_z = new_scanner_location[2] + (sign_z * beacon[letters[ret_z]])

                            new_point_location = (np_x, np_y, np_z)

                            scanners[searched_scanner_id][index] = new_point_location

                        scanner_identified = True
                        current_scanner_id = searched_scanner_id
                        break

                if scanner_identified:
                    identified_scanners += 1
                    break

            if scanner_identified:
                break

        if scanner_identified == False:
            current_scanner_id += 1

            if current_scanner_id >= len(scanners):
                    current_scanner_id = 0

            while scanner_locations[current_scanner_id] == (None, None, None):
                current_scanner_id += 1
                if current_scanner_id >= len(scanners):
                    current_scanner_id = 0

    all_existing_beacons = []
    for sc in scanners:
        for bc in sc:
            all_existing_beacons.append(bc)

    max_distance = 0
    for x in scanner_locations:
        for y in scanner_locations:
            if x == y:
                continue
            max_distance = max(max_distance, abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2]))
            
    return len(set(all_existing_beacons)), max_distance

if __name__ == "__main__":

    with open("input/day_19.txt") as file:
        data = [line.rstrip() for line in file]

        scanners = []
        
        index = 0
        while index < len(data):
            if '-' in data[index]:
                scanner = []
                index += 1
                while index < len(data) and ',' in data[index]:
                    num1, num2, num3 = data[index].split(',')
                    scanner.append((int(num1), int(num2), int(num3)))
                    index += 1

                scanners.append(scanner)
            index += 1

        ammount_of_beacons, max_distance = CalculateBeacons(scanners)    

        print("Part 1: ", ammount_of_beacons)
        print("Part 2: ", max_distance)
