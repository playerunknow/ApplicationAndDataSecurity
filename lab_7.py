def gronsfeld_cipher(text, key):
    """
    Шифрує текст за допомогою шифру Гронсфельда.

    Args:
        text: Текст для шифрування.
        key: Числовий ключ у вигляді рядка.

    Returns:
        Зашифрований текст.
    """

    # Український алфавіт
    ukr_uppercase = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    ukr_lowercase = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

    encrypted_text = ""
    key_length = len(key)

    for i, char in enumerate(text):
        shift = int(key[i % key_length])  # Отримуємо зсув з ключа

        if char in ukr_uppercase:
            index = ukr_uppercase.find(char)
            encrypted_text += ukr_uppercase[(index + shift) % len(ukr_uppercase)]
        elif char in ukr_lowercase:
            index = ukr_lowercase.find(char)
            encrypted_text += ukr_lowercase[(index + shift) % len(ukr_lowercase)]
        elif '0' <= char <= '9':  # Шифруємо цифри
            shifted_char = str((int(char) + shift) % 10)
            encrypted_text += shifted_char
        else:
            encrypted_text += char  # Залишаємо інші символи без змін

    return encrypted_text

# Приклад використання
text_to_encrypt = "Диннік Михайло Андрійович, група 12-341"
key = "1945"

encrypted_text = gronsfeld_cipher(text_to_encrypt, key)
print("не зашифрований текст:", text_to_encrypt)
print("Зашифрований текст:", encrypted_text)