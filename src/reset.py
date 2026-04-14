import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER     = os.getenv("DB_USER", "iot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iot_senha123")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "iot_db")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def reset_db():
    print("▸ Iniciando limpeza do banco de dados...")

    engine = create_engine(DATABASE_URL)

    sql = """
    DROP VIEW IF EXISTS avg_temp_por_dispositivo;
    DROP VIEW IF EXISTS leituras_por_hora;
    DROP VIEW IF EXISTS temp_max_min_por_dia;
    DROP TABLE IF EXISTS temperature_readings;
    """

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    print("▸ Views removidas: avg_temp_por_dispositivo, leituras_por_hora, temp_max_min_por_dia")
    print("▸ Tabela removida: temperature_readings")
    print("\n▸ Banco de dados limpo com sucesso!")
    print("▸ Para reinserir os dados, execute: python src/ingest.py")


if __name__ == "__main__":
    confirmation = input("▸ Tem certeza que deseja apagar todos os dados? (s/n): ").strip().lower()
    if confirmation == "s":
        os.system("cls" if os.name == "nt" else "clear")
        reset_db()
    else:
        print("▸ Operação cancelada.")