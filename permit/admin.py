#from import_export.admin import ImportExportModelAdmin
#from import_export.widgets import ForeignKeyWidget
#from import_export import fields, resources
#from import_export import resources

from permit.models import SubCounty, Ward, Zone, Category, Business, Payment
from django.contrib import admin


admin.site.register(Payment)
admin.site.register(SubCounty)
admin.site.register(Ward)
admin.site.register(Zone)
admin.site.register(Category)
admin.site.register(Business)


