from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import magic
from django.contrib.auth.models import Group
from indicators.models import Indicator
from django.templatetags.static import static


STATUS = (
    ('', 'Select a status'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected')
)

DISTRICT = (
        ('', 'Select a district'),
        ('Falaba', 'Falaba'),
        ('Karene', 'Karene'),
        ('Kono', 'Kono'),
        ('Moyamba', 'Moyamba'),
        ('Tonkolili', 'Tonkolili'),
        ('Western Rural', 'Western Rural'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

image_ex_validator = FileExtensionValidator(['png', 'jpeg', 'jpg'])
file_ex_validator = FileExtensionValidator(['pdf'])

def validate_image_type(file):
    accept = ['image/png', 'image/jpeg', 'image/jpg']
    file_image_type = magic.from_buffer(file.read(1024), mime=True)
    if file_image_type not in accept:
        raise ValidationError("Unsupported file type")
    
def validate_file_mimetype(file):
    accept = ['application/pdf']
    file_mimetype = magic.from_buffer(file.read(1024), mime=True)
    if file_mimetype not in accept:
        raise ValidationError("Unsupported file type")

# Define a custom file size validation function
def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5MB limit
    if value.size > limit:
        raise models.ValidationError('File size cannot exceed 5MB.')
    
class Ministry(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Ministries"
    
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

class User(AbstractUser):
    is_local_council = models.BooleanField(default=False)
    is_mlgrd = models.BooleanField(default=False)
    is_mda = models.BooleanField(default=False)
    is_district_cso = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
class LocalCouncil(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=user_directory_path, blank=True, null=True, validators=[image_ex_validator, validate_image_type, validate_file_size])
    district = models.CharField(max_length=250, choices=DISTRICT)
    status = models.CharField(choices=STATUS, max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username', 'gender', 'phone_number', 'district', 'position']
    
    class Meta:
        verbose_name_plural = "Local Council"
        
    def local_council_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profile_pic.url))
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('src/images/avatar.svg')
        return avatar
    
    #Concatenate first and last name
    def name(obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    
class DistrictCSO(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[image_ex_validator, validate_image_type, validate_file_size])
    district = models.CharField(max_length=250, choices=DISTRICT)
    status = models.CharField(choices=STATUS, max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username', 'position', 'gender', 'phone_number', 'district']
    
    class Meta:
        verbose_name_plural = "District CSO"
        
    def district_cso_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profile_pic.url))
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('src/images/avatar.svg')
        return avatar
    
    #Concatenate first and last name
    def name(obj):
        return "%s %s" % (obj.first_name, obj.last_name)


class MDA(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, help_text="The name of the specific Ministry to which the user belongs.")
    profile_pic = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[image_ex_validator, validate_image_type, validate_file_size])
    district = models.CharField(max_length=250, choices=DISTRICT)
    status = models.CharField(choices=STATUS, max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username', 'position', 'ministry', 'gender', 'phone_number', 'district']
    
    class Meta:
        verbose_name_plural = "MDA"
        
    def mda_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profile_pic.url))
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('src/images/avatar.svg')
        return avatar
    
    #Concatenate first and last name
    def name(obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    
    
class MLGRD(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, help_text="The name of the specific Ministry to which the user belongs.")
    profile_pic = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[image_ex_validator, validate_image_type, validate_file_size])
    district = models.CharField(max_length=250, choices=DISTRICT)
    status = models.CharField(choices=STATUS, max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username', 'position', 'ministry', 'gender', 'phone_number', 'district']
    
    class Meta:
        verbose_name_plural = "MLGRD"
        
    def mlgrd_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profile_pic.url))
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('src/images/avatar.svg')
        return avatar
    
    #Concatenate first and last name
    def name(obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    
class Assignment(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    district = models.CharField(max_length=100, choices=DISTRICT)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return self.message




