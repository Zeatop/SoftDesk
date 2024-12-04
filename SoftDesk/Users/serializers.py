from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from datetime import date
from dateutil.relativedelta import relativedelta

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    birthday = serializers.DateField(
        required=True,
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
    )
    can_be_contacted = serializers.BooleanField(required=True)
    data_can_be_shared = serializers.BooleanField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 
                 'last_name', 'birthday', 'can_be_contacted', 'data_can_be_shared')
        read_only_fields = ('id',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate_birthday(self, value):
        today = date.today()
        age = relativedelta(today, value).years
        
        if age < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour créer un compte."
            )
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})

        # Validation explicite des champs booléens
        if 'can_be_contacted' not in data:
            raise serializers.ValidationError({"can_be_contacted": "Ce champ est obligatoire."})
            
        if 'data_can_be_shared' not in data:
            raise serializers.ValidationError({"data_can_be_shared": "Ce champ est obligatoire."})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Retire password2 avant création
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birthday=validated_data['birthday'],
            can_be_contacted=validated_data['can_be_contacted'],
            data_can_be_shared=validated_data['data_can_be_shared']
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            validated_data.pop('password2', None)
            instance.set_password(password)
        
        # Validation de l'âge lors de la mise à jour
        if 'birthday' in validated_data:
            today = date.today()
            age = relativedelta(today, validated_data['birthday']).years
            if age < 15:
                raise serializers.ValidationError({"birthday": "Vous devez avoir au moins 15 ans."})
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance