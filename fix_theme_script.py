import os
import re

# Script do tema que precisa ser adicionado
theme_script = """
<script>
function toggleTheme() {
    const body = document.body;
    const button = document.querySelector('.theme-toggle');
    
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        button.textContent = '☀️ Modo Claro';
        localStorage.setItem('theme', 'dark');
    } else {
        button.textContent = '🌙 Modo Escuro';
        localStorage.setItem('theme', 'light');
    }
}

// Carregar tema salvo
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const button = document.querySelector('.theme-toggle');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        button.textContent = '☀️ Modo Claro';
    }
});
</script>
"""

# Diretório dos capítulos
chapters_dir = "chapters"

# Lista de capítulos para corrigir
chapters_to_fix = range(2076, 2091)

for chapter_num in chapters_to_fix:
    filepath = os.path.join(chapters_dir, f"{chapter_num}.html")

    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        continue

    # Ler o conteúdo do arquivo
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar se já tem o script do tema
    if "function toggleTheme()" in content:
        print(f"Capítulo {chapter_num} já tem o script do tema")
        continue

    # Encontrar a posição antes de </body>
    # Remover apenas a linha <script src="../navigation.js"></script>
    # E adicionar o script do tema + navigation.js

    # Padrão para encontrar o script navigation.js e a tag </body>
    pattern = r'(<script src="\.\./navigation\.js"></script>\s*</body>)'

    if re.search(pattern, content):
        # Substituir por: script do tema + navigation.js + </body>
        replacement = (
            theme_script + '\n<script src="../navigation.js"></script>\n</body>'
        )
        new_content = re.sub(pattern, replacement, content)

        # Salvar o arquivo atualizado
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✓ Capítulo {chapter_num} corrigido")
    else:
        print(f"⚠ Padrão não encontrado no capítulo {chapter_num}")

print("\nCorreção concluída!")
