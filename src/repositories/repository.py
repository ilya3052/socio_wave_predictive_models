from datetime import timedelta, datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import GroupModel, PostMetricsModel, PredictiveModelsModel
from .base import BaseRepository


class GroupsRepository(BaseRepository[GroupModel]):
    def __init__(self, session):
        super().__init__(session, GroupModel)

    def get_groups_with_metrics(self):
        group_ids = self.session.scalars(
            select(PostMetricsModel.group_id)
            .filter(PostMetricsModel.timestamp >= datetime.now().date() - timedelta(days=14))
            .distinct()
        ).all()

        return self.session.scalars(
            select(self.model)
            .filter(self.model.id.in_(group_ids))
            .options(selectinload(self.model.post_metrics))
        ).all()

    def get_by_external_id(self, external_id):
        return self.session.scalars(select(self.model).filter_by(external_id=external_id)).one_or_none()

class PredictiveModelsRepository(BaseRepository[PredictiveModelsModel]):
    def __init__(self, session):
        super().__init__(session, PredictiveModelsModel)

    def get_by_group_id(self, group_id):
        return self.session.scalars(select(self.model).filter_by(group_id=group_id)).all()


class PostMetricsRepository(BaseRepository[PostMetricsModel]):
    def __init__(self, session):
        super().__init__(session, PostMetricsModel)

    def get_by_group_id(self, group_id):
        return self.session.scalars(select(self.model).filter_by(group_id=group_id)).all()
