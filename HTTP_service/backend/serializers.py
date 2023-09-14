from rest_framework import serializers
from .models import FileU, User
import pandas as pd


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
        read_only_fields = ("id",)


class FileUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileU
        fields = ("id", "created_data", "file", "user", "column_file")
        read_only_fields = (
            "column_file",
            "id",
        )

    def create(self, validated_data):
        """Метод добавления колонок"""
        file = (validated_data["file"].readline()).decode("utf-8")
        data_list = file.split(",")
        data_list[-1] = data_list[-1].rstrip("\r\n")
        validated_data["column_file"] = data_list
        return super().create(validated_data)


class CSVDataSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    column_name = serializers.CharField(required=False)
    desired_value = serializers.CharField(required=False)
    sort_by = serializers.CharField(required=False)

    def get_filtered_and_sorted_data(self):
        """Метод сортировки и фильтрации"""
        obj = FileU.objects.filter(id=self.validated_data.get("id")).first()
        if obj is None:
            raise serializers.ValidationError('Записи с таким id нет')
        data = pd.read_csv(str(obj.file))
        column_name = self.validated_data.get("column_name")
        desired_value = self.validated_data.get("desired_value")
        if column_name and desired_value:
            data = data[data[column_name] == desired_value]
        sort_by = self.validated_data.get("sort_by")
        if sort_by:
            data = data.sort_values(by=sort_by)
        return data

