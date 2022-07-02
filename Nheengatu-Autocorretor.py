"""
Autocorretor para Nheengatu.
Autor: Pedro Borges
"""
import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter

def main():
    #  Leitura inicial de dados
    palavras = carregarDados()
    V = set(palavras)
    contagemDados(palavras, V)

    #  Funções auxiliares
    frequenciaPorPalavra = medidaFrequencia(palavras)
    probabilidades = probabilidadeDeOcorrencia(palavras, frequenciaPorPalavra)

    #  Análise da palavra
    userInput = input("Digite a palavra: ")
    print(autocorretor(userInput, V, frequenciaPorPalavra, probabilidades))
    print()

def carregarDados():
    """
    Propósito: Essa função carrega a corpora da língua.
    Parâmetros: file (type: string)-- o documento com as palavras a serem
        carregadas.
    Return: nenhum.
    """
    with open('/Users/pedroborges/Documents/Atom/Nheengatu/corpus.txt', 'r') as f:
        file_name_data = f.read()
        file_name_data = file_name_data.lower()
        regex = '\w+'
        words = re.findall(regex, file_name_data)
        return(words)

def contagemDados(words, vocab):
    """
    Propósito: Imprimir primeiros detalhes dos dados.
    Parâmetros: words (tipo: lista)-- a lista de palavras lidas; vocab (tipo:
        set)-- o conjunto gerado das palavras.
    Return: nenhum.
    """
    print()
    print("--------------- Análise de corpora ---------------")
    print()
    print(f"- As dez primeiras palavras do texto são: \n{words[0:10]}")
    print(f"- Há {len(vocab)} palavras únicas no vocabulário.")
    print()

def medidaFrequencia(words):
    """
    Propósito: Essa função conta a ocorrência de cada palavra no vocabulário e
        armaneza a contagem num conjunto.
    Parâmetros: palavras (tipo: lista)-- as palavras existentes na língua.
    Return: frequenciaPalavras (tipo: set)-- frequência de cada palavra na
        corpora da língua.
    """
    frequenciaPalavras = {}
    frequenciaPalavras = Counter(words)
    print("------------- Frequência das palavras -------------")
    print()
    print(frequenciaPalavras.most_common()[0:10])
    print()
    print("--------------------------------------------------")
    print()
    return(frequenciaPalavras)

def probabilidadeDeOcorrencia(words, frequenciaPalavras):
    """
    Propósito: Essa função computa a probabilidade de ocorrência de cada palavra
        do vocabulário. O cálculo traça as frequências relativas de cada palavra.
    Parâmetros: words (tipo: lista)-- a lista de palavras existentes;
        frequenciaPalavras (tipo: set)-- conjunto (vocabulário).
    Return: probabilidades (tipo: set)-- conjunto contendo a probabilidade de
        ocorrência de cada palavra.
    """
    probabilidades = {}
    Total = sum(frequenciaPalavras.values())
    for i in frequenciaPalavras.keys():
        probabilidades[i] = frequenciaPalavras[i]/Total
    return(probabilidades)

def autocorretor(input_word, vocab, word_freq_dict, probs):
    """
    Propósito: Essa função checa se o input possui uma ortografia correta ou não.
    Parâmetros: input_word (tipo: str)-- a palavra a ser analisada.
    Return: Varia dependendo da equivalência da palavra. Pode ser uma string
        (ortografia exata/correta) ou um dataframe (ortografia incorreta).
    """
    input_word = input_word.lower()
    if input_word in vocab:
        #  Se a palavra sendo checada está contida no nosso vocabulário, ela
        #  está certa e a busca por palavras similares não deve ser implementada.
        return('Sua palavra está correta!')
    else:
        #  Caso contrário, rode a busca de palavras similares através do cáculo
        #  de frequência.
        semelhancas = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Palavra', 0:'Probabilidade'})
        df['Semelhança'] = semelhancas
        output = df.sort_values(['Semelhança', 'Probabilidade'], ascending=False).head()
        return(output)

main()
