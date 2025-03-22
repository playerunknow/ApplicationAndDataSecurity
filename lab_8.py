import numpy as np

# Таблиці для виконання операцій DES
# Початкова перестановка (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Кінцева перестановка (IP^-1)
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Розширення E
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Перестановка P
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S-блоки
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Таблиця для перестановки зі стисненням (перестановка PC-1)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Таблиця для утворення ключів для кожного раунда (перестановка PC-2)
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

# Кількість зсувів для кожного раунду
SHIFT_LEFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def string_to_bit_array(text):
    """Перетворює текст у масив бітів (в бінарному форматі)"""
    # Перетворюємо текст у байти з кодуванням utf-8
    text_bytes = text.encode('utf-8')
    array = []
    for byte in text_bytes:
        # Перетворення байту у 8-бітовий код
        bin_val = bin(byte)[2:].zfill(8)
        # Додавання кожного біту у масив
        for bit in bin_val:
            array.append(int(bit))
    return array

def bit_array_to_string(array):
    """Перетворює масив бітів у текст"""
    # Збираємо байти з бітів
    bytes_array = bytearray()
    for i in range(0, len(array), 8):
        # Беремо 8 бітів і перетворюємо їх у байт
        byte = array[i:i+8]
        if len(byte) == 8:  # Перевіряємо, що маємо повний байт
            byte_val = int(''.join([str(bit) for bit in byte]), 2)
            bytes_array.append(byte_val)

    # Декодуємо байти назад у текст з utf-8
    try:
        return bytes_array.decode('utf-8')
    except UnicodeDecodeError:
        # Якщо виникає помилка декодування, повертаємо доступну частину або порожній рядок
        for i in range(len(bytes_array), 0, -1):
            try:
                return bytes_array[:i].decode('utf-8')
            except UnicodeDecodeError:
                continue
        return ""

def permute(block, table):
    """Виконує перестановку бітів згідно з таблицею"""
    return [block[x-1] for x in table]

def split(block):
    """Розділяє блок на дві рівні частини"""
    return block[:len(block)//2], block[len(block)//2:]

def xor(a, b):
    """Виконує операцію XOR (побітове додавання за модулем 2) над двома масивами бітів"""
    return [a[i] ^ b[i] for i in range(len(a))]

def shift_left(block, count):
    """Циклічний зсув бітів вліво на вказану кількість позицій"""
    return block[count:] + block[:count]

def generate_subkeys(key):
    """Генерує 16 підключів для 16 раундів алгоритму DES"""
    # Конвертація ключа у 64-бітний масив
    key_bit_array = string_to_bit_array(key)

    # Якщо ключ коротший за 8 байт (64 біти), доповнюємо його нулями
    if len(key_bit_array) < 64:
        key_bit_array = key_bit_array + [0] * (64 - len(key_bit_array))
    # Якщо ключ довший за 8 байт, обрізаємо його
    elif len(key_bit_array) > 64:
        key_bit_array = key_bit_array[:64]

    # Перестановка PC1 (стискає ключ з 64 до 56 бітів)
    key_56 = permute(key_bit_array, PC1)

    # Розділення на ліву і праву частини
    left, right = split(key_56)

    # Генерація 16 підключів
    subkeys = []
    for i in range(16):
        # Зсув вліво
        left = shift_left(left, SHIFT_LEFT[i])
        right = shift_left(right, SHIFT_LEFT[i])

        # Об'єднання частин та перестановка PC2 (від 56 до 48 бітів)
        combined = left + right
        subkey = permute(combined, PC2)

        subkeys.append(subkey)

    return subkeys

def f_function(right_block, subkey):
    """Функція f в алгоритмі DES"""
    # Розширення 32-бітного блоку до 48 бітів
    expanded = permute(right_block, E)

    # XOR розширеного блоку з підключем
    xor_result = xor(expanded, subkey)

    # Застосування S-блоків (із 48 бітів у 32 біти)
    s_box_output = []
    for i in range(8):
        # Беремо 6 бітів для поточного S-блоку
        current_6_bits = xor_result[i*6:(i+1)*6]

        # Обчислюємо рядок і стовпчик для S-блоку
        row = int(str(current_6_bits[0]) + str(current_6_bits[5]), 2)
        col = int(''.join([str(bit) for bit in current_6_bits[1:5]]), 2)

        # Отримуємо значення з S-блоку
        val = S_BOXES[i][row][col]

        # Перетворюємо значення у 4-бітовий формат
        bin_val = bin(val)[2:].zfill(4)
        for bit in bin_val:
            s_box_output.append(int(bit))

    # Перестановка P
    return permute(s_box_output, P)

def des_encrypt_block(block, subkeys):
    """Шифрує один 64-бітний блок за допомогою алгоритму DES"""
    # Початкова перестановка
    block = permute(block, IP)

    # Розділення на ліву і праву частини
    left, right = split(block)

    # 16 раундів шифрування
    for i in range(16):
        # Зберігаємо попередню праву частину
        prev_right = right

        # Функція f
        f_result = f_function(right, subkeys[i])

        # XOR лівої частини з результатом функції f
        right = xor(left, f_result)

        # Нова ліва частина - попередня права частина
        left = prev_right

        # Для демонстрації виводимо результати першого раунду
        if i == 0:
            print(f"Після 1-го раунду:")
            print(f"Ліва частина: {''.join([str(bit) for bit in left])}")
            print(f"Права частина: {''.join([str(bit) for bit in right])}")

    # Фінальне об'єднання (у зворотному порядку: права + ліва)
    combined = right + left

    # Кінцева перестановка
    result = permute(combined, IP_INV)

    return result

def des_encrypt(text, key):
    """Шифрує текст за допомогою алгоритму DES у режимі ECB"""
    # Генеруємо підключі
    subkeys = generate_subkeys(key)

    # Конвертація тексту в бітовий масив
    text_bit_array = string_to_bit_array(text)

    # Доповнення масиву до кратності 64
    if len(text_bit_array) % 64 != 0:
        padding_length = 64 - (len(text_bit_array) % 64)
        text_bit_array = text_bit_array + [0] * padding_length

    result = []

    # Обробка тексту блоками по 64 біти
    for i in range(0, len(text_bit_array), 64):
        block = text_bit_array[i:i+64]
        result.extend(des_encrypt_block(block, subkeys))

    return result

def des_decrypt(cipher_bits, key):
    """Дешифрує текст, зашифрований алгоритмом DES"""
    # Генеруємо підключі (використовуємо їх у зворотному порядку для дешифрування)
    subkeys = generate_subkeys(key)
    subkeys.reverse()

    result = []

    # Обробка шифротексту блоками по 64 біти
    for i in range(0, len(cipher_bits), 64):
        block = cipher_bits[i:i+64]
        result.extend(des_encrypt_block(block, subkeys))

    # Видалення доповнення (якщо є)
    while result and result[-1] == 0:
        result.pop()

    return bit_array_to_string(result)

def print_bits_as_hex(bits):
    """Перетворює масив бітів у шістнадцятковий формат для відображення"""
    hex_output = ""
    for i in range(0, len(bits), 4):
        if i + 4 <= len(bits):  # Перевіряємо, що маємо повний ніббл
            nibble = bits[i:i+4]
            hex_digit = hex(int(''.join([str(bit) for bit in nibble]), 2))[2:]
            hex_output += hex_digit
    return hex_output

# Демонстрація роботи алгоритму
def demonstrate_des():
    # Використовуємо ваші дані
    plaintext = "Диннік Михайло Андрійович, група 12-341"
    # Ключ (рекомендується 8 символів для 64-бітного ключа)
    key = "secretky"

    print(f"Текст для шифрування: {plaintext}")
    print(f"Ключ: {key}")

    # Шифрування
    print("\nШифрування:")
    encrypted_bits = des_encrypt(plaintext, key)
    print(f"Зашифрований текст (HEX): {print_bits_as_hex(encrypted_bits)}")

    # Дешифрування
    print("\nДешифрування:")
    decrypted_text = des_decrypt(encrypted_bits, key)
    print(f"Розшифрований текст: {decrypted_text}")

    # Детальний аналіз першого раунду
    print("\nДетальний аналіз першого раунду:")
    # Конвертація тексту та ключа у бітові масиви
    text_bits = string_to_bit_array(plaintext)
    # Беремо перші 64 біти для аналізу
    if len(text_bits) < 64:
        text_bits = text_bits + [0] * (64 - len(text_bits))
    block_bits = text_bits[:64]

    # Генерація підключів
    subkeys = generate_subkeys(key)

    # Початкова перестановка
    initial_permutation = permute(block_bits, IP)
    print(f"Після початкової перестановки (IP): {print_bits_as_hex(initial_permutation)}")

    # Розділення на ліву і праву частини
    left, right = split(initial_permutation)
    print(f"Ліва частина (L0): {print_bits_as_hex(left)}")
    print(f"Права частина (R0): {print_bits_as_hex(right)}")

    # Розширення правої частини
    expanded_right = permute(right, E)
    print(f"Розширена права частина (E(R0)): {print_bits_as_hex(expanded_right)}")

    # XOR з підключем першого раунду
    xor_result = xor(expanded_right, subkeys[0])
    print(f"Результат XOR з підключем K1: {print_bits_as_hex(xor_result)}")

    # Застосування S-блоків
    s_box_output = []
    for i in range(8):
        current_6_bits = xor_result[i*6:(i+1)*6]
        row = int(str(current_6_bits[0]) + str(current_6_bits[5]), 2)
        col = int(''.join([str(bit) for bit in current_6_bits[1:5]]), 2)
        val = S_BOXES[i][row][col]
        bin_val = bin(val)[2:].zfill(4)
        for bit in bin_val:
            s_box_output.append(int(bit))
    print(f"Вихід S-блоків: {print_bits_as_hex(s_box_output)}")

    # Перестановка P
    p_result = permute(s_box_output, P)
    print(f"Результат перестановки P: {print_bits_as_hex(p_result)}")

    # Нова права частина
    new_right = xor(left, p_result)
    print(f"Нова права частина (R1): {print_bits_as_hex(new_right)}")

    # Нова ліва частина
    new_left = right
    print(f"Нова ліва частина (L1): {print_bits_as_hex(new_left)}")

# Запуск демонстрації
if __name__ == "__main__":
    demonstrate_des()