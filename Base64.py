import numpy as np
import sys

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8-len(bits)):
                bits.insert(0,0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr

def converter_6bit_para_8bit(texto):
    binario = gerar_mensagem(texto)
    contador = 0
    binario_temporario = [0,0]
    binario_retornavel = []

    for i in  range(len(binario)):
        contador = contador + 1
        binario_temporario.append(binario[i])
        if contador >= 6:
            binario_retornavel += binario_temporario
            contador = 0
            binario_temporario = [0,0]
    if contador != 0:
        while contador < 6:
            contador = contador + 1
            binario_temporario.append(0)
        binario_retornavel += binario_temporario
    return binario_retornavel

def converter_binario_para_decimal(texto):
    somador = 128
    decimal_temporario = 0
    decimal_retornavel = []
    contador = 0
    binario_teporario = []
    binario = converter_6bit_para_8bit(texto)


    for i in range(len(binario)):
        binario_teporario.append(binario[i])
        contador = contador +1
        if contador > 7:
            for a in range(8):
                if binario_teporario[a] == 1:
                    decimal_temporario = decimal_temporario +somador
                somador = int(somador/2)
            contador = 0
            somador = 128
            decimal_retornavel.append(decimal_temporario)
            decimal_temporario = 0
            binario_teporario = []
    return  decimal_retornavel

def encode_Base_64(texto):
    tabela_de_converao_base64 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
    texto_encodado =  ""
    decimal = converter_binario_para_decimal(texto)
    for i in range(len(decimal)):
        indice = decimal[i]
        texto_encodado +=tabela_de_converao_base64[indice]

    if (len(texto)%3) == 1:
        texto_encodado += "=="
    elif (len(texto)%3) == 2:
        texto_encodado += "="
    return  texto_encodado

def converter_caracter_para_decimal(texto):
    tabela64 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
    decimal = []
    for i in range(len(texto)):
        for a in range(len(tabela64)):
            if texto[i]==tabela64[a]:
                decimal.append(a)
                break
    return decimal

def converter_decimal_para_binario(texto):
    binario = []
    binario_auxiliar = []
    decimal = converter_caracter_para_decimal(texto)
    contador = 0

    for i in range(len(decimal)):
        while decimal[i] > 0:
            if(decimal[i]%2)>0:
                binario_auxiliar.insert(0,1)
            else:
                binario_auxiliar.insert(0,0)
            contador = contador + 1
            decimal[i] = int(decimal[i]/2)
        while contador < 6:
            binario_auxiliar.insert(0,0)
            contador = contador + 1
        contador = 0
        binario += binario_auxiliar
        binario_auxiliar = []
    return  binario

def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i))
        mensagem_out += chr(sum)
    return mensagem_out

def decode_base64(texto):
    binario_6bits = converter_decimal_para_binario(texto)
    binario_8bits = []
    binario_auxiliar = []
    contador = 0
    for i in range(len(binario_6bits)):
        binario_auxiliar.append(binario_6bits[i])
        contador = contador + 1
        if contador > 7:
            binario_8bits += binario_auxiliar
            binario_auxiliar = []
            contador = 0

    mensagem = converter_mensagem(binario_8bits)


    return mensagem

def help():
    print("###############################################\n"
          "# Utilize o terminal para rodar o arquivo .py #\n"
          "#                                             #\n"
          "# -e = encoda                                 #\n"
          "# -d = decoda                                 #\n"
          "#                                             #\n"
          "# Exemplo de uso: $ python base_64 -e exemplo #\n"
          "###############################################")

if len(sys.argv) < 3:
    help()
elif sys.argv[1] == '-e':
    print(encode_Base_64(sys.argv[2]))
elif sys.argv[1] == '-d':
    print(decode_base64(sys.argv[2]))
else:
    help()

