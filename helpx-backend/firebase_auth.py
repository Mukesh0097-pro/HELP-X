import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

import firebase_admin
from firebase_admin import credentials, auth

_firebase_initialized = False

def _default_service_account_path() -> str:
    """Return default path to service account file in helpx-backend.

    Looks for 'firebase private key.json' next to this module.
    """
    backend_dir = Path(__file__).resolve().parent
    candidate = backend_dir / "firebase private key.json"
    return str(candidate)


def init_firebase() -> None:
    """Initialize Firebase Admin SDK using either env var or local service account JSON.

    Precedence:
    1) GOOGLE_APPLICATION_CREDENTIALS env var (absolute path)
    2) helpx-backend/firebase private key.json (local file)
    3) Application Default Credentials (if available)
    """
    global _firebase_initialized
    if _firebase_initialized:
        return

    # 1) Explicit env var path
    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path and os.path.exists(sa_path):
        cred = credentials.Certificate(sa_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return

    # 2) Local file next to backend
    local_path = _default_service_account_path()
    if os.path.exists(local_path):
        # Load JSON to ensure we can optionally enforce projectId
        with open(local_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        project_id = data.get("project_id")
        cred = credentials.Certificate(data)
        if project_id:
            firebase_admin.initialize_app(cred, {"projectId": project_id})
        else:
            firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return

    # 3) Fallback to ADC (will work on GCP or if gcloud auth application-default login done)
    try:
        firebase_admin.initialize_app()
        _firebase_initialized = True
    except Exception as e:
        raise RuntimeError(
            "Firebase Admin not initialized. Provide service account JSON via GOOGLE_APPLICATION_CREDENTIALS or place 'firebase private key.json' in helpx-backend."
        ) from e


def verify_id_token(id_token: str) -> Dict[str, Any]:
    """Verify Firebase ID token and return decoded claims."""
    init_firebase()
    decoded = auth.verify_id_token(id_token)
    return decoded


def extract_user_info(claims: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Extracts uid, email, and display name from Firebase claims."""
    return {
        "uid": claims.get("uid") or claims.get("user_id"),
        "email": claims.get("email"),
        "name": claims.get("name") or claims.get("displayName"),
    }
