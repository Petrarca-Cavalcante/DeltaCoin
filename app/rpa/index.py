"""Class Rpa Module."""

import os
import dotenv
import requests
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import smtplib
import ssl
from email.message import EmailMessage
from driver import Webdriver
from app.log.index import Log

dotenv.load_dotenv()




class DeltaCoin:
    """DeltCoin class."""

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.log = Log("DeltaCoin", print_else=True)

    @property
    def api(self):
        url = "https://bcb.gov.br/api/servico/sitebcb/indicadorCambio"
        self.log.write("Requesting prices straight from API", level="API", f_log=True)
        try:
            request = requests.get(url)
            if request.ok:
                self.log.write("Request done!")
                request = request.json()
                request = request["conteudo"]
            return request
        except Exception:
            self.log.write("Error at requesting API-s")
            raise Exception("Error at requesting API-s")

    @property
    def rpa(self):
        cd = Webdriver()
        wd = cd.driver
        wd.get("https://www.bcb.gov.br")

        # ENCONTRA TABELAS DE COTAÇÃO
        tables = cd.find_many("//div[@class='componente cotacao']//table") or []
        prices = []

        for table in tables:
            # CAPTURA CABEÇALHOS E CONTEÚDOS
            headers = cd.find_in(table, "./thead/tr/th")
            tds = cd.find_in(table, "./tbody/tr/td")
            #
            # CASO NÃO SEJA ENCONTRADO, ELE É "PULADO"
            if not headers or not tds:
                # > Adicionar log e meio de "recuperação" da tarefa perdida
                continue
            #
            coin = headers[0].text
            if coin not in prices:
                prices.append({
                    "Moeda": coin,
                    "Compra":tds[4].text,
                    "Venda": tds[5].text,
                    "Atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            #
        cd.kill()
        return prices


    def to_pdf(self, data):
        df = pd.DataFrame(data)

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
        remetente = os.getenv("EMAIL_SENDER") or ""
        senha = os.getenv("GOOGLE_APP_PASS") or ""

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

