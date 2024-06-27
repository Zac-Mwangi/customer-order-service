from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.conf import settings
import jwt
from django.core.validators import RegexValidator

from uuid import uuid4


class KenyanPhoneNumberField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r"^\+254\d{9}$",
            message="Phone number must be in the format +254XXXXXXXXX.",
            code="invalid_phone_number",
        )
    ]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 13  # "+254" plus 9 digits
        super().__init__(*args, **kwargs)


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("Username must be set")
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_(
            "Designates whether this user has verified their email on sign up. "
        ),
    )
    code = models.CharField(max_length=50, unique=True)
    phone_number = KenyanPhoneNumberField(max_length=20)
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        self.username = self.username.title()
        self.email = self.email.lower()

        super().save(*args, **kwargs)

    @property
    def token(self):
        token = jwt.encode(
            {
                "username": self.username,
                "email": self.email,
                # "exp": datetime.utcnow() + timedelta(days=30),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token
