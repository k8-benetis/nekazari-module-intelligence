"""
Intelligence Module Backend - Configuration

Environment-based configuration using pydantic-settings.

Copyright 2026 k8-benetis

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific terms and conditions governing
permissions and limitations under the License.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Intelligence Module"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_prefix: str = "/api/intelligence"
    cors_origins: list[str] = ["*"]
    
    # Redis Configuration
    redis_host: str = "redis-service"
    redis_port: int = 6379
    redis_password: str = ""
    
    # Orion-LD Configuration
    orion_url: str = "http://orion-ld-service:1026"
    context_url: str = "https://nekazari.artotxiki.com/ngsi-ld-context.json"
    
    # Keycloak / JWT Authentication (optional - for future use)
    keycloak_url: str = "https://auth.artotxiki.com/auth"
    keycloak_realm: str = "nekazari"
    jwt_audience: str = "account"
    jwt_issuer: str = ""
    
    # Service-to-service authentication
    module_management_key: str = ""
    
    @property
    def jwt_issuer_url(self) -> str:
        """Get the JWT issuer URL."""
        if self.jwt_issuer:
            return self.jwt_issuer
        return f"{self.keycloak_url}/realms/{self.keycloak_realm}"
    
    @property
    def jwks_url(self) -> str:
        """Get the JWKS URL for token verification."""
        return f"{self.jwt_issuer_url}/protocol/openid-connect/certs"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


