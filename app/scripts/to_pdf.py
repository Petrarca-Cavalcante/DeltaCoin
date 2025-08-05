import pandas as pd
from fpdf import FPDF

# Cria um DataFrame de exemplo
df = pd.DataFrame({
    "Nome": ["Ana", "Bruno", "Carlos"],
    "Idade": [25, 30, 22],
    "Cidade": ["SP", "RJ", "BH"]
})

# Inicializa o PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Adiciona cabeçalho
for col in df.columns:
    pdf.cell(40, 10, col, border=1)
pdf.ln()

# Adiciona os dados
for index, row in df.iterrows():
    for item in row:
        pdf.cell(40, 10, str(item), border=1)
    pdf.ln()

# Salva o PDF
pdf.output("docs_generated/dataframe_saida.pdf")
