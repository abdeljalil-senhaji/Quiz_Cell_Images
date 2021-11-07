from .models import Image
from django_filters import FilterSet, ModelChoiceFilter
import django_tables2 as tables

class ImageFilter(FilterSet):
    image_name = ModelChoiceFilter(queryset=Image.objects.values_list('image_name', flat=True).distinct())
    microscopy = ModelChoiceFilter(queryset=Image.objects.values_list('microscopy', flat=True).distinct())

    class Meta:
        model = Image
        fields = ['microscopy', 'image_name', 'description',  'cell_type', 'component', 'doi', 'organism']


class ImageTable(tables.Table):
    class Meta:
        model = Image

    Image = tables.TemplateColumn(
        '<a href="/static/images/{{ record.image_name }}.jpg"><img src="/static/images/{{ record.image_name }}.jpg" '
        'width="80" height="80"></a>')
