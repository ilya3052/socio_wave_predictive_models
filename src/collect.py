from src.core.database import Session
from src.repositories import GroupsRepository


def get_groups_with_metrics():
    with Session() as session:
        group_repo = GroupsRepository(session)
        return group_repo.get_groups_with_metrics()
