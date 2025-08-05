"""Class Rpa Module."""

import requests
import pandas as pd
from fpdf import FPDF
import smtplib
import ssl
from email.message import EmailMessage


class DeltaCoin:
    """DeltCoin class."""

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @property
    def api(self):
        url = "https://bcb.gov.br/api/servico/sitebcb/indicadorCambio"
        try:
            request = requests.get(url)
            if request.ok:
                request = request.json()
            return request
        except Exception:
            raise Exception("Error at requesting API-s")

    def to_pdf(self, data):
        df = pd.DataFrame(data)
        df = df["conteudo"].apply(pd.Series)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        col_width = pdf.w / (len(df.columns))  # largura proporcional

        # Cabeçalhos
        for col in df.columns:
            pdf.cell(col_width, 10, col, border=1)
        pdf.ln()

        # Dados
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), border=1)
            pdf.ln()

        # Salvar
        pdf.output(self.pdf_path)

    def mail(self, destinatario, assunto, corpo):
        # Dados do remetente
        remetente = "pedropetrarcar@gmail.com"
        senha = "xktf njan qxeq wodn"  # veja abaixo como obter

        # Cria a mensagem
        mensagem = EmailMessage()
        mensagem["From"] = remetente
        mensagem["To"] = destinatario
        mensagem["Subject"] = assunto
        mensagem.set_content(corpo)

        # Lê e anexa o PDF
        with open(self.pdf_path, "rb") as f:
            conteudo = f.read()
            nome_arquivo = f.name.split("/")[-1]
            mensagem.add_attachment(
                conteudo, maintype="application", subtype="pdf", filename=nome_arquivo
            )

        # Envia via SMTP Gmail
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
            servidor.login(remetente, senha)
            servidor.send_message(mensagem)

        print("E-mail enviado com sucesso!")


dc = DeltaCoin("docs_generated/dataframe_saida.pdf")
from_api = dc.api
dc.to_pdf(from_api)


# Exemplo de uso
dc.mail(
    destinatario="pedropetrarcar@gmail.com",
    assunto="Relatório em PDF",
    corpo="Segue em anexo o relatório.",
)
