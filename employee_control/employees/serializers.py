from rest_framework import serializers
from .models import Employee, Task, Station


class TaskSerializer(serializers.ModelSerializer):
    # Можно добавить название станции для удобства
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'station',
            'description',
            'status',
            'responsible_organization',
            'responsible_user',
            'due_date',
            'station_name',
        ]
        extra_kwargs = {
            'status': {'required': False, 'allow_null': True},  # разрешаем null на входе
        }

    def validate_status(self, value):
        if value is None:
            # Если пришёл null, используем значение по умолчанию из модели
            return Task._meta.get_field('status').default
        return value

class EmployeeSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='user.tasks')

    class Meta:
        model = Employee
        fields = ['id', 'user', 'position', 'phone', 'tasks']


class StationSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Station
        fields = ["name", "road", "description", "latitude", "longitude", "tasks"]