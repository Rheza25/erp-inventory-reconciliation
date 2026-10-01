import pandas as pd
import sqlite3

print("Connecting to live ERP Database...")
# 1. Open the secure connection to the database
conn = sqlite3.connect('erp_system.db')

# 2. Use standard SQL queries to extract data directly into Pandas DataFrames
inventory_df = pd.read_sql('SELECT * FROM starting_inventory', conn)
transactions_df = pd.read_sql('SELECT * FROM transactions', conn)
physical_counts_df = pd.read_sql('SELECT * FROM physical_counts', conn)

# 3. Close the connection immediately after extraction (Best Practice)
conn.close()
print("Data successfully extracted via SQL.")

# 4. Calculate total net movement per item and warehouse
print("\nCalculating net inventory movements...")
net_movements = transactions_df.groupby(['item_id', 'warehouse_id'])['qty'].sum().reset_index()
net_movements = net_movements.rename(columns={'qty': 'total_movement'})

# 5. Merge movements with starting inventory to calculate Expected Balance
print("Merging with starting inventory...")
expected_inventory = pd.merge(inventory_df, net_movements, on=['item_id', 'warehouse_id'], how='left')
expected_inventory['total_movement'] = expected_inventory['total_movement'].fillna(0)
expected_inventory['expected_balance'] = expected_inventory['opening_balance'] + expected_inventory['total_movement']

# 6. Merge with Physical Counts to find Discrepancies
print("\nComparing expected balances with physical counts...")
final_reconciliation = pd.merge(expected_inventory, physical_counts_df, on=['item_id', 'warehouse_id'], how='left')
final_reconciliation['variance'] = final_reconciliation['expected_balance'] - final_reconciliation['counted_qty']
discrepancies = final_reconciliation[final_reconciliation['variance'] != 0]

# 7. Hunt down the Root Cause (The Phantom Increases)
print("\nAnalyzing transaction logs for root causes...")
suspicious_txns = transactions_df[transactions_df['txn_type'] == 'System_Adjustment']
audit_trail = pd.merge(
    discrepancies[['item_id', 'warehouse_id', 'variance']], 
    suspicious_txns, 
    on=['item_id', 'warehouse_id'], 
    how='inner'
)

print(f"\n--- Found {len(audit_trail)} Phantom Increase Transactions ---")
print(audit_trail[['item_id', 'warehouse_id', 'variance', 'txn_id', 'txn_type', 'qty', 'user_id']])

# 8. Export the Final Reports for Management/Auditors
print("\nExporting final reports to CSV...")
final_reconciliation.to_csv('reconciliation_summary.csv', index=False)
audit_trail.to_csv('phantom_increase_audit_log.csv', index=False)

print("Success! Reports generated:")
print("- reconciliation_summary.csv")
print("- phantom_increase_audit_log.csv")
print("\nReconciliation Engine run complete.")