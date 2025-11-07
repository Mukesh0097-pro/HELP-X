import os
from typing import Optional, Dict, Any

import firebase_admin
from firebase_admin import credentials, auth

_firebase_initialized = False

def init_firebase() -> None:
    global _firebase_initialized
    if _firebase_initialized:
        return

    # Prefer explicit service account path
    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path and os.path.exists(sa_path):
        cred = credentials.Certificate(sa_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return

    # Fallback to default credentials (e.g., env or metadata)
    try:
        firebase_admin.initialize_app()
        _firebase_initialized = True
    except Exception as e:
        raise RuntimeError(
            "Firebase Admin not initialized. Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON."
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
