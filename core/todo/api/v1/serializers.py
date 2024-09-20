from rest_framework import serializers
from ...models import Task
from accounts.models import User

class TaskSerializer(serializers.ModelSerializer):
    '''A ModelSerializer for tasks'''
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["author"]
        
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url", None)
        
        return rep
    
    def create(self, validated_data):
        validated_data["author"] = User.objects.get(id=self.context.get("request").user.id)
        return super().create(validated_data)