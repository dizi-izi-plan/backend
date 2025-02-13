import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


def get_name(user: User) -> str:
    """Возвращает имя проекта.

    Новосозданный проект имеет имя вида Проект1, Проект2 и т.д.

    Args:
        user (User): Пользователь.

    Returns:
        str: Имя проекта.
    """
    name = f"Проект{user.rooms.count()}"
    all_names = user.rooms.values_list("name", flat=True)
    if name in all_names:
        new_number = max(
            all_names,
            key=lambda value: int(value[len(settings.PROJECT_NAME_BY_DEFAULT):]),
        )
        return f"Проект{int(new_number[len(settings.PROJECT_NAME_BY_DEFAULT) :]) + 1}"
    else:
        return name


def send_pdf_file(subj, email: str, file, text: str | None = None) -> Response:
    """Отправляет pdf файл на почту.

    Args:
        subj: Тема письма.
        email: Почта получателя.
        file: Файл.
        text: Текст письма. Defaults to None.
    """
    sender = "dizi.izi.plan@gmail.com"  # Позднее убрать в .env
    password = "tkttxsrnycqeijpw"  # Позднее убрать в .env
    context = ssl.create_default_context()

    # Позднее убрать в .env
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = email
            msg["Subject"] = subj
            if text:
                msg.attach(MIMEText(text))
            file_type, subtype = file.content_type.split("/")
            filename = file.name
            file = MIMEApplication(file.read(), subtype)
            file.add_header(
                "content-disposition",
                "attachment",
                filename=filename,
            )
            msg.attach(file)
            server.sendmail(sender, email, msg.as_string())
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
