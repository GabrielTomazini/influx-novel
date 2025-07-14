import re
import sys
import os

# Verificar se o nome do arquivo foi fornecido como parâmetro
if len(sys.argv) != 2:
    print("Uso: python process_html.py <nome_do_arquivo.html>")
    print("Exemplo: python process_html.py index.html")
    sys.exit(1)

# Obter o nome do arquivo do parâmetro
filename = sys.argv[1]

# Verificar se o arquivo existe
if not os.path.exists(filename):
    print(f"Erro: O arquivo '{filename}' não foi encontrado.")
    sys.exit(1)

# Ler o arquivo HTML
with open(filename, "r", encoding="utf-8") as file:
    content = file.read()

# Separar o cabeçalho HTML do conteúdo do body
header_match = re.search(r"(.*?<body>\s*)", content, re.DOTALL)
footer_match = re.search(r"(\s*</body>.*)", content, re.DOTALL)

if header_match and footer_match:
    header = header_match.group(1)
    footer = footer_match.group(1)

    # Extrair apenas o conteúdo entre <body> e </body>
    body_content = content[len(header) : -len(footer)]

    # Função para normalizar tags <br> para exatamente 2
    def normalize_br_tags(text):
        # Primeiro, substituir qualquer sequência de tags <br> por um marcador temporário
        # Isso funciona melhor que tentar contar diretamente
        
        # Padrão para encontrar sequências de tags <br> (com ou sem espaços/quebras de linha)
        br_pattern = r'(<br\s*/?>\s*){1,}'
        
        def replace_br_sequence(match):
            # Sempre substituir qualquer sequência de <br> por exatamente 2
            return '<br><br>'
        
        # Aplicar a substituição
        normalized = re.sub(br_pattern, replace_br_sequence, text, flags=re.IGNORECASE)
        
        # Agora, para linhas que não têm nenhuma tag <br>, adicionar 2
        lines = normalized.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Se a linha não está vazia
                # Verificar se a linha contém alguma tag <br>
                if not re.search(r'<br\s*/?>', line, re.IGNORECASE):
                    # Não tem nenhuma tag <br>, adicionar 2
                    processed_lines.append(line + '<br><br>')
                else:
                    # Já tem tags <br> (que foram normalizadas para 2)
                    processed_lines.append(line)
            else:
                # Linha vazia, adicionar <br><br>
                processed_lines.append('<br><br>')
        
        return '\n'.join(processed_lines)
    
    # Aplicar a normalização
    cleaned_content = normalize_br_tags(body_content)
    
    # Reconstruir o conteúdo
    new_content = header + cleaned_content + footer

    # Salvar o arquivo modificado
    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_content)

    print(f"Arquivo '{filename}' processado com sucesso!")
    print("Processamento concluído:")
    print("- Linhas sem <br>: adicionadas 2 tags <br>")
    print("- Linhas com 1 <br>: adicionada 1 tag <br>")
    print("- Linhas com 2 <br>: mantidas como estão")
    print("- Linhas com mais de 2 <br>: reduzidas para 2 tags <br>")
else:
    print("Erro: Não foi possível encontrar as tags <body> no arquivo.")
