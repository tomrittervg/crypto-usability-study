def make_full_mask(start_bit):
    if start_bit == 0:
        return 0xFF #shift me 2
    elif start_bit == 1:
        return 0x7F
    elif start_bit == 2:
        return 0x3F
    elif start_bit == 3:
        return 0x1F
    elif start_bit == 4:
        return 0x0F
    elif start_bit == 5:
        return 0x07
    elif start_bit == 6:
        return 0x03 #shift me 8
    elif start_bit == 7:
        return 0x01 #shift me 9
    else:
        raise Exception("Invalid start_bit")
def make_remainder_mask(start_bit):
    if start_bit == 0:
        return 0xC0 # shift me 6
    elif start_bit == 1:
        return 0x60 # shift me 5
    elif start_bit == 2:
        return 0x30 # shift me 4
    elif start_bit == 3:
        return 0x18 # shift me 3
    elif start_bit == 4:
        return 0x0C # shift me 2
    elif start_bit == 5:
        return 0x06 # shift me 1
    elif start_bit == 6:
        return 0x03 # shift me 0
    elif start_bit == 7:
        return 0x01 # shift me right 1
    else:
        raise Exception("Invalid start_bit")
        
def make_int(start_byte, start_bit, bytearray):
    """
    In theory this code works, but I'd rather not use it
    """
    indx = (ord(bytearray[start_byte]) & make_full_mask(start_bit)) << (start_bit+2)
    start_byte += 1
    start_bit = (start_bit + 8) % 8
    if start_bit != 7:
        indx += (ord(bytearray[start_byte]) & make_remainder_mask(start_bit)) >> (6-start_bit)
        start_bit = (start_bit + 2) % 8
    elif start_bit == 7:
        indx += (ord(bytearray[start_byte]) & make_remainder_mask(start_bit)) << 1 
        # One more byte
        start_byte += 1
        start_bit = (start_bit + 2) % 8
        indx += ord(bytearray[start_byte]) & 0x80
    return start_byte, start_bit, indx
