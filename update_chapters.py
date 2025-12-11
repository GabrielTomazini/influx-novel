import os
import re

# Diretório dos capítulos
chapters_dir = r"C:\Users\byel3\OneDrive\Área de Trabalho\Influx Novel\chapters"

# Script tag a ser adicionado
script_tag = '<script src="../navigation.js"></script>\n'

# Contador de arquivos modificados
modified_count = 0
skipped_count = 0

print("Iniciando atualização dos capítulos...")

# Percorrer todos os arquivos HTML no diretório
for filename in os.listdir(chapters_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(chapters_dir, filename)

        try:
            # Ler o conteúdo do arquivo
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            # Verificar se o script já existe
            if "navigation.js" in content:
                skipped_count += 1
                continue

            # Adicionar o script antes do fechamento de </body>
            if "</body>" in content:
                # Inserir o script antes de </body>
                content = content.replace("</body>", f"{script_tag}</body>")

                # Escrever o conteúdo modificado
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)

                modified_count += 1
                print(f"✓ Atualizado: {filename}")
            else:
                print(f"⚠ Aviso: {filename} não tem tag </body>")

        except Exception as e:
            print(f"✗ Erro ao processar {filename}: {str(e)}")

print(f"\n{'='*50}")
print(f"Concluído!")
print(f"Arquivos modificados: {modified_count}")
print(f"Arquivos já atualizados: {skipped_count}")
print(f"{'='*50}")
