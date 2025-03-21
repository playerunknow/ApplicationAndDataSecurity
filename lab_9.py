import math                                    # Імпорт модуля математичних функцій
import random                                  # Імпорт модуля для генерації випадкових чисел

def is_prime(n):                               # Функція перевірки чи є число простим
    """Check if a number is prime"""           # Документація: перевірка чи число просте
    if n <= 1:                                 # Якщо число менше або дорівнює 1
        return False                           # Повертаємо False (не є простим)
    if n <= 3:                                 # Якщо число менше або дорівнює 3
        return True                            # Повертаємо True (є простим)
    if n % 2 == 0 or n % 3 == 0:               # Якщо число ділиться на 2 або 3
        return False                           # Повертаємо False (не є простим)
    i = 5                                      # Встановлюємо початкове значення i
    while i * i <= n:                          # Поки квадрат i менше або дорівнює n
        if n % i == 0 or n % (i + 2) == 0:     # Якщо n ділиться на i або на i+2
            return False                       # Повертаємо False (не є простим)
        i += 6                                 # Збільшуємо i на 6
    return True                                # Якщо пройшли всі перевірки, число просте

def generate_prime(bits):                      # Функція генерації простого числа заданої бітової довжини
    """Generate a prime number with specified number of bits""" # Документація: генерація простого числа
    while True:                                # Нескінченний цикл
        # Generate random number with specified bit length           # Генеруємо випадкове число заданої бітової довжини
        p = random.getrandbits(bits)           # Генеруємо випадкове число заданої кількості бітів
        # Ensure it's odd (all primes except 2 are odd)             # Гарантуємо, що число непарне
        p |= 1                                 # Встановлюємо крайній біт в 1 (робимо число непарним)
        if is_prime(p):                        # Якщо число просте
            return p                           # Повертаємо згенероване просте число

def gcd(a, b):                                 # Функція обчислення найбільшого спільного дільника
    """Calculate greatest common divisor using Euclidean algorithm""" # Документація: обчислення НСД
    while b:                                   # Поки b не дорівнює 0
        a, b = b, a % b                        # Алгоритм Евкліда: заміна a на b, b на a % b
    return a                                   # Повертаємо НСД

def mod_inverse(e, phi):                       # Функція обчислення мультиплікативного оберненого за модулем
    """Calculate the modular multiplicative inverse using Extended Euclidean Algorithm""" # Документація: обчислення оберненого
    def extended_gcd(a, b):                    # Внутрішня функція: розширений алгоритм Евкліда
        if a == 0:                             # Базовий випадок: якщо a = 0
            return (b, 0, 1)                   # Повертаємо кортеж (b, 0, 1)
        else:                                  # Інакше
            gcd, x, y = extended_gcd(b % a, a) # Рекурсивний виклик функції
            return (gcd, y - (b // a) * x, x)  # Повертаємо кортеж з обчисленими значеннями

    gcd, x, y = extended_gcd(e, phi)           # Викликаємо розширений алгоритм Евкліда
    if gcd != 1:                               # Якщо НСД не дорівнює 1
        raise ValueError("Modular inverse does not exist") # Піднімаємо виняток: оберненого не існує
    else:                                      # Інакше
        return x % phi                         # Повертаємо обернене число за модулем phi

def generate_keypair(bits=8):                  # Функція генерації пари ключів RSA
    """Generate RSA public and private key pair""" # Документація: генерація ключової пари
    # Generate two distinct prime numbers                            # Генеруємо два різних простих числа
    p = generate_prime(bits)                   # Генеруємо перше просте число p
    q = generate_prime(bits)                   # Генеруємо друге просте число q

    # Ensure p and q are different                                  # Гарантуємо, що p і q різні
    while p == q:                              # Поки p дорівнює q
        q = generate_prime(bits)               # Генеруємо нове q, доки воно не буде відрізнятися від p

    # Calculate n = p * q                                           # Обчислюємо n = p * q
    n = p * q                                  # Обчислюємо n як добуток p і q

    # Calculate Euler's totient function φ(n) = (p-1) * (q-1)       # Обчислюємо функцію Ейлера φ(n)
    phi = (p - 1) * (q - 1)                    # Обчислюємо φ(n) = (p-1) * (q-1)

    # Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1         # Обираємо e (відкрита експонента)
    e = random.randrange(2, phi)               # Вибираємо випадкове e в діапазоні від 2 до phi
    while gcd(e, phi) != 1:                    # Поки НСД(e, phi) не дорівнює 1
        e = random.randrange(2, phi)           # Генеруємо нове e

    # Calculate d such that (d * e) % φ(n) = 1                      # Обчислюємо d (закрита експонента)
    d = mod_inverse(e, phi)                    # Обчислюємо d як мультиплікативно обернене до e за модулем phi

    # Return public and private key pairs                           # Повертаємо пари відкритого і закритого ключів
    return ((e, n), (d, n)), (p, q)            # Повертаємо кортеж з ключами і простими числами

def encrypt(public_key, plaintext):            # Функція шифрування повідомлення алгоритмом RSA
    """Encrypt a message using RSA algorithm""" # Документація: шифрування повідомлення
    e, n = public_key                          # Розпаковуємо відкритий ключ на e та n

    # Convert text to numbers and encrypt each character            # Перетворюємо текст на числа і шифруємо кожен символ
    cipher = []                                # Ініціалізуємо список для зашифрованих символів
    for char in plaintext:                     # Для кожного символу у вхідному тексті
        # Convert character to number (using Unicode code point)    # Конвертуємо символ у число (код Unicode)
        m = ord(char)                          # Отримуємо код Unicode для символу
        # Encrypt: c = m^e mod n                                    # Шифруємо: c = m^e mod n
        c = pow(m, e, n)                       # Обчислюємо c = m^e mod n
        cipher.append(c)                       # Додаємо зашифрований символ до списку

    return cipher                              # Повертаємо список зашифрованих символів

def decrypt(private_key, ciphertext):          # Функція дешифрування повідомлення алгоритмом RSA
    """Decrypt a message using RSA algorithm""" # Документація: дешифрування повідомлення
    d, n = private_key                         # Розпаковуємо закритий ключ на d та n

    # Decrypt each number and convert back to text                 # Дешифруємо кожне число і конвертуємо назад у текст
    plaintext = ""                             # Ініціалізуємо порожній рядок для розшифрованого тексту
    for c in ciphertext:                       # Для кожного зашифрованого символу
        # Decrypt: m = c^d mod n                                   # Дешифруємо: m = c^d mod n
        m = pow(c, d, n)                       # Обчислюємо m = c^d mod n
        # Convert number back to character                         # Конвертуємо число назад у символ
        plaintext += chr(m)                    # Додаємо символ до розшифрованого тексту

    return plaintext                           # Повертаємо розшифрований текст

def main():                                    # Головна функція програми
    # Your name and group for encryption                           # Ваше ім'я та група для шифрування
    name_group = "Петренко Іван ІС-23"         # Визначаємо текст для шифрування

    # Generate RSA key pair                                        # Генеруємо ключову пару RSA
    key_pairs, primes = generate_keypair(bits=8) # Генеруємо ключову пару з бітовою довжиною 8
    public_key, private_key = key_pairs        # Розпаковуємо ключову пару на відкритий і закритий ключі
    p, q = primes                              # Розпаковуємо прості числа p і q

    # Print key information                                        # Виводимо інформацію про ключі
    print(f"Генерація ключів RSA:")            # Виводимо заголовок
    print(f"Прості числа p = {p}, q = {q}")    # Виводимо прості числа p і q
    print(f"Модуль n = p * q = {public_key[1]}") # Виводимо модуль n
    print(f"Функція Ейлера φ(n) = (p-1) * (q-1) = {(p-1) * (q-1)}") # Виводимо значення функції Ейлера
    print(f"Відкритий ключ (e, n) = {public_key}") # Виводимо відкритий ключ
    print(f"Закритий ключ (d, n) = {private_key}") # Виводимо закритий ключ

    # Encrypt the message                                          # Шифруємо повідомлення
    encrypted_msg = encrypt(public_key, name_group) # Шифруємо текст
    print(f"\nВихідний текст: {name_group}")   # Виводимо вихідний текст
    print(f"Зашифрований текст (числа): {encrypted_msg}") # Виводимо зашифрований текст

    # Decrypt the message                                          # Дешифруємо повідомлення
    decrypted_msg = decrypt(private_key, encrypted_msg) # Дешифруємо текст
    print(f"Розшифрований текст: {decrypted_msg}") # Виводимо розшифрований текст

    # Show encryption/decryption process for each character        # Показуємо процес шифрування/дешифрування для кожного символу
    print("\nПокроковий процес шифрування/дешифрування:") # Виводимо заголовок
    print("-" * 60)                            # Виводимо роздільну лінію
    print("| Символ | Unicode | Шифрування (m^e mod n) | Шифр | Дешифрування (c^d mod n) |") # Виводимо заголовки стовпців
    print("-" * 60)                            # Виводимо роздільну лінію

    e, n = public_key                          # Розпаковуємо відкритий ключ
    d, n = private_key                         # Розпаковуємо закритий ключ

    for char in name_group:                    # Для кожного символу у тексті
        m = ord(char)                          # Отримуємо код Unicode символу
        c = pow(m, e, n)                       # Шифруємо символ
        m_decrypted = pow(c, d, n)             # Дешифруємо символ
        print(f"| {char:^6} | {m:^7} | {m}^{e} mod {n} | {c:^5} | {c}^{d} mod {n} = {m_decrypted:^5} |") # Виводимо інформацію про процес

    print("-" * 60)                            # Виводимо роздільну лінію

if __name__ == "__main__":                     # Якщо файл запущено як основний скрипт
    main()                                     # Викликаємо головну функцію