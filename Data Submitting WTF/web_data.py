from wtforms import Form
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, RadioField, \
    SelectField, SelectMultipleField, DateField

from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput


class StoryForm(Form):
    story_title = StringField(
        label="Название новости:",
        name="story-title",
        validators=[InputRequired(message="Вы не указали заголовок новости.")]
    )

    story_content = TextAreaField(label="О чём новости:", name="story-content")

    story_author = SelectField(label="Автор новости:", name="story-author", coerce=int)

    scope = RadioField(
        label="Степень доступности",
        choices=[
            ("public", "Доступна всем"),
            ("private", "Доступна только для подписчиков (обычных и премиум)"),
            ("super-private", "Доступна только для премиум-подписчиков")
        ],
        default="public"
    )

    creation_date = DateField(label="Дата публикации новости:", name="creation-date", format="%Y-%m-%d")

    story_topics = SelectMultipleField(
        label="Тема",
        name="story-topics",
        coerce=int,
        widget=ListWidget(html_tag="ul", prefix_label=False),
        render_kw={"style": "list-style-type: none; padding: 0; margin-block-start: 0.25em; margin-block-end: 0.25em;"},
        option_widget=CheckboxInput()
    )

    severity = IntegerField(
        label="Уровень важности (от 1 до 5):",
        validators=[
            InputRequired(message="Вы не указали степень важности новости."),
            NumberRange(min=1, max=5, message="Степень важности новости должна быть целым числом от 1 до 5.")
        ],
        default=3
    )

    responsibility = BooleanField(
        label="Я понимаю, что вполне могу получить по шапке, если напишу что-нибудь оскорбительное.",
        validators=[
            InputRequired(message="Вы не указали, готовы ли взять на себя ответственность за публикацию новостей спорного характера.")
        ]
    )


class UserForm(Form):
    first_name = StringField(
        label="Имя:",
        validators=[InputRequired(message="Введите имя пользователя.")]
    )

    last_name = StringField(
        label="Фамилия:",
        validators=[InputRequired(message="Введите фамилию пользователя.")]
    )

    username = StringField(
        label="Логин:",
        validators=[InputRequired(message="Введите логин пользователя.")]
    )

    password = StringField(
        label="Пароль:",
        validators=[InputRequired(message="Введите пароль пользователя.")]
    )

    confirm_password = StringField(
        label="Подтверждение пароля:",
        validators=[InputRequired(message="Подтвердите пароль пользователя.")]
    )
