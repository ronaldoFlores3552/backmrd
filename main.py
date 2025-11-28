from fastapi import FastAPI
from routers import device_router, history_router 
from services.mqtt_service import mqtt_client
import uvicorn
from dotenv import load_dotenv

# Cargar variables al inicio
load_dotenv()

app = FastAPI(
    title="API IoT & Nutrición",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    mqtt_client.start()

# Incluir routers
app.include_router(device_router.router)
app.include_router(history_router.router) # <--- Lo registramos aquí

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
#python3 main.py 
#http://localhost:8000/docs#/
