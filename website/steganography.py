## referred https://thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python

import cv2
import numpy as np
import os

def to_binary(data):
    
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")
    
def encode(carrier, message, n_bits=1):
    
    image = cv2.imread(carrier)
    n_bytes = image.shape[0] * image.shape[1] * 3 * n_bits // 8
    if len(message) > n_bytes:
        raise ValueError(f"[!] Insufficient bytes ({len(message)}), need bigger image or less data.")
    
    if isinstance(message, str):
        message += "====="
    elif isinstance(message, bytes):
        message += b"====="
    data_index = 0
    binary_secret_data = to_binary(message)
    data_len = len(binary_secret_data)
    for bit in range(1, n_bits+1):
        for row in image:
            for pixel in row:
                r, g, b = to_binary(pixel)
                
                if data_index < data_len:
                    if bit == 1:    
                        pixel[0] = int(r[:-bit] + binary_secret_data[data_index], 2)
                    elif bit > 1:
                        pixel[0] = int(r[:-bit] + binary_secret_data[data_index] + r[-bit+1:], 2)
                    data_index += 1
                if data_index < data_len:
                    if bit == 1:
                        pixel[1] = int(g[:-bit] + binary_secret_data[data_index], 2)
                    elif bit > 1:
                        pixel[1] = int(g[:-bit] + binary_secret_data[data_index] + g[-bit+1:], 2)
                    data_index += 1
                if data_index < data_len:
                    if bit == 1:
                       
                        pixel[2] = int(b[:-bit] + binary_secret_data[data_index], 2)
                    elif bit > 1:
                      
                        pixel[2] = int(b[:-bit] + binary_secret_data[data_index] + b[-bit+1:], 2)
                    data_index += 1
                if data_index >= data_len:
                    break
    return image

def decode_file(image_name, n_bits=1, in_bytes=True):
    print("Decoding...")
    image = cv2.imread(image_name)
    binary_data = ""
    for bit in range(1, n_bits+1):
        for row in image:
            for pixel in row:
                r, g, b = to_binary(pixel)
                binary_data += r[-bit]
                binary_data += g[-bit]
                binary_data += b[-bit]
   
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
   
    if in_bytes:
        decoded_data = bytearray()
        for byte in all_bytes:
            decoded_data.append(int(byte, 2))
            if decoded_data[-5:] == b"=====":
                break
    else:
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                break
    return decoded_data[:-5]

