# ========================
# BIBLIOTECAS
# ========================
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import sys

# =========================
# FUNÇÕES
# =========================
def digitar(texto, delay=0.02):
    for c in texto:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def loading(texto, tempo=2):
    print(texto, end='', flush=True)
    for _ in range(tempo * 3):
        print(".", end='', flush=True)
        time.sleep(0.3)
    print()

def linha():
    print("=" * 60)

def barra(atual, total):
    largura = 30
    progresso = int((atual / total) * largura)
    bar = "#" * progresso + "-" * (largura - progresso)
    percent = (atual / total) * 100
    print(f"\r[{bar}] {percent:.1f}%", end="")

def estimativa(bits):
    tentativas = 2 ** bits
    tps = 1_000_000_000
    anos = tentativas / tps / (60 * 60 * 24 * 365)

    if anos > 1e12:
        return f"{anos/1e12:,.2f} trilhões de anos (impraticável)"
    elif anos > 1e9:
        return f"{anos/1e9:,.2f} bilhões de anos (impraticável)"
    elif anos > 1e6:
        return f"{anos/1e6:,.2f} milhões de anos"
    else:
        return f"{anos:,.2f} anos"

# =========================
# PARTE 1 - CHAVE FRACA
# =========================
linha()
digitar(">>> DEMONSTRACAO 1: CHAVE FRACA <<<", 0.04)
linha()

mensagem1 = input("\nDigite uma mensagem: ").encode()

loading("\nGerando chave fraca", 2)
chave_fraca = b'\x01\x02' * 8

loading("Inicializando AES", 2)
cipher = AES.new(chave_fraca, AES.MODE_ECB)

loading("Criptografando mensagem", 2)
ciphertext = cipher.encrypt(pad(mensagem1, AES.block_size))

digitar(f"\nMensagem criptografada (HEX): {ciphertext.hex()}", 0.005)

# =========================
# BRUTE FORCE
# =========================
linha()
print("\n")
input(">>> Pressione [ENTER] para iniciar o ataque de Brute Force <<<")
digitar("\nIniciando ataque brute force...", 0.04)

inicio = time.time()
total = 256 * 256
tentativas = 0

for i in range(256):
    for j in range(256):
        tentativa = bytes([i, j]) * 8
        tentativas += 1

        if tentativas % 2000 == 0:
            barra(tentativas, total)

        try:
            cipher_test = AES.new(tentativa, AES.MODE_ECB)
            texto = unpad(cipher_test.decrypt(ciphertext), AES.block_size)
            
            if texto == mensagem1:
                fim = time.time()
                print("\n")
                linha()
                digitar("CHAVE QUEBRADA!", 0.05)
                linha()
                digitar(f"Chave (HEX): {tentativa.hex()}", 0.01)
                digitar(f"Mensagem recuperada: {texto.decode()}", 0.02)
                digitar(f"Tempo: {fim - inicio:.2f} segundos", 0.02)
                break
        except:
            continue
    else:
        continue
    break

linha()
digitar("\n>>> ISSO SO FUNCIONA PORQUE A CHAVE E FRACA <<<", 0.04)

time.sleep(2)

# =========================
# PARTE 2 - CHAVE FORTE
# =========================
linha()
digitar("\n>>> DEMONSTRACAO 2: CHAVE FORTE <<<", 0.04)
linha()

mensagem2 = input("\nDigite outra mensagem: ").encode()

loading("\nGerando chave forte", 2)
chave_forte = get_random_bytes(16)

loading("Inicializando AES-128 (modo CBC)", 2)
cipher2 = AES.new(chave_forte, AES.MODE_CBC)

loading("Criptografando mensagem", 2)
ciphertext2 = cipher2.encrypt(pad(mensagem2, AES.block_size))

digitar(f"\nMensagem criptografada (HEX): {ciphertext2.hex()}", 0.005)

# =========================
# IMPOSSIBILIDADE DE QUEBRA
# =========================
linha()
print("\n")
input(">>> Pressione [ENTER] para iniciar o ataque de Brute Force <<<")
digitar("\nIniciando ataque brute force...", 0.04)
time.sleep(2)

digitar("\nAtaque inviavel detectado!", 0.05)
time.sleep(1)

tempo = estimativa(128)

digitar(f"\nTempo estimado para quebra: {tempo}", 0.04)

linha()
digitar("\n>>> NAO PODE SER QUEBRADO NA PRATICA <<< ", 0.05)
linha()
