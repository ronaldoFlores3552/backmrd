import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class DatabaseService:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        
        # Validación simple para asegurarnos que leyo el .env
        if not url or not key:
            print("Error: No se encontraron SUPABASE_URL o SUPABASE_KEY en el archivo .env")
            # Podrías lanzar un error o manejarlo, aquí solo imprimimos para debug
            
        self.supabase: Client = create_client(url, key)

    def get_historial(self):
        # Obtiene datos de la tabla historial_escaneos
        response = self.supabase.table("historial_escaneos").select("*").order("fecha_escaneo", desc=True).execute()
        return response.data

    # NUEVO: Crear escaneo con peso repetido y retornar el ID
    def create_scan_from_sensor(self, usuario_id: int, peso: float, temperatura: float):
        data = {
            "usuario_id": usuario_id,
            "temperatura": temperatura,
            "total_calorias": 0,
            "proteina": peso,
            "fibra": peso,
            "carbohidratos": peso,
            "proteina_name": "",
            "fibra_name": "",
            "carbohidratos_name": ""
        }
        
        # Insertar y ejecutar
        response = self.supabase.table("historial_escaneos").insert(data).execute()
        
        # IMPORTANTE: Devolver el primer elemento de la lista 'data'
        # Esto contiene: {id: 5, usuario_id: 1, proteina: 20... etc}
        if response.data and len(response.data) > 0:
            return response.data[0]  
            
        return None

    # NUEVO: Actualizar los nombres (PUT)
    def update_scan_names(self, scan_id: int, p_name: str, f_name: str, c_name: str):
        data = {
            "proteina_name": p_name,
            "fibra_name": f_name,
            "carbohidratos_name": c_name
        }
        
        # Actualizamos donde el ID coincida
        response = self.supabase.table("historial_escaneos").update(data).eq("id", scan_id).execute()
        return response.data
    
    def get_scan_by_id(self, scan_id: int):
        # Select * from historial_escaneos where id = scan_id
        response = self.supabase.table("historial_escaneos").select("*").eq("id", scan_id).execute()
        
        # Si encuentra datos, retorna el primero (el único)
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

# Esta es la variable que tu router está intentando importar
db_client = DatabaseService()