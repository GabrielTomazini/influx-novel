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

    # Marcar linhas que fazem parte de um bloco <p>...</p>
    # (ex.: <p class="note">...</p>). Essas linhas não devem receber <br>
    # e o texto imediatamente antes de um <p> também não deve receber <br>.
    p_line = [False] * len(lines)
    inside_p = False
    p_start_re = re.compile(r"<\s*p\b", re.IGNORECASE)
    p_end_re = re.compile(r"<\s*/\s*p\s*>", re.IGNORECASE)
    for idx, l in enumerate(lines):
        if not inside_p and p_start_re.search(l):
            inside_p = True
        if inside_p:
            p_line[idx] = True
        if inside_p and p_end_re.search(l):
            inside_p = False

    # Pré-calcular o próximo índice não-vazio para cada linha (para evitar <br> antes de <p>)
    next_nonempty = [None] * len(lines)
    next_idx = None
    for idx in range(len(lines) - 1, -1, -1):
        next_nonempty[idx] = next_idx
        if lines[idx].strip():
            next_idx = idx

    # Encontrar o índice do último parágrafo de texto padrão (sem tags)
    last_text_index = -1
    for i in range(len(lines) - 1, -1, -1):
        stripped = lines[i].strip()
        if not stripped:
            continue
        if p_line[i]:
            continue
        # Se a linha começa com uma tag (h1, div, p, etc.), não é texto padrão
        if stripped.startswith("<"):
            continue
        last_text_index = i
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

        # Linhas dentro de <p>...</p> devem permanecer intactas (sem <br> adicionados)
        if p_line[i]:
            new_lines.append(line)
            continue

        # Se a linha é uma tag (ex.: <h2>, <img>, etc.), manter como está
        if stripped.startswith("<"):
            new_lines.append(line)
            continue

        # Se a linha está vazia, manter assim
        if not stripped:
            new_lines.append(line)
            continue

        # Remover qualquer <br> no final da linha
        line_cleaned = re.sub(r"(<br\s*/?>\s*)+$", "", line, flags=re.IGNORECASE)

        # Se a linha tem conteúdo, adicionar <br><br> (somente no texto padrão)
        if line_cleaned.strip():
            # Não adicionar <br> se for o último texto padrão
            if i == last_text_index:
                new_lines.append(line_cleaned)
                continue

            # Não adicionar <br> imediatamente antes de um bloco <p>
            nxt = next_nonempty[i]
            if nxt is not None and p_line[nxt]:
                new_lines.append(line_cleaned)
                continue

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
