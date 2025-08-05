import os
import dotenv

from app.log import Log
from app.rpa import DeltaCoin


dotenv.load_dotenv()

class App:
    
    def __init__(self) -> None:
        self.log = Log("App", print_else=True)

    def from_api(self):
        self.log.init_log("Booting automation as API consumer")
        self.log.write("Running app by api method", f_log=True, level="App.from_api")
        
        app = DeltaCoin(os.getenv("API_PDF_PATH"))
        request = app.api
        self.log.write("Request done", level="App.from_api")
                
        self.log.write("Writing into pdf.", level="App.from_api")
        app.to_pdf(request) 
        self.log.write("Done writing into pdf.", level="App.from_api")
        
                
        self.log.write("Prepairing to send att by E-mail!", level="App.from_api")
        
        app.mail(subject="Atualização no preço do Dollar / Euro",
                 body="Segue último valor capturado pela automação",
                 destiny=os.getenv("EMAILS"))
        
        self.log.write("App - from_api method over!", level="App.from_api")
        


    def from_rpa(self):
        self.log.init_log("Booting automation as RPA")
        self.log.write("Running app by rpa method", f_log=True, level="App.from_rpa")
        
        app = DeltaCoin(os.getenv("RPA_PDF_PATH"))
        request = app.rpa
        self.log.write("RPA done", level="App.from_rpa")
        
        self.log.write("Writing into pdf.", level="App.from_rpa")
        app.to_pdf(request) 
        self.log.write("Done writing into pdf.", level="App.from_rpa")
        
        
        self.log.write("Prepairing to send att by E-mail!", level="App.from_api")
        
        app.mail(subject="Atualização no preço do Dollar / Euro",
                 body="Segue último valor capturado pela automação",
                 destiny=os.getenv("EMAILS"))
        
        self.log.write("App - from_rpa method over!", level="App.from_api")