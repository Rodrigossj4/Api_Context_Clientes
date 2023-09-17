from pydantic import BaseModel
from src.models.Cliente.Cliente import Cliente

class Clientes(BaseModel): 
    Clientes:list[Cliente] 