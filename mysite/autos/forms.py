from django.forms import ModelForm
from autos.models import Make, Auto

class MakeForm(ModelForm):
    class Meta:
        model = Make
        fields = '__all__'


class AutoForm(ModelForm):
    class Meta:
        model = Auto
        fields = '__all__'
