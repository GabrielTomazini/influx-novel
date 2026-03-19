#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir palavras específicas dentro da div "chapter-content" em arquivos HTML.
Uso: python fix_chapters.py arquivo1.html arquivo2.html ...
"""

import sys
import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:  # pragma: no cover
    BeautifulSoup = None

# Dicionário com as substituições a serem feitas
REPLACEMENTS = {
    "Imortais Gu": "Imortais",
    "Imortal Gu": "Imortal",
    "не": "não",
    "и": "e",
    "painstakingmente": "diligentemente",
    "painstakingly": "diligentemente",
    "<A Lenda de Ren Zu>": "&lt;A Lenda de Ren Zu&gt;",
    "<As Lendas de Ren Zu>": "&lt;As Lendas de Ren Zu&gt;",
    "As Lendas de Ren Zu": "&lt;As Lendas de Ren Zu&gt;",
    "<Lendas de Ren Zu>": "&lt;Lendas de Ren Zu&gt;",
    "Rumble—!": "Estrondo—!",
    "Roar—!": "Rugido—!",
    "Rumble!": "Estrondo!",
    "Roar!": "Rugido!",
    "Rumble—!!": "Estrondo—!!",
    "Roar—!!": "Rugido—!!",
    "Roar—!": "Rugido—!",
    "Rumble…": "Estrondo…",
    "Rumble": "Estrondo",
    "Roar": "Rugido",
}


def fix_chapter_content(html_content):
    """
    Processa o conteúdo HTML e substitui palavras na div chapter-content.

    Args:
        html_content (str): Conteúdo HTML do arquivo

    Returns:
        tuple: (html_content_modificado, quantidade_de_alteracoes)
    """
    total_changes = 0

    # Primeiro, fazemos substituições no HTML puro para casos que podem ser interpretados como tags
    # (se chegarem no BeautifulSoup como tags, o texto pode ser perdido e não dá para substituir depois).
    raw_html_patterns = [
        (r"<\s*A\s+Lenda\s+de\s+Ren\s+Zu\s*>", "&lt;A Lenda de Ren Zu&gt;"),
        (r"<\s*As\s+Lendas\s+de\s+Ren\s+Zu\s*>", "&lt;As Lendas de Ren Zu&gt;"),
        (r"<\s*Lendas\s+de\s+Ren\s+Zu\s*>", "&lt;Lendas de Ren Zu&gt;"),
    ]

    modified_content = html_content
    for pattern, replacement in raw_html_patterns:
        modified_content, count = re.subn(pattern, replacement, modified_content)
        if count > 0:
            print(
                f"    ✓ '{pattern}' → '{replacement}' ({count} ocorrências - no HTML bruto)"
            )
            total_changes += count

    if BeautifulSoup is None:
        print(
            "  ⚠️  Dependência ausente: 'beautifulsoup4' (bs4). "
            "Aplicando substituições no HTML inteiro como fallback. "
            "Instale com: pip install beautifulsoup4"
        )

        for old_text, new_text in REPLACEMENTS.items():
            if "<" in old_text and ">" in old_text:
                continue
            count = modified_content.count(old_text)
            if count <= 0:
                continue
            modified_content = modified_content.replace(old_text, new_text)
            print(f"    ✓ '{old_text}' → '{new_text}' ({count} ocorrências - fallback)")
            total_changes += count

        return modified_content, total_changes

    # Agora faz o parsing HTML para substituições dentro da div chapter-content
    soup = BeautifulSoup(modified_content, "html.parser")
    chapter_content = soup.find("div", class_="chapter-content")

    if not chapter_content:
        print("  ⚠️  Div 'chapter-content' não encontrada")
        return modified_content, total_changes

    # Aplica as substituições dentro da div chapter-content.
    # Usamos o REPLACEMENTS como fonte da verdade, exceto as chaves com <...>,
    # que já foram tratadas no HTML bruto acima.
    for old_text, new_text in REPLACEMENTS.items():
        if "<" in old_text and ">" in old_text:
            continue

        chapter_html = str(chapter_content)
        count_before = chapter_html.count(old_text)
        if count_before <= 0:
            continue

        chapter_html = chapter_html.replace(old_text, new_text)

        new_soup = BeautifulSoup(
            str(soup).replace(str(chapter_content), chapter_html),
            "html.parser",
        )
        soup = new_soup
        chapter_content = soup.find("div", class_="chapter-content")

        print(f"    ✓ '{old_text}' → '{new_text}' ({count_before} ocorrências)")
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
