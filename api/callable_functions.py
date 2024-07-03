import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from typing import Any
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import insert
import os
from dotenv import load_dotenv 
from db import get_connection
load_dotenv()

use_sql = os.getenv("use_sql")
use_sql = use_sql == 'True'
if use_sql:
    engine = get_connection()
    conn = engine.connect()

def GetOrderDetails(order_id):
    if use_sql:
        user_product = pd.read_sql(f"SELECT * FROM user_products WHERE order_id = '{order_id}'", conn)
    else:
        user_product = pd.read_csv('user_products.csv')
        user_product = user_product[user_product.order_id == order_id]
    
    order_id = user_product['order_id'].iloc[0]
    description = user_product['description'].iloc[0]
    purchased_at = str(user_product['purchased_at'].iloc[0])
    price = str(user_product['price'].iloc[0])
    
    return f'''Its a product  with decsription {description} you purchase at {purchased_at} costed ₹{price}'''

def CancelOrder(order_id):
    if use_sql:
        user_product = pd.read_sql(f"SELECT * FROM user_products WHERE order_id = '{order_id}'", conn)
    else:
        user_product = pd.read_csv('user_products.csv')
        user_product = user_product[user_product.order_id == order_id]
        
    status = user_product.status.iloc[0]
    expected_delivary = user_product.expected_delivary.iloc[0]
    
    if status not in ('delivered', 'cancelled'):
        
        sql_query = text(f'''UPDATE user_products
        SET status = 'cancelled'
        WHERE order_id = {order_id};''')
        conn.execute(sql_query)
        
        return f'As you have requested we have cancelled the product'
    
    if status == 'delivered':
        return f'The product was delivered to on {str(expected_delivary)}, I am afraid we cant cancel this order, but you can request for return of this order, shall I raise a request to return the order?'
    
    if status == 'cancelled':
        return 'This product is already cancelled'

def GetOrderStatus(order_id):
    if use_sql:
        user_product = pd.read_sql(f"SELECT * FROM user_products WHERE order_id = '{order_id}'", conn)
    else:
        user_product = pd.read_csv('user_products.csv')
        user_product = user_product[user_product.order_id == order_id]
        
    status = user_product.status.iloc[0]
    return f'Your product is {status}'

def ReturnOrder(order_id):
    
    if use_sql:
    
        sql_query = text(f'''UPDATE user_products
            SET status = 'return initiated'
            WHERE order_id = {order_id};''')
        conn.execute(sql_query)
    
    return 'Return order initiated, Our delivery partner will pick up the prduct within 2 days!'

def GetRefundStatus(order_id):
    return 'refund status'

def ReplaceOrder(order_id):
    return 'ReplaceOrder'

def HumanSupport(order_id):
    return 'HumanSupport'

def ChangeDelivaryTime(order_id):
    return 'ChangeDelivaryTime'

def OrderTracking(order_id):
    return 'OrderTracking'

def RefundStatus(order_id):
    return 'RefundStatus'

def ReplacementPolicy(order_id):
    return 'ReplacementPolicy'

def CancellationPolicy(order_id):
    return 'CancellationPolicy'

def ReturnPolicy(order_id):
    return 'ReturnPolicy'

def CashbackOrRewards(order_id):
    return 'CashbackOrRewards'

def DownloadInvoice(order_id):
    return 'DownloadInvoice'

def HumanSupport(order_id):
    return 'HumanSupport in not received'

