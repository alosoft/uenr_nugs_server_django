from rest_framework import serializers
from nugs.models import Bloc


class BlocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloc
        fields = ('name', 'logos', 'banners', 'description', 'contact',
                  'profile', 'history', 'executives', 'website', 'date', 'gallery_list')
