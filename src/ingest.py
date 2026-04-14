import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER     = os.getenv("DB_USER", "iot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iot_senha123")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "iot_db")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def conectar():
    engine = create_engine(DATABASE_URL)
    print("Conexao com o banco estabelecida!")
    return engine


def carregar_csv(caminho: str) -> pd.DataFrame:
    print(f"Lendo arquivo: {caminho}")
    df = pd.read_csv(caminho)
    df.columns = [c.strip().lower().replace("/", "_").replace(" ", "_") for c in df.columns]
    rename_map = {
        "room_id_id": "device_id",
        "noted_date": "reading_timestamp",
        "temp":       "temperature",
        "out_in":     "location_type",
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)
    df["reading_timestamp"] = pd.to_datetime(df["reading_timestamp"], dayfirst=True, errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df.dropna(subset=["temperature", "reading_timestamp"], inplace=True)
    print(f"{len(df):,} registros carregados apos limpeza.")
    return df


def inserir_dados(df: pd.DataFrame, engine):
    print("Inserindo dados no PostgreSQL...")
    df.to_sql("temperature_readings", con=engine, if_exists="replace", index=False, chunksize=10_000)
    print(f"{len(df):,} registros inseridos!")


def criar_views(engine):
    sql = """
    CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
    SELECT device_id,
           ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
           ROUND(MIN(temperature)::numeric, 2) AS min_temp,
           ROUND(MAX(temperature)::numeric, 2) AS max_temp,
           COUNT(*) AS total_leituras
    FROM temperature_readings GROUP BY device_id ORDER BY avg_temp DESC;

    CREATE OR REPLACE VIEW leituras_por_hora AS
    SELECT EXTRACT(HOUR FROM reading_timestamp)::int AS hora,
           COUNT(*) AS contagem,
           ROUND(AVG(temperature)::numeric, 2) AS avg_temp_hora
    FROM temperature_readings GROUP BY hora ORDER BY hora;

    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
    SELECT DATE(reading_timestamp) AS data,
           ROUND(MAX(temperature)::numeric, 2) AS temp_max,
           ROUND(MIN(temperature)::numeric, 2) AS temp_min,
           ROUND(AVG(temperature)::numeric, 2) AS temp_media,
           COUNT(*) AS leituras_dia
    FROM temperature_readings GROUP BY DATE(reading_timestamp) ORDER BY data;
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("3 views SQL criadas!")


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "iot-temp.csv")
    if not os.path.exists(csv_path):
        print(f"ERRO: Arquivo nao encontrado em {csv_path}")
        print("Baixe em: https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices")
        return
    engine = conectar()
    df = carregar_csv(csv_path)
    inserir_dados(df, engine)
    criar_views(engine)
    print("\nPipeline concluido! Execute: streamlit run src/dashboard.py")


if __name__ == "__main__":
    main()
