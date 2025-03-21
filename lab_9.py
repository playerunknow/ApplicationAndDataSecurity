import math
import random

def is_prime(n):
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime(bits):
    """Generate a prime number with specified number of bits"""
    while True:
        # Generate random number with specified bit length
        p = random.getrandbits(bits)
        # Ensure it's odd (all primes except 2 are odd)
        p |= 1
        if is_prime(p):
            return p

def gcd(a, b):
    """Calculate greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Calculate the modular multiplicative inverse using Extended Euclidean Algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return (gcd, y - (b // a) * x, x)

    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % phi

def generate_keypair(bits=8):
    """Generate RSA public and private key pair"""
    # Generate two distinct prime numbers
    p = generate_prime(bits)
    q = generate_prime(bits)

    # Ensure p and q are different
    while p == q:
        q = generate_prime(bits)

    # Calculate n = p * q
    n = p * q

    # Calculate Euler's totient function φ(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Calculate d such that (d * e) % φ(n) = 1
    d = mod_inverse(e, phi)

    # Return public and private key pairs
    return ((e, n), (d, n)), (p, q)

def encrypt(public_key, plaintext):
    """Encrypt a message using RSA algorithm"""
    e, n = public_key

    # Convert text to numbers and encrypt each character
    cipher = []
    for char in plaintext:
        # Convert character to number (using Unicode code point)
        m = ord(char)
        # Encrypt: c = m^e mod n
        c = pow(m, e, n)
        cipher.append(c)

    return cipher

def decrypt(private_key, ciphertext):
    """Decrypt a message using RSA algorithm"""
    d, n = private_key

    # Decrypt each number and convert back to text
    plaintext = ""
    for c in ciphertext:
        # Decrypt: m = c^d mod n
        m = pow(c, d, n)
        # Convert number back to character
        plaintext += chr(m)

    return plaintext

def main():
    # Your name and group for encryption
    name_group = "Петренко Іван ІС-23"

    # Generate RSA key pair
    key_pairs, primes = generate_keypair(bits=8)
    public_key, private_key = key_pairs
    p, q = primes

    # Print key information
    print(f"Генерація ключів RSA:")
    print(f"Прості числа p = {p}, q = {q}")
    print(f"Модуль n = p * q = {public_key[1]}")
    print(f"Функція Ейлера φ(n) = (p-1) * (q-1) = {(p-1) * (q-1)}")
    print(f"Відкритий ключ (e, n) = {public_key}")
    print(f"Закритий ключ (d, n) = {private_key}")

    # Encrypt the message
    encrypted_msg = encrypt(public_key, name_group)
    print(f"\nВихідний текст: {name_group}")
    print(f"Зашифрований текст (числа): {encrypted_msg}")

    # Decrypt the message
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print(f"Розшифрований текст: {decrypted_msg}")

    # Show encryption/decryption process for each character
    print("\nПокроковий процес шифрування/дешифрування:")
    print("-" * 60)
    print("| Символ | Unicode | Шифрування (m^e mod n) | Шифр | Дешифрування (c^d mod n) |")
    print("-" * 60)

    e, n = public_key
    d, n = private_key

    for char in name_group:
        m = ord(char)
        c = pow(m, e, n)
        m_decrypted = pow(c, d, n)
        print(f"| {char:^6} | {m:^7} | {m}^{e} mod {n} | {c:^5} | {c}^{d} mod {n} = {m_decrypted:^5} |")

    print("-" * 60)

if __name__ == "__main__":
    main()