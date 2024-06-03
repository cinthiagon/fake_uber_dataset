import random
import pandas as pd
from faker import Faker

fake = Faker()

# Parâmetros
total_ocorrencias = 27
percent_homens_45_60 = 0.63
percent_ocorrencias_fim_semana_dia = 0.7  # 70% de chance
dias_favoritos = ["sábado", "domingo"]
dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
meses = ["janeiro", "fevereiro", "março", "abril", "maio"]
tipos_ocorrencia = ["fraude", "estelionato"]
mes_dias = {
    "janeiro": 31,
    "fevereiro": 29,  # 2024 é um ano bissexto
    "março": 31,
    "abril": 30,
    "maio": 31
}

# Funções auxiliares
def gerar_idade(homens_45_60):
    if homens_45_60:
        return random.randint(45, 60)
    else:
        return random.randint(18, 44) if random.random() < 0.5 else random.randint(61, 80)

def gerar_data():
    mes = random.choice(meses)
    dia = random.randint(1, mes_dias[mes])
    return f"{dia:02d}/{meses.index(mes) + 1:02d}/2024", mes

def gerar_horario():
    # Maior concentração durante o dia
    if random.random() < 0.7:  # 70% de chance de ser entre 8h e 20h
        hora = random.randint(8, 20)
    else:  # 30% de chance de ser entre 21h e 7h
        hora = random.randint(0, 7) if random.random() < 0.5 else random.randint(21, 23)
    minuto = random.randint(0, 59)
    return f"{hora:02d}:{minuto:02d}"

def gerar_id():
    return random.randint(1, 9999999999)

# Gerando dados
ocorrencias = []

for _ in range(total_ocorrencias):
    homens_45_60 = random.random() < percent_homens_45_60
    genero = "masculino" if homens_45_60 else random.choice(["masculino", "feminino"])
    idade = gerar_idade(homens_45_60)
    
    # Definir se a ocorrência será no fim de semana durante o dia ou não
    if random.random() < percent_ocorrencias_fim_semana_dia:
        dia_semana = random.choice(dias_favoritos)
        horario = gerar_horario()
    else:
        dia_semana = random.choice(dias_semana)
        horario = gerar_horario()
    
    data, mes = gerar_data()
    tipo_ocorrencia = random.choice(tipos_ocorrencia)
    
    ocorrencia = {
        "ID": gerar_id(),
        "Idade": idade,
        "Gênero": genero,
        "Data da Ocorrência": data,
        "Dia da Semana": dia_semana,
        "Horário": horario,
        "Mês da Ocorrência": mes,
        "Descrição": tipo_ocorrencia
    }
    
    ocorrencias.append(ocorrencia)

# Criando DataFrame
df_ocorrencias = pd.DataFrame(ocorrencias)

# Exibindo as primeiras linhas do DataFrame
print(df_ocorrencias.head())

# Contagem de ocorrências por mês
contagem_meses = df_ocorrencias['Mês da Ocorrência'].value_counts()
print("\nContagem de Ocorrências por Mês:")
print(contagem_meses)

# Salvando em um arquivo CSV
df_ocorrencias.to_csv('ocorrencias_uber.csv', index=False)


# Salvando em um arquivo Excel
df_ocorrencias.to_excel('ocorrencias_uber.xlsx', index=False)
