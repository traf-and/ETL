import random
from datetime import datetime, timedelta
import json
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from module.mongo_utils import get_mongo_data
from module.postgre_utils import insert_into_postgres, get_ids_postgres


def parse_EventLogs(data:list):
    out = [0]*len(data)
    for ind, row in enumerate(data):
        out[ind] = (row['event_id'], 
                    row['timestamp'], 
                    row['event_type'], 
                    row['details'])
    return out

def parse_ModerationQueue(data:list):
    out = [0]*len(data)
    flags = []
    for ind, row in enumerate(data):
        out[ind] = (row['review_id'], 
                    row['user_id'], 
                    row['product_id'], 
                    row['review_text'],
                    row['rating'],
                    row['moderation_status'],
                    row['submitted_at'])
        
        for flag in row['flags']:
            flags.append((row['review_id'], flag))

    return out, flags

def parse_ProductPriceHistory(data:list):
    out = [0]*len(data)
    changes = []
    for ind, row in enumerate(data):
        out[ind] = (row['product_id'], 
                    row['current_price'], 
                    row['currency'])
        
        for change in row['price_changes']:
            changes.append((row['product_id'],change['date'],change['price']))

    return out, changes

def parse_SearchQueries(data:list):
    out = [0]*len(data)
    filters = []
    for ind, row in enumerate(data):
        out[ind] = (row['query_id'], 
                    row['user_id'], 
                    row['query_text'],
                    row['timestamp'],
                    row['results_count'])
        
        for filter in row['filters']:
            filters.append((row['query_id'],filter))

    return out, filters

def parse_SupportTickets(data:list):
    out = [0]*len(data)
    messages = []
    for ind, row in enumerate(data):
        out[ind] = (row['ticket_id'], 
                    row['user_id'], 
                    row['status'],
                    row['issue_type'],
                    row['created_at'],
                    row['updated_at'])
        
        for message in row['messages']:
            messages.append((row['ticket_id'], message))

    return out, messages

def parse_UserRecommendations(data:list):
    out = []#[0]*len(data)
    recommended_products = []
    usr = {}
    for ind, row in enumerate(data):
        if row['user_id'] in usr:
            usr[row['user_id']] += [row['last_updated']]
        else:
            usr[row['user_id']] = [row['last_updated']]
        
        for product in row['recommended_products']:
            recommended_products.append((row['user_id'], product))

    for k,v in usr.items():
        out.append((k, max(v)))

    return out, recommended_products

def parse_UserSessions(data:list):
    out = [0]*len(data)
    pages_visited = []
    actions = []
    for ind, row in enumerate(data):
        out[ind] = (row['session_id'], 
                    row['user_id'],
                    row['start_time'],
                    row['end_time'],
                    row['device'])
        
        for page in row['pages_visited']:
            pages_visited.append((row['session_id'], page))

        for action in row['actions']:
            actions.append((row['session_id'], action))

    return out, pages_visited, actions

def load_data_to_postgre() -> None:
    collections = [
        'UserSessions',
        'ProductPriceHistory',
        'EventLogs',
        'SupportTickets',
        'UserRecommendations',
        'ModerationQueue',
        'SearchQueries'
    ]


    conn = PostgresHook('postgres_conn_id').get_conn()

    tb = 'EventLogs'
    attr = 'event_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data = parse_EventLogs(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)

    tb = 'ModerationQueue'
    attr = 'review_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data, flags = parse_ModerationQueue(data)
        print(data)
        print(flags)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_flags', flags)

    tb = 'ProductPriceHistory'
    attr = 'product_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(id_val)
    print(data)
    if data:
        data, price_changes = parse_ProductPriceHistory(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_price_changes', price_changes)

    tb = 'SearchQueries'
    attr = 'query_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data, filters = parse_SearchQueries(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_filters', filters)

    tb = 'SupportTickets'
    attr = 'ticket_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data, messages = parse_SupportTickets(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_messages', messages)

    tb = 'UserRecommendations'
    attr = 'user_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data, products = parse_UserRecommendations(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_products', products)

    tb = 'UserSessions'
    attr = 'session_id'
    print(tb)
    id_val = get_ids_postgres(conn, tb, attr)
    data = get_mongo_data(tb, attr, id_val)
    print(data)
    if data:
        data, actions, pages = parse_UserSessions(data)
        tb = tb.lower()
        insert_into_postgres(conn, tb, data)
        insert_into_postgres(conn, f'{tb}_actions', actions)
        insert_into_postgres(conn, f'{tb}_pages', pages)

    print('OK')

    conn.close()

dag = DAG('dag_dag_load_data_to_postgre',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 3, 16))


task_load_data_to_postgre = PythonOperator( 
    task_id='load_data_to_postgre',
    python_callable=load_data_to_postgre,
    dag=dag,
    provide_context=True
)

task_load_data_to_postgre
