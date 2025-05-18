def gf_mult(a, b, poly=0x11b):
    """Galua maydonda ko'paytirish amali"""
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:
            a ^= poly
        b >>= 1
    return res

def gf_inverse(a, poly=0x11b):
    """Galua maydonda teskari elementni topish"""
    if a == 0:
        return 0
    for i in range(1, 256):
        if gf_mult(a, i, poly) == 1:
            return i
    return 0

def s_box_value(x):
    """Bir bayt uchun S-box qiymatini hisoblash"""
    if x == 0:
        return 0x63
    # Galua maydonda teskari element
    inv = gf_inverse(x)
    # Affin transformatsiya
    res = inv
    for _ in range(4):
        res = (res << 1) | (res >> 7)
    res ^= inv
    res ^= 0x63
    return res & 0xff

def generate_s_box():
    """S-box jadvalini yaratish"""
    s_box = [[0]*16 for _ in range(16)]
    for i in range(256):
        row = i // 16
        col = i % 16
        s_box[row][col] = s_box_value(i)
    return s_box

def print_s_box(s_box):
    """S-box ni chiroyli ko'rinishda chop etish"""
    print("S-box jadvali:")
    print("   ", end="")
    for i in range(16):
        print(f"{i:02X} ", end="")
    print("\n  +" + "-"*48)
    for i in range(16):
        print(f"{i:02X}|", end="")
        for j in range(16):
            print(f" {s_box[i][j]:02X}", end="")
        print()

# Asosiy dastur
if __name__ == "__main__":
    s_box = generate_s_box()
    print_s_box(s_box)
    
    # Test uchun bir nechta qiymatlar
    print("\nTest natijalari:")
    test_values = [0x00, 0x01, 0x12, 0x53, 0x7C, 0xFF]
    for val in test_values:
        row = val // 16
        col = val % 16
        print(f"0x{val:02X} -> 0x{s_box[row][col]:02X}")