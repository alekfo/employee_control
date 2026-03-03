from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeSerializer


#ModelViewSet – это готовый класс, предоставляющий полный набор CRUD-операций для модели
#благодаря этому нам достаточно определить всего два атрибута:
# queryset – базовый набор записей,
# serializer_class – сериализатор для преобразования моделей в JSON и обратно.
class EmployeeViewSet(viewsets.ModelViewSet):
    # чтобы только аутентифицированные пользователи могли обращаться к API сотрудников:
    #при наличии этой строки любой запрос к /api/employees/ без токена вернёт ошибку 401 Unauthorized.
    permission_classes = [IsAuthenticated]
    #queryset – задаёт, с какими объектами работает вьюсет. Здесь – все сотрудники.
    queryset = Employee.objects.all()
    #указывает, какой сериализатор использовать:
    serializer_class = EmployeeSerializer

    #метод вызывается каждый раз, когда нужно получить queryset для текущего запроса
    def get_queryset(self):
        #Сначала получаем базовый queryset через super().get_queryset() (это будет Employee.objects.all()).
        queryset = super().get_queryset()
        #Затем проверяем, есть ли в query-параметрах (часть URL после ?) параметр name.
        name = self.request.query_params.get('name')
        if name:
            # фильтруем по имени (без учета регистра)
            queryset = queryset.filter(name__icontains=name)
        return queryset

    # переопределим create, чтобы вернуть именно тот JSON, который ты хочешь
    def create(self, request, *args, **kwargs):
        #создаём экземпляр сериализатора (используя объявленный вначале serializer_class), передавая ему данные из тела запроса (request.data).
        # DRF автоматически разбирает JSON в словарь.
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #self.perform_create(serializer) – сохраняет объект в базу. Внутри вызывает serializer.save().
            self.perform_create(serializer)
            # Возвращаем success=true + данные созданного объекта
            return Response({
                'success': True,
                **serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)