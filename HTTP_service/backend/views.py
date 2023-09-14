from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import FileU, User
from .serializers import FileUSerializer, UserSerializer, CSVDataSerializer
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import os
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(summary="Регистрация пользователя", tags=["Register/Login"])
class RegisterAccount(APIView):
    """
    Для регистрации пользователей
    """

    def post(self, request, *args, **kwargs):
        if {"password", "username"}.issubset(request.data):
            errors = {}
            try:
                validate_password(request.data["password"])
            except Exception as password_error:
                error_array = []

                for item in password_error:
                    error_array.append(item)
                return JsonResponse({"error": {"password": error_array}})
            else:
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data["password"])
                    user.save()
                    return JsonResponse({"Status": True})
                else:
                    return JsonResponse({"error": user_serializer.errors})
        return JsonResponse({"error": "Не указаны все необходимые аргументы"})


@extend_schema(summary="Вход, получение токена", tags=["Register/Login"])
class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """

    def post(self, request, *args, **kwargs):
        if {"username", "password"}.issubset(request.data):
            user = authenticate(
                request,
                username=request.data["username"],
                password=request.data["password"],
            )

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse(
                    {"Status": True, "Token": token.key, "user_id": user.id}
                )

            return JsonResponse({"Status": False, "Errors": "Не удалось авторизовать"})

        return JsonResponse(
            {"Status": False, "Errors": "Не указаны все необходимые аргументы"}
        )


@extend_schema(tags=["User"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список пользователей",
    ),
    update=extend_schema(
        summary="Обновить имя пользователя",
    ),
    destroy=extend_schema(
        summary="Удалять нельзя",
    ),
    create=extend_schema(
        summary="¯\_(ツ)_/¯",
    ),
    retrieve=extend_schema(
        summary="Получить пользователя по id",
    ),
    partial_update=extend_schema(
        summary="Обновить имя пользователя",
    ),
)
class UserServiceApi(ModelViewSet):
    """
    Для работы с данными пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["id", "username"]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if str(request.user.id) != kwargs["pk"]:
                return JsonResponse({"Errors": "Нельзя менять чужие данные"})
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return JsonResponse({"Errors": "Удалять нельзя"})

    def create(self, request, *args, **kwargs):
        return JsonResponse({"Errors": "404"})


@extend_schema(tags=["File"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех файлов",
    ),
    update=extend_schema(
        summary="¯\_(ツ)_/¯",
    ),
    destroy=extend_schema(
        summary="Удалить файл",
    ),
    create=extend_schema(
        summary="Создать новый файл",
    ),
    retrieve=extend_schema(
        summary="Получить файл по id",
    ),
    partial_update=extend_schema(
        summary="¯\_(ツ)_/¯",
    ),
)
class UploadViewFile(ModelViewSet):
    """
    Загрузить файл, просмотреть список файлов
    """

    queryset = FileU.objects.all()
    serializer_class = FileUSerializer
    filterset_fields = ["id", "user"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            request.data._mutable = True
            request.data["user"] = request.user.id
            request.data._mutable = False
            return super().create(request, args, kwargs)
        return JsonResponse({"Errors": "Не удалось авторизовать"})

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            obj = FileU.objects.filter(id=kwargs["pk"]).first()
            if str(request.user.id) != str(obj.user.id):
                return JsonResponse({"Errors": "Нельзя менять чужие данные"})
            instance = self.get_object()
            os.remove(str(instance.file))
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({"Errors": "Не удалось авторизовать"})

    def update(self, request, *args, **kwargs):
        pass


@extend_schema(summary="Работа с данными файла", tags=["File_data"])
class DataFile(APIView):
    """
    Для работы с данными файлами
    """

    def get(self, request):
        if self.request.user.is_authenticated:
            serializer = CSVDataSerializer(data=request.data)
            if serializer.is_valid():
                filtered_and_sorted_data = serializer.get_filtered_and_sorted_data()
                return Response(filtered_and_sorted_data.to_dict(orient="records"))
            return Response(serializer.errors, status=400)
        return JsonResponse({"Errors": "Не удалось авторизовать"})
