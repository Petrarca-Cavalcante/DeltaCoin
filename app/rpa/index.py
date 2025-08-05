"""Class Rpa Module."""

import requests
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import smtplib
import ssl
from email.message import EmailMessage
from driver import Webdriver
import os
import dotenv
dotenv.load_dotenv()


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
                request = request["conteudo"]
            return request
        except Exception:
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
