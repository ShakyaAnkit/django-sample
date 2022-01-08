
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import Designation
from .serializers import DesignationSerializer


class DesignationListAPIView(ListAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
