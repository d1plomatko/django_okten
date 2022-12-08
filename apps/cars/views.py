from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CarModel
from .serializers import CarSerializer
from rest_framework.permissions import AllowAny


class CarsListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        qs = CarModel.objects.all()
        query = self.request.query_params.dict()
        auto_park_id = query.get('auto_park_id')

        if query:
            qs = qs.filter(auto_park=auto_park_id)

        serializer = CarSerializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
