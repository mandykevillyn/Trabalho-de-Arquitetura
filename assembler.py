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

def adicionar_label(palavra):
    if palavra not in variaveis and palavra not in labels:
        labels[palavra] = contador_bytes +1



################################## começando o main #########################################

labels = {} #aqui teremos um dicionário contendo as labels e os seus endereços
variaveis = {} #aqui teremos um dicionário das variáveis e os endereços 
lista_bytes = [] #basicamente, uma lista de endereços (de labels, variaveis, instruções e operandos)

contador_bytes = 0 #contador de bytes
contador_variaveis = 0 #contador de variáveis


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

                if checar_operando_valido(instrucao, operando, tipo_operando, numero_operandos):
                    add_instrucao(instrucao)
                    add_operando(instrucao, operando, tipo_operando, numero_operandos) 

txt.close()

criar_arquivo()
