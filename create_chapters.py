import os
from pathlib import Path

# Diretório de capítulos
chapters_dir = Path(__file__).parent / "chapters"

# Ler o arquivo 2275.html como template
template_path = chapters_dir / "2275.html"
with open(template_path, "r", encoding="utf-8") as f:
    template_content = f.read()

# Criar capítulos de 2276 a 2285
for chapter_num in range(2276, 2286):
    prev_chapter = chapter_num - 1
    next_chapter = chapter_num + 1

    # Substituir número do capítulo no template
    new_content = template_content.replace("Capítulo 2275", f"Capítulo {chapter_num}")

    # Substituir link anterior
    new_content = new_content.replace(
        f'href="2274.html"', f'href="{prev_chapter}.html"'
    )

    # Se houver link próximo, substituir também
    # Vamos verificar se existe um link próximo
    if f'href="2276.html"' in new_content:
        new_content = new_content.replace(
            f'href="2276.html"', f'href="{next_chapter}.html"'
        )

    # Salvar novo capítulo
    new_chapter_path = chapters_dir / f"{chapter_num}.html"
    with open(new_chapter_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Criado capítulo {chapter_num}")

print("\n✓ Todos os 10 capítulos foram criados com sucesso!")
