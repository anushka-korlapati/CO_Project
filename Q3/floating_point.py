def binary_to_float(binary):
    # Check for special cases: 0, positive/negative infinity, and NaN
    if binary == '00000000':
        return 0.0
    elif binary == '01111000':
        return float('inf')
    elif binary == '11111000':
        return float('-inf')
    elif binary == '11111001':
        return float('nan')

    # Extract the sign, exponent, and mantissa bits
    exponent_bits = binary[0:3]
    mantissa_bits = binary[3:]

    # Calculate the bias for the exponent
    bias = 2**(3 - 1) - 1

    # Convert the exponent from binary to decimal
    exponent = int(exponent_bits, 2) - bias

    # Calculate the implicit leading 1 for the mantissa
    implicit_leading = 1.0

    # Convert the mantissa from binary to decimal
    mantissa = 0.0
    for i in range(len(mantissa_bits)):
        bit = int(mantissa_bits[i])
        mantissa += bit * (2**(-i - 1))

    # Combine the sign, exponent, and mantissa to get the final floating-point number
    result = implicit_leading * (1 + mantissa) * (2 ** exponent)

    return result


# Example usage
# binary_representation = '01111000'
# float_number = binary_to_float(binary_representation)
# print(float_number)


def float_to_binary(num):
    # Check for special cases: 0, positive/negative infinity, and NaN
    if num == 0:
        return '00000000'
    elif num == float('inf'):
        return '01111000'
    elif num == float('-inf'):
        return '11111000'
    elif num != num:  # NaN check
        return '11111001'

    # Check the sign of the number
    sign = '1' if num < 0 else '0'
    num = abs(num)

    # Convert the number to binary
    binary = ''
    exponent = 0

    if num < 1.0:
        while num < 1.0:
            num *= 2
            exponent -= 1
    else:
        while num >= 2.0:
            num /= 2
            exponent += 1

    # Calculate the bias for the exponent
    bias = 2**(3 - 1) - 1

    # Calculate the biased exponent value
    biased_exponent = exponent + bias

    # Convert the exponent to binary
    exponent_bits = bin(biased_exponent)[2:].zfill(3)

    # Convert the mantissa to binary
    mantissa_bits = ''
    fraction = num - 1.0  # Remove the implicit leading 1
    for i in range(5):
        fraction *= 2
        bit = int(fraction)
        mantissa_bits += str(bit)
        fraction -= bit

    # Combine the sign, exponent, and mantissa to get the final binary representation
    binary = exponent_bits + mantissa_bits

    return binary



# Example usage
num = 1.5
binary_representation = float_to_binary(num)
print(binary_representation)

