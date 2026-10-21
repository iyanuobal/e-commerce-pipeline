
import csv
import os
import logging
from pathlib import Path


def check_files(folder, expected_files):
    present = os.listdir(folder)
    missing = []
    for file in expected_files:
        if file not in present:
            missing.append(file)
    return missing

folder = r"C:\Users\iyanu\OneDrive\Documents\My_Cap_Pro\ecommerce\pipeline\data\raw\olist"
EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
    #"fake.csv"
]          



def get_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
    return header



from datetime import datetime, timezone
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq

#Ingestion: Bronze Layer
def ingest_data(file_path, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        #Read the CSV. keeping every column as a string (Bronze = raw)
        header = get_header(file_path)
        convert_options = pv.ConvertOptions(column_types = {col: pa.string() for col in header})
        table = pv.read_csv(file_path, convert_options = convert_options)

        #Add the ingestion timestamp column
        _ingested_at_ = datetime.now(timezone.utc)
        _source_file_ = os.path.basename(file_path)
        table = table.append_column("_ingested_at", pa.array([_ingested_at_] * len(table)))
        table = table.append_column("_source_file", pa.array([_source_file_] * len(table)))
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        out_path = os.path.join(output_folder, f"{table_name}.parquet")
        pq.write_table(table, out_path)



logging.basicConfig(
     level = logging.INFO,
     format = "%(asctime)s %(levelname)s %(message)s",
)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR= PROJECT_ROOT / "data" / "raw" / "olist" 
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze" 

def ingest_all(raw_dir, bronze_dir):
     missing = check_files(raw_dir, EXPECTED_FILES)
     if missing:
          logging.error("Missing files, stopping: %s", missing)
          return missing
     loaded = 0
     failed = []
     for file_name in sorted(os.listdir(raw_dir)):
          if not file_name.endswith(".csv"):
               continue

          table_name = os.path.splitext(file_name)[0]
          file_path = os.path.join(raw_dir, file_name)
          output_folder = os.path.join(bronze_dir, table_name)
          
          try:
            ingest_data(file_path, output_folder)
            logging.info("Loaded %s", file_name)
            loaded += 1
          except Exception:
               logging.exception("Failed to load %s", file_name)
               failed.append(file_name)
     logging.info("Done: %d loaded, %d failed", loaded, len(failed))
     return failed


ingest_all(RAW_DIR, BRONZE_DIR)