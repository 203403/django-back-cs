from rest_framework import routers, serializers, viewsets

# Importacion de modelos
from primerComponente.models import PrimerTabla

class PrimerTablaSerializer(serializers.ModelSerializer):
    class meta:
        model = PrimerTabla
        fields = ("nombre", "edad")