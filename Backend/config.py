"""This module extracts information from your `.env` file so that
you can use your AplhaVantage API key in other parts of the application.
"""

import os
from pydantic_settings import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    """Uses os to return the correct path of the `.env` file."""
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path


class Settings(BaseSettings):
    """Uses pydantic to define settings for project."""

    alpha_api_key: str
    db_name: str = "stocks.db"  # Add default value
    model_directory: str = "./models"  # Add default value

    class Config:
        env_file = return_full_path(".env")
        # This allows pydantic to read from environment variables even if .env doesn't exist
        env_file_encoding = 'utf-8'
        case_sensitive = False  # This allows ALPHA_API_KEY to match alpha_api_key


# Create instance of `Settings` class
settings = Settings()
