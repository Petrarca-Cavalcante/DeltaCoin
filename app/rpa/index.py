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
from app.rpa.driver import Webdriver

from app.log import Log

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
                self.log.write("Request done!", level="API")
                request = request.json()
                request = request["conteudo"]
            return request
        except Exception:
            self.log.write("Error at requesting API-s", level="API")
            raise Exception("Error at requesting API-s")

    @property
    def rpa(self):
        self.log.write("Booting WebDriver to extract data as RPA", level="RPA", f_log=True)
        #
        cd = Webdriver()
        wd = cd.driver
        wd.get("https://www.bcb.gov.br")
        self.log.write("Accessed - https://www.bcb.gov.br !", level="RPA")
        #
        
        # ENCONTRA TABELAS DE COTAÇÃO
        self.log.write("Looking for price tables", level="RPA")
        tables = cd.find_many("//div[@class='componente cotacao']//table") or []
        if not tables:
            self.log.write("Tables not found or empty", level="RPA")
        #            

        prices = []
        for table in tables:
            # CAPTURA CABEÇALHOS E CONTEÚDOS
            headers = cd.find_in(table, "./thead/tr/th")
            tds = cd.find_in(table, "./tbody/tr/td")
            #
            # CASO NÃO SEJA ENCONTRADO, ELE É "PULADO"
            if not headers or not tds:
                # > Adicionar meio de "recuperação" da tarefa perdida
                self.log.write(f"Headers or Rows from price table are missing! SKIPPING! \n> {headers} | {tds}", level="RPA")
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
        self.log.write("RPA ran trought price table/list", level="RPA")
        #
        cd.kill()
        return prices


    def to_pdf(self, data):
        self.log.write("Starting .pdf generation.", level="to_pdf", f_log=True)
        df = pd.DataFrame(data)

        self.log.write("Defining proportions of pdf grid.", level="to_pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        col_width = pdf.w / (len(df.columns))  # largura proporcional

        self.log.write("Setting headers of pdf.", level="to_pdf")
        # Cabeçalhos
        for col in df.columns:
            pdf.cell(col_width, 10, col, border=1)
        pdf.ln()

        self.log.write("Inserting data into pdf.", level="to_pdf")
        # Dados
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), border=1)
            pdf.ln()

        # Salvar
        self.log.write(f"Writing pdf as > {self.pdf_path}", level="to_pdf")
        pdf.output(self.pdf_path)
    
    
    def mail(self, destiny, subject, body):
        self.log.write("Starting mailing pdf generated.", level="mail", f_log=True)
        
        remetente = os.getenv("EMAIL_SENDER") or ""
        senha = os.getenv("GOOGLE_APP_PASS") or ""

        # Criate message
        self.log.write("Message creation", level="mail")
        
        message = EmailMessage()
        message["From"] = remetente
        message["To"] = destiny
        message["Subject"] = subject
        message.set_content(body)
        #
        # Reads and indexes pdf
        self.log.write("Pdf Indexing", level="mail")
        with open(self.pdf_path, "rb") as f:
            conteudo = f.read()
            nome_arquivo = f.name.split("/")[-1]
            message.add_attachment(
                conteudo, maintype="application", subtype="pdf", filename=nome_arquivo
            )

        self.log.write("Preparing to send email!", level="mail")
        # Send via SMTP Gmail
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
            servidor.login(remetente, senha)
            servidor.send_message(message)

        self.log.write("E-mail sent successfully!", level="mail")
        


