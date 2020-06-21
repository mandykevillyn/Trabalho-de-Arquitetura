import sys

#criando um dicionário das instruções com o endereço em hexa e o respectivo operando, 
# que pode ser: byte, varnum, const, index, offset, disp

instrucoes = {  'nop': [0x01, []],
                'iadd': [0x02, []],
                'isub': [0x05, []],
                'iand': [0x08, []],
                'ior': [0x0B, []],
                #'dup': [0x0E, []],
                #'pop': [0x10, []],
                #'swap': [0x13, []],
                'bipush': [0x19, ['byte']],
                'iload': [0x1C, ['varnum']],
                'istore': [0x22, ['nova_varnum']],
                #'wide': [0x28, []],
                #'ldc_w': [0x32, ['index']],
                #'iinc': [0x36, ['varnum', 'const']],
                'goto': [0x3C, ['offset']],
                #'iflt': [0x43, ['offset']],
                #'ifeq': [0x47,['offset']],
                'if_icmpeq': [0x4B, ['offset']],
                #'invokevirtual': [0x55, ['disp']],
                #'ireturn': [0x6B, []]
}
#as instruções comentadas talvez não sejam compativeis com 

labels = {} #aqui teremos um dicionário contendo as labels e os seus endereços
variaveis = {} #aqui teremos um dicionário das variáveis e os endereços 
lista_bytes = [] #basicamente, uma lista de endereços (de labels, variaveis, instruções e operandos)
contador_bytes = 0 #contador de bytes
contador_variaveis = 0 #contador de variáveis

def adicionar_label(palavra):
    if palavra not in variaveis and palavra not in labels:
        labels[palavra] = contador_bytes +1 #adiciono no dicionario o "endereço" em que a label aparece para depois calcular a distancia

def adicionar_instrucao (instrucao):
    global contador_bytes
    lista_bytes.append(instrucoes[instrucao][0])
    contador_bytes += 1

def adicionar_operando(operando, tipo_operando, numero_operandos):
    global contador_bytes, contador_variaveis
    for i in range(0, numero_operandos, 1):
        if tipo_operando[i] == "varnum":
            lista_bytes.append(variaveis[operando[i]])
            contador_bytes += 1

        elif tipo_operando[i] == "nova_varnum":
            if operando[i] not in variaveis.keys():
                variaveis[operando[i]] = contador_variaveis
                contador_variaveis += 1
            lista_bytes.append(variaveis[operando[i]])
            contador_bytes +=1
        
        elif tipo_operando[i] ==  "byte" or tipo_operando[i] == "const":
            lista_bytes.append(int(operando[i]))
            contador_bytes += 1
        
        elif tipo_operando[i] == "disp" or tipo_operando[i] == "index": 
            lista_bytes.append(int(operando[i]))
            contador_bytes += 2

        else: #no caso de offsets ele adiciona o contador de bytes para depois podermos calcular a distância
            lista_bytes.append([operando[i], contador_bytes])
            contador_bytes += 2

def criar_arquivo():
    global contador_bytes
    #nessa função temos que gravar os bytes no arquivo, incluindo os bits de inicialização
    bytes_gravacao = bytearray()    # array de bytes que será escrita no arquivo
    tamanho_arquivo = (contador_bytes + 20).to_bytes(4, "little", signed = True) 
    # os primeiros 4 bits do arquivo é o tamanho dele
    bytes_gravacao += tamanho_arquivo
    inicializacao = [0x7300, 0x0006, 0x1001, 0x0400, 0x1001 + len(variaveis.keys())] 
    # bytes pré-definidos de inicialização, explicados na aula 14

    for byte in inicializacao: #adicionando os bytes de inicialização no array de gravação
        bytes_gravacao += byte.to_bytes(4, "little", signed = True)

    for byte in lista_bytes: #agora gravando o nosso programa no array de gravação
        if type(byte) == list: #caso o operando seja offset, ele será uma lista
            distancia_offset = labels[byte[0]] - byte[1] #calculei a distancia para ter o endereço do offset
            bytes_gravacao += distancia_offset.to_bytes(2, "big", signed = True) 
            #na aula 14 é avisado que há um problema com operandos de desvio e eles são salvos em big endian
        
        else: #caso nao seja label, é adicionado ao array para gravação
                bytes_gravacao.append(byte)

    #agora temos que gerar o arquivo 
    print(bytes_gravacao)
    arquivo = open(sys.argv[1][:-4] + ".exe", 'wb')
    arquivo.write(bytes_gravacao)
    arquivo.close()

################################## começando o main #########################################


txt = open(sys.argv[1], 'r')

for linha in txt:
        linha_lista = linha.lower().split()    # se dê errado vê isso aqui, falta o try
        print(linha_lista)
        if linha_lista[0] not in instrucoes:                      # vai checar se a linha possui label
            adicionar_label(linha_lista[0])                         # se possuir, label é adicionada ao seu dicionario
            del linha_lista[0]
        if linha_lista != []:
            instrucao = linha_lista[0]

            if instrucao in instrucoes:
                tipo_operando = instrucoes[instrucao][1]
                numero_operandos = len(tipo_operando)
                operando = linha_lista[1 : numero_operandos + 1]
                
                adicionar_instrucao(instrucao)
                adicionar_operando(operando, tipo_operando, numero_operandos) 

txt.close()

criar_arquivo()
