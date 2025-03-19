def double_transposition_encrypt(text, column_key, row_key):
    # Удаляем пробелы для более чистого шифрования
    text = text.replace(" ", "")

    # 1. Определение размеров таблицы
    cols = len(column_key)
    rows = (len(text) + cols - 1) // cols  # Вычисление количества строк

    # 2. Создание и заполнение таблицы
    table = [['' for _ in range(cols)] for _ in range(rows)]
    text_index = 0
    for r in range(rows):
        for c in range(cols):
            if text_index < len(text):
                table[r][c] = text[text_index]
                text_index += 1
            else:
                table[r][c] = 'X'  # Заполнитель

    # 3. Перестановка столбцов
    column_order = [int(x) - 1 for x in column_key]  # Преобразование ключей в индексы
    reordered_table = [['' for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for i, col_index in enumerate(column_order):
            reordered_table[r][i] = table[r][col_index]
    table = reordered_table

    # 4. Перестановка строк
    row_order = [int(x) - 1 for x in row_key]  # Преобразование ключей в индексы
    reordered_table = [['' for _ in range(cols)] for _ in range(rows)]
    for i, row_index in enumerate(row_order):
        reordered_table[i] = table[row_index]
    table = reordered_table

    # 5. Чтение зашифрованного текста
    encrypted_text = ''.join(''.join(row) for row in table)

    return encrypted_text


def double_transposition_decrypt(encrypted_text, column_key, row_key):
    # 1. Определение размеров таблицы
    cols = len(column_key)
    rows = (len(encrypted_text) + cols - 1) // cols

    # 2. Восстановление таблицы
    table = [['' for _ in range(cols)] for _ in range(rows)]
    text_index = 0
    for r in range(rows):
        for c in range(cols):
            if text_index < len(encrypted_text):
                table[r][c] = encrypted_text[text_index]
                text_index += 1

    # 3. Обратная перестановка строк
    row_order = [int(x) - 1 for x in row_key]
    reordered_table = [['' for _ in range(cols)] for _ in range(rows)]
    for i, row_index in enumerate(row_order):
        reordered_table[row_index] = table[i]
    table = reordered_table

    # 4. Обратная перестановка столбцов
    column_order = [int(x) - 1 for x in column_key]
    reordered_table = [['' for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for i, col_index in enumerate(column_order):
            reordered_table[r][col_index] = table[r][i]
    table = reordered_table

    # 5. Восстановление текста
    decrypted_text = ''.join(''.join(row) for row in table)

    # Удаление заполнителей 'X'
    decrypted_text = decrypted_text.rstrip('X')

    return decrypted_text


# Пример использования
if __name__ == "__main__":
    # Исходный текст
    text_to_encrypt = "Диннік Михайло Андрійович, група 12-341"
    column_key = "2413"
    row_key = "4123"

    # Шифрование
    encrypted_text = double_transposition_encrypt(text_to_encrypt, column_key, row_key)
    print("Зашифрованный текст:", encrypted_text)

    # Расшифровка
    decrypted_text = double_transposition_decrypt(encrypted_text, column_key, row_key)
    print("Расшифрованный текст:", decrypted_text)