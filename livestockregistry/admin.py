from django.contrib import admin
from .models import  Breed, Property, Affiliation, Livestock
from .models import ParentChild, VaccinationLog, WeightRecord, Profile


admin.site.register(Breed)
admin.site.register(Property)
admin.site.register(Affiliation)
admin.site.register(Livestock)
admin.site.register(ParentChild)
admin.site.register(VaccinationLog)
admin.site.register(WeightRecord)
admin.site.register(Profile)


