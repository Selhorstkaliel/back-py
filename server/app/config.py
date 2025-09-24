from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 3001
    NODE_ENV: str = "development"
    SQLITE_PATH: str = "./data/dev.sqlite"
    JWT_PRIVATE_KEY: str | None = None
    JWT_PUBLIC_KEY: str | None = None
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    CPF_CNPJ_PUBLIC_API: str = "https://ws.hubdodesenvolvedor.com.br/v2/cpf-cnpj/?cpfcnpj="

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()