from fastapi import APIRouter,HTTPException
from services.db_services import db_client
from models.schemas import HistorialLectura, ScanCreateRequest
from typing import List

router = APIRouter(prefix="/historial", tags=["Base de Datos Supabase"])

@router.get("/", response_model=List[HistorialLectura])
def obtener_historial():
    """
    Obtiene todos los registros de la tabla historial_escaneos.
    """
    data = db_client.get_historial()
    return data

@router.get("/{id_escaneo}", response_model=HistorialLectura)
def obtener_escaneo_por_id(id_escaneo: int):
    """
    Busca una fila específica por su ID.
    """
    dato = db_client.get_scan_by_id(id_escaneo)
    
    if not dato:
        raise HTTPException(status_code=404, detail="Escaneo no encontrado")
        
    return dato

@router.post("/", summary="Guardar escaneo manual")
def guardar_escaneo(scan: ScanCreateRequest):
    """
    Simula guardar un dato manualmente en la BD.
    """
    result = db_client.create_scan(scan.usuario_id, 0, scan.temperatura)
    return {"status": "success", "data": result}