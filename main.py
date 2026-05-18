from src.collect import get_groups_with_metrics
from src.predictive_models.train import train_models_on_groups


def main():
    groups_ids = [group.id for group in get_groups_with_metrics()]
    train_result = train_models_on_groups(groups_ids)


if __name__ == "__main__":
    main()
