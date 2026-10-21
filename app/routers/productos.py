"""Router de Productos: Catálogo y control de existencias."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..repository import ProductoRepository, get_repo
from ..schemas import Categoria, ExistenciasUpdate, ProductoIn, ProductoOut

router = APIRouter(prefix="/productos", tags=["Productos"])
Repo = Annotated[ProductoRepository, Depends(get_repo)]

@router.post("", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoIn, repo: Repo) -> ProductoOut:
    resultado = repo.add(data)
    if resultado is None:
        raise HTTPException(status_code=409, detail="El SKU ya existe")
    return resultado

@router.get("", response_model=list[ProductoOut])
def listar_productos(
    repo: Repo, 
    categoria: Categoria | None = None, 
    solo_disponibles: bool = False
) -> list[ProductoOut]:
    return repo.list(categoria=categoria, solo_disponibles=solo_disponibles)

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, repo: Repo) -> ProductoOut:
    producto = repo.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: int, data: ProductoIn, repo: Repo) -> ProductoOut:
    if repo.get(producto_id) is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for p in repo.list():
        if p.sku == data.sku and p.id != producto_id:
            raise HTTPException(status_code=409, detail="El SKU ya existe en otro producto")

    producto = repo.update(producto_id, data)
    return producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, repo: Repo) -> Response:
    if not repo.delete(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{producto_id}/existencias", response_model=ProductoOut)
def modificar_existencias(producto_id: int, data: ExistenciasUpdate, repo: Repo) -> ProductoOut:
    producto = repo.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if producto.existencias + data.cantidad < 0:
        raise HTTPException(status_code=409, detail="Existencias insuficientes")
    
    return repo.update_existencias(producto_id, data.cantidad)