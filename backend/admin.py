from django.contrib import admin
from .models import Comment, Institutions_Unit, Institution, City, Capacity, Aqi, Favorite
from django.contrib.auth.models import User


# 客製化頁面顯示清單 (list_diaplay)：顯示 com_title 與 com_con 欄位
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['com_title', 'com_con']
    list_display_links = ['com_title']
    list_filter = ['com_title', 'com_con']
    search_fields = ['com_title']



    class Meta:
        model = Comment


admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Institution)
admin.site.register(City)
admin.site.register(Capacity)
admin.site.register(Aqi)
admin.site.register(Favorite)
admin.site.register(Institutions_Unit)
