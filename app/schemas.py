"""Esquemas Pydantic para el Catálogo de Productos."""
from enum import Enum
from pydantic import BaseModel, Field

class Categoria(str, Enum):
    perifericos = "perifericos"
    monitores = "monitores"
    almacenamiento = "almacenamiento"

class ProductoIn(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{3}$", examples=["TEC-001"])
    nombre: str = Field(min_length=3, max_length=80, examples=["Teclado Mecánico"])
    precio: float = Field(gt=0, examples=[450.0])
    existencias: int = Field(ge=0, examples=[10])
    categoria: Categoria

class ProductoOut(ProductoIn):
    id: int
    disponible: bool

class ExistenciasUpdate(BaseModel):
    cantidad: int