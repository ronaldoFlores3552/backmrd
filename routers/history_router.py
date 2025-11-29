from fastapi import APIRouter,HTTPException
from services.db_services import db_client
from services.gemini_service import gemini_client
from models.schemas import HistorialLectura, ScanCreateRequest, CaloriasRequest
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

@router.post("/calorias")
def calcular_calorias_desde_gemini(datos: CaloriasRequest):
    """
    Solicita a Gemini el total de calorías usando nombres y pesos enviados en el cuerpo.
    No accede a la base de datos.
    """
    try:
        total_calorias = gemini_client.obtener_total_calorias_por_alimentos(
            proteina_name=datos.proteina_name,
            proteina=datos.proteina_peso,
            carbohidratos_name=datos.carbohidratos_name,
            carbohidratos=datos.carbohidratos_peso,
            fibra_name=datos.fibra_name,
            fibra=datos.fibra_peso,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo obtener el total de calorías desde Gemini: {exc}",
        )

    return {"status": "success", "total_calorias": total_calorias}

@router.post("/", summary="Guardar escaneo manual")
def guardar_escaneo(scan: ScanCreateRequest):
    """
    Simula guardar un dato manualmente en la BD.
    """
    result = db_client.create_scan(scan.usuario_id, 0, scan.temperatura)
    return {"status": "success", "data": result}
