from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    html = """
    <h1>Bienvenido a Area101 API</h1>
    <p>Enlaces útiles:</p>
    <ul>
        <li><a href="/api/schema/">Esquema OpenAPI (JSON)</a></li>
        <li><a href="/api/docs/">Documentación Swagger UI</a></li>
        <li><a href="/api/redoc/">Documentación ReDoc</a></li>
        <li><a href="/api/sessions/">API Sesiones</a></li>
    </ul>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', include('community_sessions.urls')),
    path('', home),  # <--- ruta para la raíz
]