from datetime import datetime
from typing import Annotated, Dict, Any, List

from sqlalchemy import String, text, ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

today = Annotated[datetime, mapped_column(server_default=text("CURRENT_DATE"))]

str_11 = Annotated[str, 11]
str_16 = Annotated[str, 16]
str_128 = Annotated[str, 128]
str_150 = Annotated[str, 150]
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]


class Base(DeclarativeBase):
    id: Mapped[int_pk]
    repr_cols_num = 3
    repr_columns = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_columns or idx < self.repr_cols_num:
                cols.append(f"{col} = {getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TypesMixin:
    type_annotation_map = {
        str_11: String(11),
        str_16: String(16),
        str_128: String(128),
        str_150: String(150),
        str_256: String(256),
        str_512: String(512)
    }


class GroupModel(Base, TypesMixin):
    __tablename__ = "social_entities_group"
    external_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str_128]
    link: Mapped[str_256]
    added_at: Mapped[created_at]

    post_metrics: Mapped[List['PostMetricsModel']] = relationship(
        back_populates='group',
        uselist=True
    )

    predictive_models: Mapped['PredictiveModelsModel'] = relationship(
        back_populates='group'
    )

class PredictiveModelsModel(Base, TypesMixin):
    __tablename__ = 'social_entities_predictivemodels'
    params: Mapped[Dict[str, Any]] = mapped_column(type_=JSONB)
    model: Mapped[str_128]
    group_id: Mapped[int] = mapped_column(ForeignKey("social_entities_group.id", ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(back_populates='predictive_models')

class PostMetricsModel(Base, TypesMixin):
    __tablename__ = "stats_postmetrics"

    post_id: Mapped[int]
    likes_count: Mapped[int]
    views_count: Mapped[int]
    reposts_count: Mapped[int]
    comms_count: Mapped[int]
    hour: Mapped[int]
    day_of_week: Mapped[int]
    is_weekend: Mapped[bool]
    has_text: Mapped[bool]
    text_length: Mapped[int]
    like_view_ratio: Mapped[float]
    has_video: Mapped[bool]
    has_photo: Mapped[bool]
    word_count: Mapped[int]

    timestamp: Mapped[datetime]

    group_id: Mapped[int] = mapped_column(ForeignKey("social_entities_group.id", ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(back_populates='post_metrics')
