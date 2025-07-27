from typing import override
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_user = models.ImageField(upload_to='user_images/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)


    def __str__(self):
        return self.user.username

# Opciones comunes
SEX_CHOICES = [
    ('Macho', 'Macho'),
    ('Hembra', 'Hembra'),
]

BREEDING_TYPE = [
    ('Natural', 'Natural'),
    ('Artificial', 'Artificial'),
]

GROWTH_PHASE = [
    ('ternero', 'Ternero'),
    ('joven', 'Joven'),
    ('adulto', 'Adulto'),
]

# Base abstracta para trazabilidad
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_set", on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="updated_%(class)s_set", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

class Breed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    @override
    def __str__(self):
        return f"{self.name}"


class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="property_images/", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"


class Affiliation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)


class Livestock(TimeStampedModel):
    code = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='livestock_images/', null=True, blank=True)
    birth_date = models.DateField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    growth_phase = models.CharField(max_length=20, choices=GROWTH_PHASE)
    sex = models.CharField(max_length=8, choices=SEX_CHOICES)
    breeding_type = models.CharField(max_length=20, choices=BREEDING_TYPE)
    is_active = models.BooleanField(default=True)
    deactivation_note = models.TextField(blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} ({self.breed.name}) - {self.sex}"


class ParentChild(models.Model):
    child = models.ForeignKey(Livestock, related_name='child_relations', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        Livestock,
        related_name='parent_relations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    relation_type = models.CharField(max_length=6, choices=[('mother', 'Mother'), ('father', 'Father')])
    is_by_insemination = models.BooleanField(default=False, help_text="Marcar si fue producto de inseminación")
    insemination_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'relation_type'], name='unique_parent_per_type')
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.child == self.parent:
            raise ValidationError("Un animal no puede ser su propio padre o madre.")

        if self.is_by_insemination:
            if self.parent is not None:
                raise ValidationError("No se puede asignar un padre si se trata de inseminación.")
            if not self.insemination_type:
                raise ValidationError("Debe especificar el tipo de inseminación.")
        else:
            if self.parent is None:
                raise ValidationError("Debe asignar un padre o madre si no es inseminación.")

    def __str__(self):
        if self.is_by_insemination:
            return f"{self.child.code} ({self.relation_type}) - Inseminación: {self.insemination_type}"
        return f"{self.parent.code} ({self.relation_type}) → {self.child.code}"




class VaccinationLog(TimeStampedModel):
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE)
    date = models.DateField()
    vaccine_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.livestock.code} - {self.vaccine_type} ({self.date})"


class WeightRecord(TimeStampedModel):
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    recorded_at = models.DateField()

    def __str__(self):
        return f"{self.livestock.code} - {self.weight} kg on {self.recorded_at}"





