def double_permutation_cipher(text, col_key, row_key):
    """
    Шифрує текст за допомогою алгоритму подвійних перестановок.

    Args:
        text: Текст для шифрування.
        col_key: Ключ для перестановки стовпців (список чисел).
        row_key: Ключ для перестановки рядків (список чисел).

    Returns:
        Зашифрований текст.
    """
    # Визначаємо розміри таблиці
    cols = len(col_key)
    rows = len(row_key)

    # Переконуємося, що довжина тексту відповідає розміру таблиці
    # Якщо текст коротший, доповнюємо його пробілами
    if len(text) < cols * rows:
        text += ' ' * (cols * rows - len(text))

    # Обрізаємо текст, якщо він довший за розмір таблиці
    text = text[:cols * rows]

    # Заповнюємо початкову таблицю
    original_table = []
    for i in range(rows):
        row = text[i * cols:(i + 1) * cols]
        original_table.append(list(row))

    # Перестановка стовпців
    after_col_permutation = [[''] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            after_col_permutation[i][col_key.index(j + 1) - 1] = original_table[i][j]

    # Перестановка рядків
    final_table = [[''] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            final_table[row_key.index(i + 1) - 1][j] = after_col_permutation[i][j]

    # Формування зашифрованого тексту
    encrypted_text = ''
    for i in range(rows):
        for j in range(cols):
            encrypted_text += final_table[i][j]

    return encrypted_text

# Приклад використання
text_to_encrypt = "Диннік Михайло Андрійович, група 12-341"
col_key = [2, 4, 1, 3]  # Ключ для перестановки стовпців
row_key = [4, 1, 2, 3]  # Ключ для перестановки рядків

encrypted_text = double_permutation_cipher(text_to_encrypt, col_key, row_key)
print("Зашифрований текст за алгоритмом подвійних перестановок:", encrypted_text)