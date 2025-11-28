from fastapi import APIRouter, HTTPException
import time
from services.mqtt_service import mqtt_client
from services.db_services import db_client
from models.schemas import CommandResponse, SolicitudPeso, ActualizarNombres, HistorialLectura

router = APIRouter(prefix="/device", tags=["Operaciones Dispositivo"])

# 1. POST modificado: Recibe ID usuario, pide peso, guarda en BD
@router.post("/peso", response_model=HistorialLectura)
def solicitar_y_guardar_peso(solicitud: SolicitudPeso):
    
    mqtt_client.send_command("peso")
    time.sleep(2) 
    
    datos_sensor = mqtt_client.get_latest_data()
    peso_detectado = datos_sensor.get("peso", 0.0)
    temp_detectada = datos_sensor.get("temperatura", 0.0)
    
    nuevo_registro = db_client.create_scan_from_sensor(
        usuario_id=solicitud.idusuario,
        peso=peso_detectado,
        temperatura=temp_detectada
    )
    
    if not nuevo_registro:
        raise HTTPException(status_code=500, detail="No se pudo guardar en la base de datos")

    # Al retornar el diccionario completo de Supabase, 
    # FastAPI lo valida contra HistorialLectura y lo envía como JSON completo
    return nuevo_registro


# 2. PUT Nuevo: Para ponerle nombres a los alimentos
@router.put("/peso", response_model=HistorialLectura)
def solicitar_y_guardar_peso(solicitud: SolicitudPeso):
    
    mqtt_client.send_command("peso")
    time.sleep(2) 
    
    datos_sensor = mqtt_client.get_latest_data()
    peso_detectado = datos_sensor.get("peso", 0.0)
    temp_detectada = datos_sensor.get("temperatura", 0.0)
    
    nuevo_registro = db_client.create_scan_from_sensor(
        usuario_id=solicitud.idusuario,
        peso=peso_detectado,
        temperatura=temp_detectada
    )
    
    if not nuevo_registro:
        raise HTTPException(status_code=500, detail="No se pudo guardar en la base de datos")

    return nuevo_registro

@router.post("/motor", response_model=CommandResponse)
def activar_motor():
    mqtt_client.send_command("motor")
    return {"status": "success", "message": "Comando motor enviado"}