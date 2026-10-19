import math

# Parameters
TOTAL_SAMPLES = 4096  # Full period quantization
TABLE_SIZE = 512      # First eighth (4096 / 8)
FRACTIONAL_BITS = 15
MAX_VALUE = 32767     # 2^15 - 1 (represents ~0.999...)
MIN_VALUE = -32768    # -2^15 (represents -1)

# Generate lookup table
sine_lut = []

for i in range(TABLE_SIZE):
    # Calculate angle for this sample
    # Full period is 2*pi over 4096 samples
    # First eighth is pi/4 over 512 samples
    angle = (i / TOTAL_SAMPLES) * 2 * math.pi
    
    # Calculate sine value
    sine_value = math.sin(angle)
    
    # Quantize to 15 fractional bits
    # Map [-1, 1] to [-32768, 32767]
    quantized = int(round(sine_value * MAX_VALUE))
    
    # Clamp to valid range
    quantized = max(MIN_VALUE, min(MAX_VALUE, quantized))
    
    sine_lut.append(quantized)

# Print the lookup table
print(f"/* Sine wave lookup table - First eighth (0 to pi/4) */")
print(f"/* {TABLE_SIZE} samples, 15 fractional bits */")
print(f"/* Time step: (1/4096) * 2π per sample */")
print(f"const int16_t sine_lut[{TABLE_SIZE}] = {{")

# Format output in rows of 8 values
for i in range(0, TABLE_SIZE, 8):
    row = sine_lut[i:i+8]
    formatted_row = ", ".join(f"{val:6d}" for val in row)
    if i + 8 < TABLE_SIZE:
        print(f"    {formatted_row},")
    else:
        print(f"    {formatted_row}")

print("};")

# Print some verification info
print(f"\n/* Verification: */")
print(f"/* First value (sin(0)): {sine_lut[0]} (should be ~0) */")
print(f"/* Last value (sin(π/4)): {sine_lut[-1]} (should be ~{int(round(math.sin(math.pi/4) * MAX_VALUE))}) */")
print(f"/* Middle value: {sine_lut[TABLE_SIZE//2]} */")

# Print the lookup function
print("\n")
print("/* Sine lookup function */")
print("/* Input: phase from 0 to 4095 */")
print("/* Output: sine value with 15 fractional bits */")
print("int16_t sine_lookup(uint16_t phase) {")
print("    uint16_t octant = phase >> 9;  /* Divide by 512 to get octant (0-7) */")
print("    uint16_t index = phase & 0x1FF;  /* Modulo 512 to get index within octant */")
print("    int16_t value;")
print("    ")
print("    switch(octant) {")
print("        case 0:  /* 0 to π/4: direct lookup */")
print("            value = sine_lut[index];")
print("            break;")
print("        case 1:  /* π/4 to π/2: reverse lookup */")
print("            value = sine_lut[511 - index];")
print("            break;")
print("        case 2:  /* π/2 to 3π/4: reverse lookup */")
print("            value = sine_lut[511 - index];")
print("            break;")
print("        case 3:  /* 3π/4 to π: direct lookup */")
print("            value = sine_lut[index];")
print("            break;")
print("        case 4:  /* π to 5π/4: direct lookup, negate */")
print("            value = -sine_lut[index];")
print("            break;")
print("        case 5:  /* 5π/4 to 3π/2: reverse lookup, negate */")
print("            value = -sine_lut[511 - index];")
print("            break;")
print("        case 6:  /* 3π/2 to 7π/4: reverse lookup, negate */")
print("            value = -sine_lut[511 - index];")
print("            break;")
print("        case 7:  /* 7π/4 to 2π: direct lookup, negate */")
print("            value = -sine_lut[index];")
print("            break;")
print("        default:")
print("            value = 0;  /* Should never happen */")
print("            break;")
print("    }")
print("    ")
print("    return value;")
print("}")
