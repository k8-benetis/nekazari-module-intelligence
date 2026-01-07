"""
Intelligence Module Backend - Configuration

Environment-based configuration using pydantic-settings.
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


