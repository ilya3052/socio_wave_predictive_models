from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class ParentSchemaConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid', populate_by_name=True)


class GroupSchema(ParentSchemaConfig):
    id: int = Field(
        alias="group_id",
        description="Уникальный ID группы в системе"
    )
    external_id: int = Field(
        alias='group_externalID',
        description='ID группы на платформе'
    )
    name: str = Field(
        alias="group_name",
        max_length=128,
        description="Название группы"
    )
    link: str = Field(
        alias="group_link",
        max_length=256,
        description="Полная ссылка на группу"
    )
    added_at: date = Field(
        alias="group_added_at",
        le=date.today(),
        default=date.today()
    )


class PredictiveModelsSchema(ParentSchemaConfig):
    id: int = Field(alias="predictive_models_id", description="Уникальный ID модели в системе")
    model: str = Field(alias="predictive_models_model", max_length=128, description="Название модели")
    params: dict = Field(alias="predictive_models_params", description="Параметры модели в формате JSON")
    group_id: int = Field(description="Внешний ключ для связи с группой")


class PostMetricsSchemaBase(ParentSchemaConfig):
    post_id: int = Field(
        alias="stats_postmetrics_post_id",
        description="ID поста в группе для которого собираются метрики"
    )
    likes_count: int = Field(
        alias="stats_postmetrics_likes_count",
        description="Количество лайков поста"
    )
    views_count: int = Field(
        alias="stats_postmetrics_views_count",
        description="Количество просмотров поста"
    )
    reposts_count: int = Field(
        alias="stats_postmetrics_repost_count",
        description="Количество репостов поста"
    )
    comms_count: int = Field(
        alias="stats_postmetrics_comms_count",
        description="Количество комментариев поста"
    )
    hour: int = Field(
        alias="stats_postmetrics_hour",
        description="Час публикации"
    )
    day_of_week: int = Field(
        alias="stats_postmetrics_day_of_week",
        description="День публикации"
    )
    is_weekend: bool = Field(
        alias="stats_postmetrics_is_weekend",
        description="Признак публикации в выходной день"
    )
    is_night: bool = Field(
        alias="stats_postmetrics_is_night",
        description="Признак публикации ночью"
    )
    is_prime_time: bool = Field(
        alias="stats_postmetrics_is_prime_time",
        description="Признак публикации вечером"
    )
    has_text: bool = Field(
        alias="stats_postmetrics_has_text",
        description="Признак наличия текста в посте"
    )
    text_length: int = Field(
        alias="stats_postmetrics_text_length",
        description="Длина текста поста"
    )
    is_morning: bool = Field(
        alias="stats_postmetrics_is_morning",
        description="Признак публикации утром"
    )
    is_lunch: bool = Field(
        alias="stats_postmetrics_is_lunch",
        description="Признак публикации в обед"
    )
    like_view_ratio: float = Field(
        alias="stats_postmetrics_like_view_ratio",
        description="Соотношение лайков к просмотрам"
    )
    er: float = Field(
        alias="stats_postmetrics_er",
        description="Соотношение всех показателей к просмотрам"
    )
    has_video: bool = Field(
        alias="stats_postmetrics_has_video",
        description="Признак наличия видео в посте"
    )
    has_photo: bool = Field(
        alias="stats_postmetrics_has_photo",
        description="Признак наличия фото в посте"
    )
    word_count: int = Field(
        alias="stats_postmetrics_word_count",
        description="Количество слов в посте"
    )

    group_id: int = Field(description="Внешний ключ для связи с группой")
    timestamp: datetime = Field(alias="stats_postmetrics_timestamp", default=datetime.now())


class PostMetricsSchema(PostMetricsSchemaBase):
    id: int = Field(alias="", description="")


class PostMetricsSchemaCreate(PostMetricsSchemaBase):
    pass
