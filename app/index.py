import os
import dotenv

from app.log import Log
from app.rpa import DeltaCoin


dotenv.load_dotenv()

class App:
    
    def __init__(self) -> None:
        self.log = Log("App", print_else=True)
