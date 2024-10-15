# Langkah 1: Membuat matriks cipher Playfair
def create_matrix(key):
    """Membuat matriks 5x5 untuk Playfair Cipher berdasarkan kunci yang diberikan."""
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Huruf I/J dianggap sama
    used_chars = set()

    # Menghapus karakter duplikat dari kunci dan membangun matriks
    for char in key.upper():
        if char not in used_chars and char in alphabet:
            used_chars.add(char)
            matrix.append(char)

    # Menambahkan sisa huruf alfabet yang belum digunakan
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)

    # Mengubah daftar karakter menjadi matriks 5x5
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

# Langkah 2: Mencari posisi sebuah karakter dalam matriks
def find_position(matrix, char):
    """Mencari baris dan kolom dari sebuah karakter dalam matriks."""
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

# Langkah 3: Memisahkan teks menjadi digram (pasangan 2 huruf)
def split_digrams(text):
    """Memisahkan teks menjadi digram, menambahkan 'X' jika diperlukan."""
    text = text.replace("J", "I").replace(" ", "").upper()  # Mengubah J menjadi I dan menghapus spasi
    digrams = []
    i = 0

    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i + 1]
            if char1 == char2:  # Jika ada huruf berulang, sisipkan 'X'
                digrams.append((char1, 'X'))
                i += 1
            else:
                digrams.append((char1, char2))
                i += 2
        else:  # Jika jumlah huruf ganjil, tambahkan 'X' di akhir
            digrams.append((char1, 'X'))
            i += 1

    return digrams

# Langkah 4: Enkripsi sebuah digram menggunakan aturan Playfair
def encrypt_digram(matrix, digram):
    r1, c1 = find_position(matrix, digram[0])
    r2, c2 = find_position(matrix, digram[1])

    if r1 == r2:  # Jika berada di baris yang sama, geser ke kanan
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:  # Jika berada di kolom yang sama, geser ke bawah
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:  # Jika membentuk persegi, tukar kolom
        return matrix[r1][c2] + matrix[r2][c1]

# Langkah 5: Enkripsi seluruh plaintext menggunakan Playfair Cipher
def encrypt_playfair(plaintext, key):
    """Mengenkripsi plaintext menggunakan Playfair Cipher."""
    matrix = create_matrix(key)
    digrams = split_digrams(plaintext)
    encrypted_text = ''.join(encrypt_digram(matrix, digram) for digram in digrams)
    return encrypted_text

# Contoh penggunaan
if __name__ == "__main__":
    # Input
    key = "TEKNIK INFORMATIKA"
    plaintext_1 = "GOOD BROOM SWEEP CLEAN"
    plaintext_2 = "REDWOOD NATIONAL STATE PARK"
    plaintext_3 = "JUNK FOOD AND HEALTH PROBLEMS"

    # Proses Enkripsi
    encrypted_1 = encrypt_playfair(plaintext_1, key)
    encrypted_2 = encrypt_playfair(plaintext_2, key)
    encrypted_3 = encrypt_playfair(plaintext_3, key)

    # Hasil Enkripsi
    print("Hasil Enkripsi:")
    print(encrypted_1)
    print(encrypted_2)
    print(encrypted_3)
