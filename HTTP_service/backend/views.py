from django.http import FileResponse
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import FileU, User
from .serializers import FileUSerializer, UserSerializer, CSVDataSerializer
from rest_framework.response import Response


class UserServiceApi(ModelViewSet):
    """
    Для работы с данными пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["id", "name"]


class UploadViewFile(ModelViewSet):
    """
    Загрузить файл, просмотреть список файлов
    """

    queryset = FileU.objects.all()
    serializer_class = FileUSerializer
    filterset_fields = ["id", "created_data", "user"]


class DataFile(APIView):
    """
    Для работы с файлами
    """

    def get(self, request):
        serializer = CSVDataSerializer(data=request.data)
        if serializer.is_valid():
            filtered_and_sorted_data = serializer.get_filtered_and_sorted_data()
            return Response(filtered_and_sorted_data.to_dict(orient="records"))
        return Response(serializer.errors, status=400)


class DownloadFile(View):
    """
    Скачать csv файл по id
    """

    def get(self, request, *args, **kwargs):
        obj = FileU.objects.filter(id=kwargs["pk"]).first()
        if obj is None:
            return JsonResponse({"Error": "файла с таким id нет"})
        csv_file = open(str(obj.file), "rb")
        response = FileResponse(csv_file, content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{str(obj.file)}"'
        return response
