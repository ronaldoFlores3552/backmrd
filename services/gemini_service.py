import os
import re
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv

# Asegura que las variables de entorno estén cargadas
load_dotenv()


class GeminiService:
    """
    Pequeño wrapper para solicitar a Gemini el total de calorías.
    """

    def __init__(self, model_name: str = None):
        api_key = os.environ.get("GEMINI_API_KEY")
        self._error: Optional[str] = None

        if not api_key:
            self._error = "Falta la variable de entorno GEMINI_API_KEY."
            self.model = None
            return

        # Configure solo con API key; la versión no se pasa aquí en esta librería
        genai.configure(api_key=api_key)
        self.model = self._init_model(model_name)

    def _init_model(self, model_name: Optional[str]):
        """
        Intenta inicializar el modelo probando múltiples opciones comunes.
        """
        candidatos = []

        # Modelo explícito desde el init tiene prioridad
        if model_name:
            candidatos.append(model_name)

        # Luego lo que llegue por env
        env_model = os.environ.get("GEMINI_MODEL")
        if env_model:
            candidatos.append(env_model)

        # Por requerimiento: solo usar el modelo gemini-2.0-flash (y su variante con prefijo)
        candidatos.extend(
            [
                "gemini-2.0-flash",
                "models/gemini-2.0-flash",
            ]
        )

        last_error: Optional[Exception] = None
        last_candidate: Optional[str] = None

        for candidate in candidatos:
            try:
                return genai.GenerativeModel(candidate)
            except Exception as exc:  # noqa: PERF203
                last_error = exc
                last_candidate = candidate
                continue

        # Si ninguno funcionó, guarda el error para devolverlo luego
        self._error = (
            "No se pudo inicializar Gemini con los modelos probados. "
            f"Último candidato: {last_candidate}, error: {last_error}"
        )
        return None

    def obtener_total_calorias(self, proteina: float, carbohidratos: float, fibra: float) -> float:
        if not self.model:
            raise ValueError(self._error or "No se pudo inicializar el cliente de Gemini.")

        prompt = (
            "Necesito el total de calorías sumando proteínas, carbohidratos y fibra. "
            "Responde únicamente con el número total en formato decimal usando punto como separador. "
            f"Proteína: {proteina}, Carbohidratos: {carbohidratos}, Fibra: {fibra}."
        )

        response = self.model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""

        return self._extract_number_or_raise(text)

    def obtener_total_calorias_por_alimentos(
        self,
        proteina_name: str,
        proteina: float,
        carbohidratos_name: str,
        carbohidratos: float,
        fibra_name: str,
        fibra: float,
    ) -> float:
        """
        Calcula calorías estimadas a partir de nombres y pesos de cada alimento.
        """
        if not self.model:
            raise ValueError(self._error or "No se pudo inicializar el cliente de Gemini.")

        prompt = (
            "Eres un experto en nutrición. Estima el total de calorías para los siguientes alimentos "
            "usando valores promedio por 100 g. Devuelve solo el número total en calorías (kcal) en formato decimal "
            "con punto como separador, sin texto adicional.\n\n"
            f"1) {proteina_name or 'proteína'}: {proteina} g\n"
            f"2) {carbohidratos_name or 'carbohidratos'}: {carbohidratos} g\n"
            f"3) {fibra_name or 'fibra'}: {fibra} g\n"
        )

        response = self.model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""

        return self._extract_number_or_raise(text)

    @staticmethod
    def _extract_number_or_raise(text: str) -> float:
        """
        Intenta extraer el primer número decimal (permite , o .) de la respuesta.
        """
        match = re.search(r"[-+]?[0-9]+(?:[\\.,][0-9]+)?", text)
        if not match:
            raise ValueError(f"No se pudo interpretar la respuesta de Gemini: '{text}'")

        number_str = match.group().replace(",", ".")
        return float(number_str)


gemini_client = GeminiService()
