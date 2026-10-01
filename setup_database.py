import sqlite3
import pandas as pd

print("Initializing ERP Database...")

# 1. Create a connection to a new database file (creates it if it doesn't exist)
conn = sqlite3.connect('erp_system.db')

# 2. Load our existing synthetic CSV data
inventory_df = pd.read_csv('starting_inventory.csv')
transactions_df = pd.read_csv('transactions.csv')
physical_counts_df = pd.read_csv('physical_counts.csv')

# 3. Push the data into formal SQL tables
print("Creating SQL tables and inserting data...")
inventory_df.to_sql('starting_inventory', conn, if_exists='replace', index=False)
transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
physical_counts_df.to_sql('physical_counts', conn, if_exists='replace', index=False)

# 4. Close the connection
conn.close()
print("Success! Database 'erp_system.db' is live and populated.")