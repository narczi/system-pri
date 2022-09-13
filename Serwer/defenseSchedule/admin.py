from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser, CommissionParticipation, Commission, Defense, AvailableTimeSlot, Team, Project, ProjectGradeCard, EvaluationCriteria, ProjectCardEvaluation, CoordinatorTimeSlot

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'group_name')

    def group_name(self, obj):
            return obj.groups.values_list('name',flat=True).get()

    group_name.short_description = 'Grupa'

    list_filter = ('is_admin',)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'team_membership')}),
        ('Permissions', {'fields': ('is_admin','groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_admin','groups')})
    )
    search_fields = ('email',)
    ordering = ('email',)
    #filter_horizontal = ()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['grade_card']

class ProjectAdmin(admin.ModelAdmin):
    exclude = ['grade_card']
    form = ProjectForm


class ProjectCardEvaluationInline(admin.TabularInline):
    model = ProjectCardEvaluation

class ProjectGradeCardAdmin(admin.ModelAdmin):
    inlines = [
        ProjectCardEvaluationInline,
    ]


class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


class TeamInline(admin.TabularInline):
    model = MyUser
    fields = ('email',)
    readonly_fields = ('email',)

class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamInline,
    ]

class CoordinatorTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('pk', 'time_start', 'time_end')

class AvailableTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'person')

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_complete', 'is_accepted', 'is_selected')

class CommissionParticipationAdmin(admin.ModelAdmin):
    #list_display = ('')
    pass

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
admin.site.register(CommissionParticipation, CommissionParticipationAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Defense)
admin.site.register(CoordinatorTimeSlot, CoordinatorTimeSlotAdmin)
admin.site.register(AvailableTimeSlot, AvailableTimeSlotAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectGradeCard, ProjectGradeCardAdmin)
admin.site.register(EvaluationCriteria, EvaluationCriteriaAdmin)
#admin.site.register(ProjectCardEvaluation)