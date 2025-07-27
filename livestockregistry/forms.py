

from django import forms
from .models import Livestock
from .models import Breed
from .models import ParentChild

class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = '__all__'
        labels = {
            'code': 'Código',
            'image': 'Imagen',
            'birth_date': 'Fecha de nacimiento',
            'breed': 'Raza',
            'growth_phase': 'Fase de crecimiento',
            'sex': 'Sexo',
            'breeding_type': 'Tipo de reproducción',
            'is_active': '¿Activo?',
            'deactivation_note': 'Motivo de desactivación',
            'property': 'Propiedad',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = "bg-neutral-200 text-slate-950  border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full"
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "rounded border border-gray-300  bg-white "
                })
            else:
                field.widget.attrs.update({"class": base_class})




class BreedForm(forms.ModelForm):
    class Meta:
        model = Breed
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-neutral-200 text-slate-950  border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-neutral-200 text-slate-950  border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full',
                'rows': 4
            }),
        }


class ParentChildForm(forms.ModelForm):
    class Meta:
        model = ParentChild
        fields = ['child', 'relation_type', 'is_by_insemination', 'parent', 'insemination_type']
        widgets = {
            'child': forms.Select(attrs={
                'class': 'bg-neutral-200 text-slate-950 border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full'
            }),
            'relation_type': forms.Select(attrs={
                'class': 'bg-neutral-200 text-slate-950 border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full'
            }),
            'is_by_insemination': forms.CheckboxInput(attrs={
                'class': 'rounded border border-gray-300 dark:border-white/20 bg-white dark:bg-cyan-900/10 text-slate-950 dark:text-white'
            }),
            'parent': forms.Select(attrs={
                'class': 'bg-neutral-200 text-slate-950 border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full'
            }),
            'insemination_type': forms.TextInput(attrs={
                'class': 'bg-neutral-200 text-slate-950 border border-gray-700/10 focus:outline-none focus:ring-2 focus:ring-cyan-500/10 rounded px-3 py-2 w-full'
            }),
        }
