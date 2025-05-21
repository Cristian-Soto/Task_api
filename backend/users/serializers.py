from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar y actualizar la información del usuario actual.
    
    Este serializador se utiliza para:
    1. Obtener datos del perfil del usuario autenticado
    2. Actualizar datos del perfil como nombre, apellido, etc.
    
    Por razones de seguridad, el ID y correo electrónico son de solo lectura.
    """
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    task_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 
            'last_login', 'date_joined', 'task_count'
        ]
        read_only_fields = ['id', 'email', 'last_login', 'date_joined', 'task_count']
    
    def get_task_count(self, obj):
        """
        Calcula el número de tareas asociadas al usuario.
        
        Args:
            obj (User): Instancia del modelo de usuario
            
        Returns:
            int: Número de tareas del usuario
        """
        return obj.tasks.count()
    
    def update(self, instance, validated_data):
        """
        Actualiza la información del usuario y actualiza el campo last_login.
        
        Args:
            instance (User): Instancia del modelo de usuario a actualizar
            validated_data (dict): Datos validados para la actualización
            
        Returns:
            User: Instancia actualizada del modelo de usuario
        """        # Actualizar el campo last_login
        instance.last_login = timezone.now()
        
        # Actualizar los demás campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro de nuevos usuarios en el sistema.
    
    Este serializador implementa:
    1. Validación de contraseñas (deben coincidir y cumplir requisitos de seguridad)
    2. Validación de datos del usuario (correo único, nombre de usuario único)
    3. Creación segura de usuarios con contraseña encriptada
    
    Los campos de contraseña son de solo escritura para garantizar la seguridad.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        label="Confirmar contraseña"
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password2', 
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
        
    def validate_email(self, value):
        """
        Valida que el correo electrónico no esté ya registrado.
        
        Args:
            value (str): Correo electrónico a validar
            
        Returns:
            str: Correo electrónico validado
            
        Raises:
            serializers.ValidationError: Si el correo ya está registrado
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value
    
    def validate_username(self, value):
        """
        Valida que el nombre de usuario tenga al menos 4 caracteres.
        
        Args:
            value (str): Nombre de usuario a validar
            
        Returns:
            str: Nombre de usuario validado
            
        Raises:
            serializers.ValidationError: Si el nombre de usuario es muy corto
        """
        if len(value) < 4:
            raise serializers.ValidationError(
                "El nombre de usuario debe tener al menos 4 caracteres."
            )
        return value
        
    def validate(self, attrs):
        """
        Valida que las contraseñas coincidan.
        
        Args:
            attrs (dict): Atributos a validar
            
        Returns:
            dict: Atributos validados
            
        Raises:
            serializers.ValidationError: Si las contraseñas no coinciden
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden"}
            )
        return attrs
    
    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.
        
        Args:
            validated_data (dict): Datos validados para crear el usuario
            
        Returns:
            User: Nueva instancia del modelo de usuario
        """
        # Eliminar password2 antes de crear el usuario
        validated_data.pop('password2')
        
        # Crear el usuario con contraseña encriptada
        user = User.objects.create_user(**validated_data)
        
        return user