"""Class Rpa Module."""
import requests

class DeltaCoin:
    """DeltCoin class."""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
    
    @property
    def api(self):
        url = "https://bcb.gov.br/api/servico/sitebcb/indicadorCambio"
        try:
            request = requests.get(url)
        except Exception:
            raise Exception("Error at requesting API-s")

    
    