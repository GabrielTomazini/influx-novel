import os
import re

# Diretório dos capítulos
chapters_dir = "chapters"

# Range de capítulos (de 1908 até 2000)
start_chapter = 1908
end_chapter = 2000

# Texto a ser removido
note_pattern = r'<div class="note">Esse capítulo ainda não foi revisado, pode conter alguns erros</div>\s*\n?'

# Contador de arquivos modificados
modified_count = 0

for chapter_num in range(start_chapter, end_chapter + 1):
    file_path = os.path.join(chapters_dir, f"{chapter_num}.html")
    
    if os.path.exists(file_path):
        # Ler o conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se a nota existe no arquivo
        if '<div class="note">Esse capítulo ainda não foi revisado, pode conter alguns erros</div>' in content:
            # Remover a nota
            new_content = re.sub(note_pattern, '', content)
            
            # Salvar o arquivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            modified_count += 1
            print(f"Removido do capítulo {chapter_num}")
    else:
        print(f"Arquivo {file_path} não encontrado")

print(f"\nTotal de arquivos modificados: {modified_count}")
