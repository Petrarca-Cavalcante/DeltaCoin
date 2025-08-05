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
