#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar duas tags <br><br> no final de cada parágrafo dentro de <div class="chapter-content">.
O título h1 não recebe <br> logo após.
Uso: python add_br_paragraphs.py arquivo1.html arquivo2.html ...
"""

import sys
import re
from pathlib import Path


def add_br_to_paragraphs(html_content: str) -> tuple[str, int]:
    """
    Adiciona as tags <br><br> literal no final de cada parágrafo dentro da div.chapter-content.
    Retorna (html_modificado, total_alteracoes)
    """
    # Encontrar a div chapter-content
    chapter_start = html_content.find('<div class="chapter-content">')
    if chapter_start == -1:
        return html_content, 0

    chapter_end = html_content.find("</div>", chapter_start)
    if chapter_end == -1:
        return html_content, 0

    # Extrair o conteúdo interno da div
    before_chapter = html_content[
        : chapter_start + len('<div class="chapter-content">')
    ]
    after_chapter = html_content[chapter_end:]
    inner_content = html_content[
        chapter_start + len('<div class="chapter-content">') : chapter_end
    ]

    # Processar o conteúdo interno
    changes = 0

    # Remover <br> logo após </h1>
    inner_content = re.sub(
        r"(</h1>)\s*<br\s*/?>\s*", r"\1\n", inner_content, flags=re.IGNORECASE
    )

    # Processar linha por linha
    lines = inner_content.split("\n")

    # Encontrar o índice do último parágrafo com conteúdo
    last_content_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            last_content_index = i
            break

    new_lines = []

    skip_br = False  # Flag para não adicionar <br> logo após h1

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Se a linha anterior era </h1>, não adicionar <br>
        if skip_br and not stripped:
            skip_br = False
            new_lines.append(line)
            continue

        if "</h1>" in line:
            skip_br = True
            new_lines.append(line)
            continue

        # Se a linha está vazia, manter assim
        if not stripped:
            new_lines.append(line)
            continue

        # Remover qualquer <br> no final da linha
        line_cleaned = re.sub(r"(<br\s*/?>\s*)+$", "", line, flags=re.IGNORECASE)

        # Se a linha tem conteúdo, adicionar <br><br> (exceto no último parágrafo)
        if line_cleaned.strip():
            if i == last_content_index:
                # Último parágrafo - não adiciona <br><br>
                new_lines.append(line_cleaned)
            else:
                # Outros parágrafos - adiciona <br><br>
                new_lines.append(line_cleaned + "<br><br>")
                changes += 1
        else:
            new_lines.append(line)

    new_inner_content = "\n".join(new_lines)

    return before_chapter + new_inner_content + after_chapter, changes


def process_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Erro ao ler {path}: {e}")
        return False

    new_text, changes = add_br_to_paragraphs(text)
    if changes > 0 and new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"✅ {path} — {changes} linhas/parágrafos atualizadas")
        return True
    else:
        print(f"ℹ️ {path} — nenhuma alteração necessária")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python add_br_paragraphs.py arquivo1.html arquivo2.html ...")
        sys.exit(1)

    print("🔍 Iniciando adição de <br><br> em parágrafos...\n")
    any_changed = False
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.exists() and p.suffix.lower() == ".html":
            if process_file(p):
                any_changed = True
        else:
            print(f"⚠️ Ignorando: {arg}")

    print()
    if any_changed:
        print("✅ Concluído! Alguns arquivos foram atualizados.")
    else:
        print("ℹ️ Concluído! Nenhuma mudança necessária.")
