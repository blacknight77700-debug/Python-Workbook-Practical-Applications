"""
======================================================================
THANKSGIVING FOOD DRIVE INVENTORY & REPORTING SYSTEM - README NOTE
======================================================================

1. DATA FILES:
   - inventory.txt: Persists the active inventory state. Stored as 
     flat, comma-separated lines ("ItemName,Quantity"). Automatically 
     created and seeded with a quantity of 0 on first execution if missing.
   - transactions.txt: Maintains a permanent audit trail. Appends a 
     timestamped log entry ("Month-DD-YYYY HH:MM AM/PM - Updated [Item]...") 
     every time a quantity is successfully modified.

2. HOW BASKETS ARE CALCULATED:
   - The system evaluates all items within the `catalog_basket` dictionary 
     against current inventory levels. 
   - It identifies the lowest stock level to determine the maximum 
     number of complete Thanksgiving food baskets that can be assembled, 
     while capturing any "limiting items" (handling ties) that restrict 
     further basket assembly.

3. HOW TOP/BOTTOM-5 EXTREMES ARE COMPUTED:
   - Filters basket items to ensure they exist within the active inventory.
   - Implements a deterministic two-tier sorting algorithm via a lambda key 
     tuple: primary sorting by quantity (ascending), with an alphabetical 
     name tie-breaker for consistent ordering.
   - Slices the sorted dataset to extract the bottom 5 (critical shortages) 
     and top 5 (well-stocked items) for reporting.
======================================================================
"""
