"""Repositorio en memoria para el Catálogo de Productos."""
from .schemas import Categoria, ProductoIn, ProductoOut

class ProductoRepository:
    def __init__(self) -> None:
        self._items: dict[int, ProductoOut] = {}
        self._next_id = 1

    def add(self, data: ProductoIn) -> ProductoOut | None:
        for p in self._items.values():
            if p.sku == data.sku:
                return None
        
        producto = ProductoOut(
            **data.model_dump(),
            id=self._next_id,
            disponible=data.existencias > 0,
        )
        self._items[producto.id] = producto
        self._next_id += 1
        return producto

    def list(self, categoria: Categoria | None = None, solo_disponibles: bool = False) -> list[ProductoOut]:
        productos = list(self._items.values())
        if categoria is not None:
            productos = [p for p in productos if p.categoria == categoria]
        if solo_disponibles:
            productos = [p for p in productos if p.disponible]
        return productos

    def get(self, producto_id: int) -> ProductoOut | None:
        return self._items.get(producto_id)

    def update(self, producto_id: int, data: ProductoIn) -> ProductoOut | None:
        current = self._items.get(producto_id)
        if current is None:
            return None

        updated = ProductoOut(
            **data.model_dump(),
            id=producto_id,
            disponible=data.existencias > 0,
        )
        self._items[producto_id] = updated
        return updated

    def delete(self, producto_id: int) -> bool:
        return self._items.pop(producto_id, None) is not None

    def update_existencias(self, producto_id: int, cantidad: int) -> ProductoOut | None:
        current = self._items.get(producto_id)
        if current is None:
            return None
        
        nuevas_existencias = current.existencias + cantidad
        updated = current.model_copy(
            update={
                "existencias": nuevas_existencias,
                "disponible": nuevas_existencias > 0,
            }
        )
        self._items[producto_id] = updated
        return updated

repo = ProductoRepository()

def get_repo() -> ProductoRepository:
    return repo