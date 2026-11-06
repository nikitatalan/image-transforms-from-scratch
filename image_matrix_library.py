import math
from PIL import Image

#Part X

def matrix_addition(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if rows_A != rows_B or cols_A != cols_B:
        return "Matrix dimensions do not match"

    result = []
    for i in range(rows_A):
        row = []
        for j in range(cols_A):
            row.append(A[i][j] + B[i][j])
        result.append(row)

    return result


def matrix_substraction(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if rows_A != rows_B or cols_A != cols_B:
        return "Matrix dimensions do not match"

    result = []

    for i in range(rows_A):
        row = []
        for j in range(cols_A):
            row.append(A[i][j] - B[i][j])
        result.append(row)

    return result


def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        return "Matrix dimensions do not match"

    result = []
    for i in range(rows_A):
        row = []
        for j in range(cols_B):
            value = 0
            for k in range(cols_A):
                value += A[i][k] * B[k][j]
            row.append(value)
        result.append(row)

    return result


def matrix_transpose(A):
    rows_A = len(A)
    cols_A = len(A[0])

    result = []

    for i in range(cols_A):
        row = []
        for j in range(rows_A):
            row.append(A[j][i])
        result.append(row)

    return result


def scalar_multiplication(A, k):
    rows_A = len(A)
    cols_A = len(A[0])

    result = []

    for i in range(rows_A):
        row = []
        for j in range(cols_A):
            row.append(A[i][j] * k)
        result.append(row)

    return result

#Part Y

def image_to_matrix(image):

    image_rgb = image.convert("RGB")
    width, height = image_rgb.size
    matrix_red, matrix_green, matrix_blue = [], [], []

    for y in range(height):
        row_r, row_g, row_b = [], [], []
        for x in range(width):
            r, g, b = image_rgb.getpixel((x, y))
            row_r.append(r)
            row_g.append(g)
            row_b.append(b)
        matrix_red.append(row_r)
        matrix_green.append(row_g)
        matrix_blue.append(row_b)

    return matrix_red, matrix_green, matrix_blue


def matrix_to_image(matrix_red, matrix_green, matrix_blue):

    width, height = len(matrix_red[0]), len(matrix_red)

    image = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            r = int(max(0, min(255, matrix_red[y][x])))
            g = int(max(0, min(255, matrix_green[y][x])))
            b = int(max(0, min(255, matrix_blue[y][x])))
            image.putpixel((x, y), (r, g, b))
    return image


def rotate_matrix(matrix, point, angle_degrees):

    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rows, cols = len(matrix),len(matrix[0])
    cx, cy = point[0], point[1]

    #Step 1: rotate all 4 corners to find output canvas size
    corners = [(0, 0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)]
    rotated_x_values = []
    rotated_y_values = []
    for (x, y) in corners:
        dx = x - cx
        dy = y - cy
        rotated_x_values.append(cos_a * dx - sin_a * dy + cx)
        rotated_y_values.append(sin_a * dx + cos_a * dy + cy)

    #Find new borders of the grid and then new dimensions by subtracting min from max
    min_x = int(math.floor(min(rotated_x_values)))
    max_x = int(math.ceil(max(rotated_x_values)))
    min_y = int(math.floor(min(rotated_y_values)))
    max_y = int(math.ceil(max(rotated_y_values)))

    new_cols = max_x - min_x + 1
    new_rows = max_y - min_y + 1

    result = []
    for i in range(new_rows):
        result.append([0]*new_cols)
    #Step 2: fill the output pixel by pixel using inverse mapping

    for out_y in range(new_rows):
        for out_x in range(new_cols):
            #translate output pixel relative to the rotation center
            dx = out_x + min_x - cx
            dy = out_y + min_y - cy

            #rotate backwards (negate the angle) to find the source pixel
            src_x = int(round(cos_a * dx + sin_a * dy + cx))
            src_y = int(round(-sin_a * dx + cos_a * dy + cy))

            #copy pixel if it exists in the original image
            if 0 <= src_x < cols and 0 <= src_y < rows:
                result[out_y][out_x] = matrix[src_y][src_x]

    return result

def scale_matrix(matrix, scale_factor):

    if scale_factor <= 0:
        raise ValueError(f"Scale_factor must be > 0. Got: {scale_factor}")

    rows, cols = len(matrix), len(matrix[0])

    #Find new dimension values
    new_rows = int(round(rows * scale_factor))
    new_cols = int(round(cols * scale_factor))

    scale_inverse = 1.0 / scale_factor

    result = []
    for new_y in range(new_rows):
        row = []
        for new_x in range(new_cols):
            #Inverse mapping: multiply output coordinate by (1/s)
            src_xi = int(round(new_x * scale_inverse))
            src_yi = int(round(new_y * scale_inverse))
            src_xi = max(0, min(cols - 1, src_xi))
            src_yi = max(0, min(rows - 1, src_yi))
            row.append(matrix[src_yi][src_xi])
        result.append(row)

    return result


def skew_matrix(matrix, skew_x, skew_y):

    rows, cols = len(matrix), len(matrix[0])

    #Find new dimension values
    new_cols = cols + int(abs(skew_x) * rows)
    new_rows = rows + int(abs(skew_y) * cols)

    result = []
    for i in range(new_rows):
        result.append([0] * new_cols)

    for y in range(rows):
        for x in range(cols):
            #Calculate shift amounts
            x_shift = int(y * skew_x)
            y_shift = int(x * skew_y)
            #Find new coordinates new_x and new_y
            new_x = x + x_shift
            new_y = y + y_shift
            #Write values only if they are inside the grid
            if 0 <= new_x < new_cols and 0 <= new_y < new_rows:
                result[new_y][new_x] = matrix[y][x]

    return result

def transpose_matrix(matrix):
    return matrix_transpose(matrix)


def to_grayscale(matrix_red, matrix_green, matrix_blue):

    #Step 1: weight each channel with scalar_multiplication
    weighted_R = scalar_multiplication(matrix_red, 0.299)
    weighted_G = scalar_multiplication(matrix_green, 0.587)
    weighted_B = scalar_multiplication(matrix_blue, 0.114)

    #Step 2: sum the three weighted matrices with matrix_addition
    grey_float = matrix_addition(matrix_addition(weighted_R, weighted_G),weighted_B)

    #Step 3: round each value to the nearest integer and clamp to [0, 255]
    rows, cols = len(grey_float), len(grey_float[0])
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            grey = max(0, min(255, int(round(grey_float[i][j]))))
            row.append(grey)
        result.append(row)

    return result


def edge_detection(matrix):

    rows, cols = len(matrix), len(matrix[0])

    #Sobel kernels as flat (1 x 9) row matrices for matrix_multiplication
    Kx_flat = [[-1, 0, 1, -2, 0, 2, -1, 0, 1]]
    Ky_flat = [[-1, -2, -1, 0, 0, 0, 1, 2, 1]]

    result = []
    for i in range(rows):
        result.append([0] * cols)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):

            #Extract the 3x3 neighbourhood and flatten into a (9x1) matrix
            neighbourhood_flat = []
            for ki in range(3):
                for kj in range(3):
                    neighbourhood_flat.append([matrix[i + ki - 1][j + kj - 1]])
            #neighbourhood_flat is now a list of 9 single-element lists -> (9x1)

            #Using matrix_multiplication to compute the dot products, (1x9) * (9x1) = (1x1)
            Gx = matrix_multiplication(Kx_flat, neighbourhood_flat)[0][0]
            Gy = matrix_multiplication(Ky_flat, neighbourhood_flat)[0][0]

            magnitude = math.sqrt(Gx**2 + Gy**2)
            if magnitude > 128:
                result[i][j] = 256
            else:
                result[i][j] = 0

    return result

#main

def main():

    image_path = input("\nEnter the path to your image file: ").strip()
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"\n[Error] Could not find: '{image_path}' ")
        print("Check the file path and try again.")
        return

    matrix_red, matrix_green, matrix_blue = image_to_matrix(image)

    print("\nAvailable transformations:")
    print("1. Rotate")
    print("2. Scale")
    print("3. Skew")
    print("4. Transpose")
    print("5. Convert to Greyscale")
    print("6. Edge Detection")

    choice = input("\nEnter transformation number (1-6): ").strip()
    output_path = input("Enter output file path (e.g. output.png): ").strip()

    result_image = None

    if choice == "1":
        try:
            angle = float(input("Rotation angle in degrees: "))
            cx = float(input(f"Centre x (0 to {image.width - 1}): "))
            cy = float(input(f"Centre y (0 to {image.height - 1}): "))
        except ValueError:
            print("Please enter valid numbers.")
            return
        r = rotate_matrix(matrix_red, [cx, cy], angle)
        g = rotate_matrix(matrix_green, [cx, cy], angle)
        b = rotate_matrix(matrix_blue, [cx, cy], angle)
        result_image = matrix_to_image(r, g, b)

    elif choice == "2":
        try:
            factor = float(input("Enter a positive scale factor: "))
        except ValueError:
            print("Enter a valid number.")
            return
        r = scale_matrix(matrix_red, factor)
        g = scale_matrix(matrix_green, factor)
        b = scale_matrix(matrix_blue, factor)
        result_image = matrix_to_image(r, g, b)

    elif choice == "3":
        try:
            sx = float(input("Enter a horizontal skew factor: "))
            sy = float(input("Enter a vertical skew factor: "))
        except ValueError:
            print("Enter valid numbers.")
            return
        r = skew_matrix(matrix_red, sx, sy)
        g = skew_matrix(matrix_green, sx, sy)
        b = skew_matrix(matrix_blue, sx, sy)
        result_image = matrix_to_image(r, g, b)

    elif choice == "4":
        r = transpose_matrix(matrix_red)
        g = transpose_matrix(matrix_green)
        b = transpose_matrix(matrix_blue)
        result_image = matrix_to_image(r, g, b)

    elif choice == "5":
        grey = to_grayscale(matrix_red, matrix_green, matrix_blue)
        result_image = Image.new("L", (len(grey[0]), len(grey)))
        for y in range(len(grey)):
            for x in range(len(grey[0])):
                result_image.putpixel((x, y), grey[y][x])

    elif choice == "6":
        grey = to_grayscale(matrix_red, matrix_green, matrix_blue)
        edges = edge_detection(grey)
        result_image = Image.new("L", (len(edges[0]), len(edges)))
        for y in range(len(edges)):
            for x in range(len(edges[0])):
                result_image.putpixel((x, y), min(255, edges[y][x]))

    else:
        print(f"\n'{choice}' is not a valid option. Please choose 1-6.")
        return

    try:
        result_image.show()
        result_image.save(output_path)
        print(f"\nImage saved to: {output_path}")
    except:
        print(f"\nCould not save the image")

if __name__ == "__main__":
    main()
