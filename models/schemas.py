from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Lo que recibes para iniciar el escaneo
class SolicitudPeso(BaseModel):
    idusuario: int

# Lo que recibes para actualizar los nombres después
class ActualizarNombres(BaseModel):
    idhistorial: int
    proteina_name: str
    fibra_name: str
    carbohidratos_name: str

class CommandResponse(BaseModel):
    status: str
    message: str
    id_escaneo: Optional[int] = None
    
# Modelo para mostrar datos del historial
class HistorialLectura(BaseModel):
    id: int
    usuario_id: int
    fecha_escaneo: datetime
    temperatura: Optional[float] = None
    # Agregamos los campos nutricionales
    proteina: Optional[float] = None
    fibra: Optional[float] = None
    carbohidratos: Optional[float] = None
    # Agregamos los nombres por si ya existen
    proteina_name: Optional[str] = None
    fibra_name: Optional[str] = None
    carbohidratos_name: Optional[str] = None

class ScanCreateRequest(BaseModel):
    usuario_id: int
    temperatura: float