import json
import time
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import requests

from client import StravaAPIClient

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
DETAILS_DIR = RAW_DIR / "details"
ATHLETE_FILE = RAW_DIR / "athlete.json"
ACTIVITIES_FILE = RAW_DIR / "activities.json"

REQUEST_DELAY_SECONDS = 0.2
SAFETY_MARGIN_SECONDS = 7 * 24 * 60 * 60
MAX_PAGES = 100
RATE_LIMIT_WAIT_SECONDS = 900


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _get_with_retry(fetch_fn, *args, max_retries: int = 3, **kwargs):
    for attempt in range(max_retries):
        try:
            return fetch_fn(*args, **kwargs)
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 429:
                if attempt == max_retries - 1:
                    raise
                print(
                    f"Limite de requisições atingido. "
                    f"Aguardando {RATE_LIMIT_WAIT_SECONDS}s antes de tentar novamente..."
                )
                time.sleep(RATE_LIMIT_WAIT_SECONDS)
            else:
                raise
    return None


def fetch_athlete(client: StravaAPIClient, output_file: Path = ATHLETE_FILE) -> None:
    athlete = _get_with_retry(client.get_athlete)
    _write_json(output_file, athlete)
    print(f"Dados do atleta salvos em {output_file}")


def fetch_activities(client: StravaAPIClient, activities_file: Path = ACTIVITIES_FILE, per_page: int = 200) -> None:
  
    existing = _read_json(activities_file, default=[])

    if existing:
        last_date = max(activity["start_date"] for activity in existing)
        after = int(pd.to_datetime(last_date).timestamp()) - SAFETY_MARGIN_SECONDS
        print(f"Base existente com {len(existing)} atividades. Buscando novidades...")
    else:
        after = None
        print("Nenhuma base encontrada. Buscando histórico completo...")

    new_activities = []

    for page in range(1, MAX_PAGES + 1):
        activities = _get_with_retry(
            client.get_activities, after=after, page=page, per_page=per_page
        )
        if not activities:
            break

        new_activities.extend(activities)
        print(f"  página {page}: {len(activities)} atividades")
        time.sleep(REQUEST_DELAY_SECONDS)
    else:
        print(f"Aviso: limite de {MAX_PAGES} páginas atingido. Pode haver mais dados.")

    if not new_activities:
        print("Nenhuma nova atividade encontrada.")
        return

    merged = {activity["id"]: activity for activity in existing}
    merged.update({activity["id"]: activity for activity in new_activities})

    result = sorted(merged.values(), key=lambda activity: activity["start_date"])
    _write_json(activities_file, result)

    added = len(result) - len(existing)
    print(f"{added} atividades novas. Total: {len(result)} em {activities_file}")


def fetch_activity_details(client: StravaAPIClient, activities_file: Path = ACTIVITIES_FILE, details_dir: Path = DETAILS_DIR, limit: Optional[int] = None) -> None:
    activities = _read_json(activities_file, default=[])

    if not activities:
        print(f"Nenhuma atividade em {activities_file}. Rode fetch_activities primeiro.")
        return

    details_dir.mkdir(parents=True, exist_ok=True)

    all_ids = {activity["id"] for activity in activities}
    fetched_ids = {int(path.stem) for path in details_dir.glob("*.json")}
    pending_ids = sorted(all_ids - fetched_ids)

    if not pending_ids:
        print("Todas as atividades já foram detalhadas.")
        return

    to_fetch = pending_ids[:limit] if limit else pending_ids
    print(f"{len(pending_ids)} pendentes. Buscando {len(to_fetch)} nesta execução.")

    for index, activity_id in enumerate(to_fetch, start=1):
        try:
            activity = _get_with_retry(client.get_activity, activity_id)
        except requests.exceptions.HTTPError as exc:
            print(f"  [{index}/{len(to_fetch)}] {activity_id}: falhou ({exc}). Pulando.")
            continue

        _write_json(details_dir / f"{activity_id}.json", activity)
        print(f"  [{index}/{len(to_fetch)}] {activity_id} salva")
        time.sleep(REQUEST_DELAY_SECONDS)

    remaining = len(pending_ids) - len(to_fetch)
    if remaining:
        print(f"Concluído. Ainda faltam {remaining} atividades.")
    else:
        print(f"Concluído. Todos os detalhes estão em {details_dir}")


def main() -> None:
    client = StravaAPIClient()

    fetch_athlete(client)
    fetch_activities(client)
    fetch_activity_details(client, limit=200)


if __name__ == "__main__":
    main()