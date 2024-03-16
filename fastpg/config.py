"""fastpg config."""

import json
import pathlib
from typing import Any, Dict, List, Optional
from pathlib import Path

from pydantic import (
    BaseModel,
    DirectoryPath,
    Field,
    PostgresDsn,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """API settings"""

    name: str = "FastPG: FastAPI Implementation of PostgreSQL"
    debug: bool = False
    cors_origins: List[str] = ["*"]
    version : str = "0.0.1"
    description: str = "Convert your PostgreSQL Database into executable APIs"
    docs_url: str = "/"
    username: str
    schema: str
    password: str
    host: str
    port: int
    dbname: str
    db_min_conn_size: int = 1
    db_max_conn_size: int = 10
    db_max_queries: int = 50000
    db_max_inactive_conn_lifetime: float = 300
    class Config:
        env_file = Path(Path(__file__).resolve().parent) / ".env"


settings = APISettings()
