from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Session

class TestReservas(APITestCase):
    def setUp(self):
        self.sesion = Session.objects.create(
            title="Taller de Django",
            description="Sesión de prueba",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            capacity=2
        )

    def test_reserva_exitosa(self):
        """Flujo feliz: se puede reservar si hay plazas"""
        data = {
            "name": "Pedro",
            "email": "pedro@email.com"
        }
        response = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.status_code, 201)  # Línea anterior mantenida pero reemplazada
        self.assertEqual(response.data["name"], "Pedro")
        self.assertEqual(response.data["email"], "pedro@email.com")

    def test_reserva_duplicada(self):
        """Permiso: no se puede reservar dos veces con el mismo email"""
        data = {
            "name": "Pedro",
            "email": "pedro@email.com"
        }
        self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", data)  # 1ra reserva
        response = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", data)  # 2da reserva
        self.assertEqual(response.status_code, 400)
        # self.assertIn("Ya tienes una reserva", str(response.data))  # Comentado por precisión
        self.assertEqual(response.data.get("error"), "Ya tienes una reserva")

    def test_reserva_overbooking(self):
        """Overbooking: no deja reservar si no hay plazas"""
        # Reservamos 2 plazas que es el límite
        self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {
            "name": "A",
            "email": "a@email.com"
        })
        self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {
            "name": "B",
            "email": "b@email.com"
        })
        # Intentamos una 3ra
        response = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {
            "name": "C",
            "email": "c@email.com"
        })
        self.assertEqual(response.status_code, 400)
        # self.assertIn("No hay plazas", str(response.data))  # Comentado por precisión
        self.assertEqual(response.data.get("detail"), "No hay plazas disponibles")

    # def test_reserva_datos_invalidos(self):
    #     """Datos inválidos: campos vacíos"""
    #     response = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("Faltan datos", str(response.data))
    def test_reserva_datos_invalidos(self):
        """Datos inválidos: campos vacíos"""
        response = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {})
        self.assertEqual(response.status_code, 400)
        # self.assertIn("Faltan datos", str(response.data.get("error", "")))  # Comentado
        self.assertEqual(response.data.get("error"), "Faltan datos")

    def test_cancelar_reserva(self):
        """Flujo feliz: se puede cancelar una reserva"""
        # res = self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {
        #     "name": "Juan",
        #     "email": "juan@email.com"
        # }).data  # Comentado porque no se usa 'res'
        self.client.post(f"/api/sessions/{self.sesion.id}/reserve/", {
            "name": "Juan",
            "email": "juan@email.com"
        })
        response = self.client.post(f"/api/sessions/{self.sesion.id}/cancel/", {
            "email": "juan@email.com"
        })
        self.assertEqual(response.status_code, 200)
        # self.assertIn("reserva cancelada", str(response.data).lower())  # Comentado por precisión
        self.assertEqual(response.data.get("detail"), "Reserva cancelada")

    def test_cancelar_reserva_no_email(self):
        """Fallo: cancelar sin email"""
        response = self.client.post(f"/api/sessions/{self.sesion.id}/cancel/", {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("detail"), "Email requerido")

    def test_cancelar_reserva_inexistente(self):
        """Fallo: cancelar reserva que no existe"""
        response = self.client.post(f"/api/sessions/{self.sesion.id}/cancel/", {
            "email": "nadie@email.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get("detail"), "No se encontró una reserva para ese email")
