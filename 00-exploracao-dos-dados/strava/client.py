import os
import time
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    logger.info(f"Variáveis de ambiente carregadas de {ENV_PATH}")
else:
    logger.warning(f"Arquivo .env não encontrado em {ENV_PATH}")

class StravaAPIClient:


    def __init__(self):
        self.base_url = "https://www.strava.com/api/v3"
        self.base_url_oauth = "https://www.strava.com/oauth/token"
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.token_expiry_margin = int(os.getenv("TOKEN_EXPIRY_MARGIN_SECONDS"))
        self.access_token = None
        self.expires_at = 0

        if not self.client_id or not self.client_secret or not self.refresh_token:
            raise ValueError(
                "Client ID, Client Secret e Refresh Token são obrigatórios. Verifique as variáveis de ambiente."
            )


    def _refresh_access_token(self) -> None:
        url = self.base_url_oauth
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        print('Refreshing access token...')
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(response.status_code, response.text)
        data = response.json()
        self.access_token = data["access_token"]
        self.expires_at = data["expires_at"]
        self.refresh_token = data["refresh_token"]


    def _ensure_access_token(self) -> None:
        if not self.access_token or self.expires_at - self.token_expiry_margin <= int(time.time()):
            self._refresh_access_token()


    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        self._ensure_access_token()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


    def get_athlete(self) -> Dict[str, Any]:
            return self._get("/athlete")


    def get_activities(
        self,
        after: Optional[int] = None,
        before: Optional[int] = None,
        page: int = 1,
        per_page: int = 30,
    ) -> list[Dict[str, Any]]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        return self._get("/athlete/activities", params=params)


    def get_activity(self, activity_id: int) -> Dict[str, Any]:
        return self._get(f"/activities/{activity_id}")

    

