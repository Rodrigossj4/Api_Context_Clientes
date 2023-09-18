from pydantic import BaseModel
from typing import Optional


class Endereco(BaseModel):
    id: Optional[int]
    idCliente: int
    logradouro: str
    bairro: str
    cep: str
    numero: str
    complemento: str
    cidade: str
    estado: str
