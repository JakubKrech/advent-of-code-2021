from utils.timer import timer_decorator
from copy import deepcopy

def GetNeighbourPixel(image, xx, yy):

    retVal = '.'
    if xx >= 0 and xx < len(image) and yy >= 0 and yy < len(image[0]):
        retVal = image[xx][yy]

    return retVal

def AddPadding(image, padding_size):
    
    new_image = []

    full_line_padding = ['.'] * (padding_size + len(image) + padding_size)
    
    # top padding
    for _ in range(padding_size):
        new_image.append(full_line_padding)

    # side padding around image
    for line in image:
        image_line_with_padding = ['.'] * padding_size
        image_line_with_padding += line
        image_line_with_padding += ['.'] * padding_size
        new_image.append(image_line_with_padding)

    # bottom padding
    for _ in range(padding_size):
        new_image.append(full_line_padding)

    return new_image

@timer_decorator
def EnhanceImage(i_e_algorithm, input_image, steps):

    image = AddPadding(input_image, 200)

    for step in range(steps):
        newImage = [['' for i in range(len(image))] for j in range(len(image[0]))]

        for x in range(0, len(image)):
            for y in range(0, len(image[0])):
                
                pixel_values = ''

                pixel_values += GetNeighbourPixel(image, x - 1, y - 1)
                pixel_values += GetNeighbourPixel(image, x - 1, y    )
                pixel_values += GetNeighbourPixel(image, x - 1, y + 1)
                pixel_values += GetNeighbourPixel(image, x    , y - 1)
                pixel_values += GetNeighbourPixel(image, x    , y    )
                pixel_values += GetNeighbourPixel(image, x    , y + 1)
                pixel_values += GetNeighbourPixel(image, x + 1, y - 1)
                pixel_values += GetNeighbourPixel(image, x + 1, y    )
                pixel_values += GetNeighbourPixel(image, x + 1, y + 1)

                binary_number_string = ''

                for pixel in pixel_values:
                    binary_number_string += '1' if pixel == '#' else '0'

                number = int(binary_number_string, 2)
                newChar = i_e_algorithm[number % 512]

                newImage[x][y] = newChar

        image = deepcopy(newImage)

    counter = 0
    for xx in range(130, len(image) - 130):
        for yy in range(130, len(image[0]) - 130):
            if image[xx][yy] == '#':
                counter += 1

    return counter

if __name__ == "__main__":
    with open("input/day_20.txt") as file:    
        data = [s.rstrip() for s in file]

        i_e_algorithm = data[0]

        input_image = data[2:]
        for index, line in enumerate(input_image):
            input_image[index] = list(line)
        
        print("Part 1:", EnhanceImage(i_e_algorithm, input_image, 2))
        print("Part 2:", EnhanceImage(i_e_algorithm, input_image, 50))
    