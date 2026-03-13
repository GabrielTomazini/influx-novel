import re
from pathlib import Path

# Diretório de capítulos
chapters_dir = Path(__file__).parent / "chapters"
index_path = Path(__file__).parent / "index.html"

# Extrair títulos dos capítulos 2276-2285
titles = {}
for chapter_num in range(2276, 2286):
    chapter_file = chapters_dir / f"{chapter_num}.html"
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Procura pelo padrão <h1>Capítulo XXXX - ...</h1>
        match = re.search(r'<h1>([^<]+)</h1>', content)
        if match:
            title = match.group(1)
            titles[chapter_num] = title
            print(f"Capítulo {chapter_num}: {title}")
        else:
            print(f"Capítulo {chapter_num}: Nenhum título encontrado")

# Ler o index.html
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Substituir os títulos no index.html
for chapter_num in range(2276, 2286):
    if chapter_num in titles:
        old_pattern = f'<li><a href="chapters/{chapter_num}.html">Capítulo {chapter_num} -</a></li>'
        new_pattern = f'<li><a href="chapters/{chapter_num}.html">{titles[chapter_num]}</a></li>'
        index_content = index_content.replace(old_pattern, new_pattern)
        print(f"✓ Atualizado capítulo {chapter_num}")

# Salvar o índice atualizado
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("\n✓ Index atualizado com sucesso!")
