import time, requests, streamlit as st
from ..config import HTTP_TIMEOUT, HTTP_RETRIES, HTTP_BACKOFF, USER_AGENT

def retry_get(url: str):
    err = None
    for i in range(HTTP_RETRIES):
        try:
            r = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
            r.raise_for_status()
            return r
        except Exception as e:
            err = e
            if i < HTTP_RETRIES - 1:
                time.sleep(HTTP_BACKOFF * (2 ** i))
    st.session_state["last_error"] = f"{err}" if err else "Unknown network error"
    return None