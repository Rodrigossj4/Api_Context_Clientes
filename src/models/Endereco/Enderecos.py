from pydantic import BaseModel
from src.models.Endereco.Endereco import Endereco


class Enderecos(BaseModel):
    Enderecos: list[Endereco]
