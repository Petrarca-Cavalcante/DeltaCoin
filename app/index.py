import os
import dotenv

from app.log import Log
from app.rpa import DeltaCoin


dotenv.load_dotenv()

class App:
    
    def __init__(self) -> None:
        self.log = Log("App", print_else=True)

    
    def from_api(self):
        self.log.write("Running app by api method", f_log=True, level="App.from_api")
        app = DeltaCoin(os.getenv("API_PDF_PATH"))
        request = app.api
        self.log.write("Request done", level="App.from_api")
        
        self.log.write("Writing into pdf.", level="App.from_api")
        app.to_pdf(request) 
        self.log.write("Done writing into pdf.", level="App.from_api")
        
        app.mail(subject="Atualização no preço do Dollar / Euro",
                 body="Segue último valor capturado pela automação",
                 destiny=os.getenv("EMAILS"))
        
