#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path


def contar_palavras(caminho_arquivo):
    """
    Conta o número de palavras em um arquivo.

    Args:
        caminho_arquivo: Caminho para o arquivo a ser analisado

    Returns:
        Dicionário com estatísticas do arquivo
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        # Conta palavras (separadas por espaços em branco)
        palavras = conteudo.split()
        num_palavras = len(palavras)

        # Conta linhas
        linhas = conteudo.split("\n")
        num_linhas = len(linhas)

        # Conta caracteres
        num_caracteres = len(conteudo)
        num_caracteres_sem_espacos = len(
            conteudo.replace(" ", "").replace("\n", "").replace("\t", "")
        )

        return {
            "palavras": num_palavras,
            "linhas": num_linhas,
            "caracteres": num_caracteres,
            "caracteres_sem_espacos": num_caracteres_sem_espacos,
        }

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python contar_palavras.py <caminho_do_arquivo>")
        print("\nExemplo:")
        print("  python contar_palavras.py chapters/1149.html")
        print("  python contar_palavras.py index.html")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não existe.")
        sys.exit(1)

    print(f"\nAnalisando: {caminho_arquivo}")
    print("-" * 50)

    resultado = contar_palavras(caminho_arquivo)

    if resultado:
        print(f"Palavras:                {resultado['palavras']:,}")
        print(f"Linhas:                  {resultado['linhas']:,}")
        print(f"Caracteres (total):      {resultado['caracteres']:,}")
        print(f"Caracteres (sem espaços): {resultado['caracteres_sem_espacos']:,}")
        print("-" * 50)


if __name__ == "__main__":
    main()
