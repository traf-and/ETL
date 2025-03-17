import json
import psycopg2

def insert_into_postgres(conn, table_name, data):
    with conn.cursor() as cur:
        for item in data:
            if table_name == 'UserSessions'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.UserSessions (session_id, user_id, start_time, end_time, device)
                    VALUES (%s, %s, %s, %s, %s)
                """, item)
            elif table_name == 'UserSessions_actions'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.UserSessions_actions (session_id, actions)
                    VALUES (%s, %s)
                """, 
                    item)
            elif table_name == 'UserSessions_pages'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.UserSessions_pages (session_id, pages_visited)
                    VALUES (%s, %s)
                """, item)
            elif table_name == 'ProductPriceHistory'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.ProductPriceHistory (product_id, current_price, currency)
                    VALUES (%s, %s, %s)
                """, item)
            elif table_name == 'ProductPriceHistory_price_changes'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.ProductPriceHistory_price_changes (product_id, change_date, change_price)
                    VALUES (%s, %s, %s)
                """, item)
            elif table_name == 'EventLogs'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.EventLogs (event_id, timestamp, event_type, details)
                    VALUES (%s, %s, %s, %s)
                """, item)
            elif table_name == 'SupportTickets'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.SupportTickets (ticket_id, user_id, status, issue_type, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, item)
            elif table_name == 'SupportTickets_messages'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.SupportTickets_messages (ticket_id, message)
                    VALUES (%s, %s)
                """, item)
            elif table_name == 'UserRecommendations'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.UserRecommendations (user_id, last_updated)
                    VALUES (%s, %s)
                """, item)
            elif table_name == 'UserRecommendations_products'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.UserRecommendations_products (user_id, recommended_product)
                    VALUES (%s, %s)
                """, item)
            elif table_name == 'ModerationQueue'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.ModerationQueue (review_id, user_id, product_id, review_text, rating, moderation_status, submitted_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, item)
            elif table_name == 'ModerationQueue_flags'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.ModerationQueue_flags (review_id, flag)
                    VALUES (%s, %s)
                """, item)
            elif table_name == 'SearchQueries'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.SearchQueries (query_id, user_id, query_text, timestamp, results_count)
                    VALUES (%s, %s, %s, %s, %s)
                """, item)
            elif table_name == 'SearchQueries_filters'.lower():
                cur.execute("""
                    INSERT INTO mongo_data.SearchQueries_filters (query_id, filter)
                    VALUES (%s, %s)
                """, item)
        conn.commit()  # Зафиксировать изменения в базе данных

def get_ids_postgres(conn, table_name, attr):
    with conn.cursor() as cur:
        cur.execute(f"""
            select coalesce(max(substring({attr}, '\d+')::int), '0')
            from mongo_data.{table_name}
        """)
        res = cur.fetchone()[0]
    return int(res)
