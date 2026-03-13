import os
from pathlib import Path

# Diretório de capítulos
chapters_dir = Path(__file__).parent / "chapters"

# Templates para os novos capítulos vazios
def create_empty_chapter(chapter_num):
    prev_chapter = chapter_num - 1
    next_chapter = chapter_num + 1
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
    <title>Capítulo {chapter_num} -</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()">🌙 Modo Escuro</button>

<div class="navigation">
    <a href="{prev_chapter}.html" class="prev-chapter">Capítulo Anterior</a>
    <a href="../index.html" class="menu-link">📚 Voltar ao Menu</a>
    <a href="{next_chapter}.html" class="next-chapter">Próximo Capítulo</a>
</div>

<div class="chapter-content">
<h1>Capítulo {chapter_num} -</h1>
<p class="note">Atenção! Esse capítulo ainda não foi revisado e pode conter alguns erros.</p>

</div>

<div class="navigation">
    <a href="{prev_chapter}.html" class="prev-chapter">Capítulo Anterior</a>
    <a href="../index.html" class="menu-link">📚 Voltar ao Menu</a>
    <a href="{next_chapter}.html" class="next-chapter">Próximo Capítulo</a>
</div>

<script src="../navigation.js"></script>
</body>
</html>"""
    
    return html_content

# Criar capítulos de 2276 a 2285
for chapter_num in range(2276, 2286):
    new_content = create_empty_chapter(chapter_num)
    
    # Salvar novo capítulo
    chapter_path = chapters_dir / f"{chapter_num}.html"
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Capítulo {chapter_num} atualizado com links corretos")

print("\n✓ Todos os capítulos foram atualizados com sucesso!")
print("   Links adicionados: Anterior, Menu, Próximo")
