import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    soma_diferencas = 0

    for i in range(6):
        diferenca = abs(as_a[i] - as_b[i])
        soma_diferencas += diferenca

    grau_similaridade = soma_diferencas / 6
    
    return grau_similaridade

def calcula_assinatura(texto):
    '''Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    sentencas = separa_sentencas(texto)
    if len(sentencas) == 0:
        return None

    total_palavras = 0
    total_caracteres_palavras = 0
    palavras_total = []
    total_caracteres_sentencas = 0
    total_frases = 0
    total_caracteres_frases = 0

    for sentenca in sentencas:
        frases = separa_frases(sentenca)
        total_frases += len(frases)
        total_caracteres_sentencas += len(sentenca)

        for frase in frases:
            palavras = separa_palavras(frase)
            total_palavras += len(palavras)
            palavras_total.extend(palavras)
            total_caracteres_frases += sum(len(palavra) for palavra in palavras)

    if total_palavras == 0 or total_frases == 0:
        return None
    
    tamanho_medio_palavra = total_caracteres_palavras / total_palavras if total_palavras > 0 else 0
    relacao_type_token = len(set(palavras_total)) / total_palavras if total_palavras > 0 else 0
    razao_hapax_legomena = n_palavras_unicas(palavras_total) / total_palavras if total_palavras > 0 else 0
    tamanho_medio_sentenca = total_caracteres_sentencas / len(sentencas) if len(sentencas) > 0 else 0
    complexidade_sentenca = total_frases / len(sentencas) if len(sentencas) > 0 else 0
    tamanho_medio_frase = total_caracteres_frases / len(palavras_total) if len(palavras_total) > 0 else 0

    return [tamanho_medio_palavra, relacao_type_token, razao_hapax_legomena, tamanho_medio_sentenca, complexidade_sentenca, tamanho_medio_frase]

def avalia_textos(textos, ass_cp):
    '''IMPLEMENTAR. Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    
    menor_similaridade = float('inf') 
    texto_mais_similar = -1
    
    for i, texto in enumerate(textos):
        assinatura_texto = calcula_assinatura(texto)
        
        if assinatura_texto is None:
            continue
        
        similaridade = compara_assinatura(assinatura_texto, ass_cp)
        
        if similaridade < menor_similaridade:
            menor_similaridade = similaridade
            texto_mais_similar = i + 1
    
    return texto_mais_similar

