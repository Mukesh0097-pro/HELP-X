import os
import uuid
import httpx
from typing import Optional, Tuple

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

FACEBOOK_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
FACEBOOK_USERINFO_URL = "https://graph.facebook.com/me"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)


def build_google_login_url(redirect_uri: str, state: Optional[str] = None) -> str:
    client_id = get_env("GOOGLE_CLIENT_ID")
    if not client_id:
        raise RuntimeError("GOOGLE_CLIENT_ID is not set")
    scopes = "openid email profile"
    state = state or str(uuid.uuid4())
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scopes,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    from urllib.parse import urlencode
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_google_code_for_user(code: str, redirect_uri: str) -> Tuple[str, str, str]:
    """Return (email, name, provider_user_id) for Google user."""
    client_id = get_env("GOOGLE_CLIENT_ID")
    client_secret = get_env("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Google OAuth env vars missing")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    with httpx.Client(timeout=10) as client:
        token_resp = client.post(GOOGLE_TOKEN_URL, data=data)
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        if not access_token:
            raise RuntimeError("Failed to obtain Google access token")

        user_resp = client.get(
            GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
        )
        user_resp.raise_for_status()
        info = user_resp.json()
        email = info.get("email")
        name = info.get("name") or info.get("given_name") or "Google User"
        sub = info.get("sub") or info.get("id") or ""
        if not email:
            raise RuntimeError("Google did not return an email; ensure 'email' scope is granted")
        return email, name, sub


def build_facebook_login_url(redirect_uri: str, state: Optional[str] = None) -> str:
    client_id = get_env("FACEBOOK_CLIENT_ID")
    if not client_id:
        raise RuntimeError("FACEBOOK_CLIENT_ID is not set")
    state = state or str(uuid.uuid4())
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "email,public_profile",
        "state": state,
    }
    from urllib.parse import urlencode
    return f"{FACEBOOK_AUTH_URL}?{urlencode(params)}"


def exchange_facebook_code_for_user(code: str, redirect_uri: str) -> Tuple[str, str, str]:
    """Return (email, name, provider_user_id) for Facebook user."""
    client_id = get_env("FACEBOOK_CLIENT_ID")
    client_secret = get_env("FACEBOOK_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Facebook OAuth env vars missing")

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }
    with httpx.Client(timeout=10) as client:
        token_resp = client.get(FACEBOOK_TOKEN_URL, params=params)
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        if not access_token:
            raise RuntimeError("Failed to obtain Facebook access token")

        user_params = {"fields": "id,name,email", "access_token": access_token}
        user_resp = client.get(FACEBOOK_USERINFO_URL, params=user_params)
        user_resp.raise_for_status()
        info = user_resp.json()
        email = info.get("email")
        name = info.get("name") or "Facebook User"
        fid = info.get("id") or ""
        if not email:
            raise RuntimeError("Facebook did not return an email; ensure 'email' permission is granted")
        return email, name, fid
