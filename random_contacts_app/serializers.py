
from rest_framework import serializers
from .models import Contact, MyUser


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['phone', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(phone=self.validated_data['phone'],name=self.validated_data['name'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
    
class BulkAddContactsSerializer(serializers.ListSerializer):
    def create(self):
        contacts = [Contact(**item) for item in self.validated_data]
        return Contact.objects.bulk_create(contacts)


class ContactsSerializer(serializers.Serializer):
    fromPhone = serializers.CharField(style={"input_type": "fromPhone"}, required=True)
    toPhone = serializers.CharField(style={"input_type": "toPhone"}, required=True)
    dist = serializers.IntegerField(style={"input_type": "dist"}, required=True)

    class Meta:
        model = Contact
        fields = ['fromPhone', 'toPhone', 'dist']
    #     list_serializer_class = BulkAddContactsSerializer

    def create(self):
        contact = Contact(**self.validated_data)
        if not Contact.objects.filter(**self.validated_data).exists():
            contact.save()
        return contact
    
class TopContactsSerializer(serializers.Serializer):
    fromPhone = serializers.CharField(style={"input_type": "fromPhone"}, required=True)

