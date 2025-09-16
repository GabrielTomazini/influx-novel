#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir palavras específicas dentro da div "chapter-content" em arquivos HTML.
Uso: python fix_chapters.py arquivo1.html arquivo2.html ...
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Dicionário com as substituições a serem feitas
REPLACEMENTS = {
    "не": "não",
    "и": "e",
    "painstakingmente": "diligentemente",
    "painstakingly": "diligentemente",
    "<A Lenda de Ren Zu>": "&lt;A Lenda de Ren Zu&gt;",
}


def fix_chapter_content(html_content):
    """
    Processa o conteúdo HTML e substitui palavras na div chapter-content.

    Args:
        html_content (str): Conteúdo HTML do arquivo

    Returns:
        tuple: (html_content_modificado, quantidade_de_alteracoes)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    chapter_content = soup.find("div", class_="chapter-content")

    if not chapter_content:
        print("  ⚠️  Div 'chapter-content' não encontrada")
        return html_content, 0

    total_changes = 0
    original_text = str(chapter_content)

    # Aplica as substituições
    for old_word, new_word in REPLACEMENTS.items():
        # Conta quantas vezes a palavra aparece antes da substituição
        count_before = original_text.count(old_word)
        if count_before > 0:
            # Substitui todas as ocorrências
            chapter_content_str = str(chapter_content)
            chapter_content_str = chapter_content_str.replace(old_word, new_word)

            # Reconstrói o soup com o conteúdo modificado
            new_soup = BeautifulSoup(
                str(soup).replace(str(chapter_content), chapter_content_str),
                "html.parser",
            )
            soup = new_soup
            chapter_content = soup.find("div", class_="chapter-content")

            print(f"    ✓ '{old_word}' → '{new_word}' ({count_before} ocorrências)")
            total_changes += count_before

    return str(soup), total_changes


def process_html_file(file_path):
    """
    Processa um arquivo HTML individual.

    Args:
        file_path (Path): Caminho para o arquivo HTML

    Returns:
        bool: True se houve alterações, False caso contrário
    """
    try:
        # Lê o arquivo
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Processa o conteúdo
        new_content, changes = fix_chapter_content(content)

        if changes > 0:
            # Salva as alterações
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ {changes} alterações salvas")
            return True
        else:
            print("  ℹ️  Nenhuma alteração necessária")
            return False

    except Exception as e:
        print(f"  ❌ Erro ao processar arquivo: {e}")
        return False


def main():
    """Função principal do script."""
    if len(sys.argv) < 2:
        print("❌ Uso: python fix_chapters.py arquivo1.html arquivo2.html ...")
        print("\nExemplo:")
        print("  python fix_chapters.py chapters/1421.html")
        print("  python fix_chapters.py chapters/*.html")
        sys.exit(1)

    print("🔍 Iniciando correção de capítulos...")
    print(f"📝 Substituições configuradas: {len(REPLACEMENTS)}")
    for old, new in REPLACEMENTS.items():
        print(f"   • '{old}' → '{new}'")
    print()

    files_processed = 0
    files_changed = 0

    # Processa cada arquivo fornecido
    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)

        if not file_path.exists():
            print(f"⚠️  Arquivo não encontrado: {file_path}")
            continue

        if not file_path.suffix.lower() == ".html":
            print(f"⚠️  Ignorando arquivo não-HTML: {file_path}")
            continue

        print(f"📄 Processando: {file_path}")

        if process_html_file(file_path):
            files_changed += 1

        files_processed += 1
        print()

    # Relatório final
    print("📊 Relatório Final:")
    print(f"   • Arquivos processados: {files_processed}")
    print(f"   • Arquivos modificados: {files_changed}")
    print(f"   • Arquivos inalterados: {files_processed - files_changed}")

    if files_changed > 0:
        print("✅ Correção concluída com sucesso!")
    else:
        print("ℹ️  Nenhum arquivo precisou ser alterado.")


if __name__ == "__main__":
    main()
