import random
from datetime import datetime, timedelta
import json
from faker import Faker

from module.mongo_utils import get_max_id

fake = Faker()

session_id_counter = get_max_id('UserSessions', 'session_id')
product_id_counter = get_max_id('ProductPriceHistory', 'product_id')
event_id_counter = get_max_id('EventLogs', 'event_id')
ticket_id_counter = get_max_id('SupportTickets', 'ticket_id')
query_id_counter = get_max_id('SearchQueries', 'query_id')
review_id_counter = get_max_id('ModerationQueue', 'review_id')

num_sessions = 5
num_products = 5
num_events = 10
num_tickets = 3
num_users = 7
num_recommendations = 5
num_reviews = 5
num_search_queries = 5

def generate_user_sessions():
    global session_id_counter
    sessions = []
    for _ in range(num_sessions):
        start_time = fake.date_time_this_year()
        duration = timedelta(minutes=random.randint(15, 120))
        end_time = start_time + duration
        pages_visited = [fake.uri_page() for _ in range(random.randint(1, 5))]
        device = fake.user_agent()
        actions = [random.choice(['click', 'scroll', 'hover', 'input']) for _ in range(random.randint(1, 5))]
        
        session = {
            'session_id': f'session_{session_id_counter}',
            'user_id': f'user_{random.randint(1, num_users)}',
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'pages_visited': pages_visited,
            'device': device,
            'actions': actions
        }
        sessions.append(session)
        session_id_counter += 1
    return sessions

def generate_product_price_history():
    global product_id_counter
    products = []
    for _ in range(num_products):
        price_changes = [
            {
                'date': fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
                'price': round(random.uniform(10.0, 1000.0), 2)
            } for _ in range(random.randint(1, 5))
        ]
        current_price = round(random.uniform(10.0, 1000.0), 2)
        currency = fake.currency_code()

        product = {
            'product_id': f'product_{product_id_counter}',
            'price_changes': price_changes,
            'current_price': current_price,
            'currency': currency
        }
        products.append(product)
        product_id_counter += 1
    return products

def generate_event_logs():
    global event_id_counter
    events = []
    for _ in range(num_events):
        event_type = random.choice(['login', 'logout', 'purchase', 'view', 'error'])
        details = fake.sentence()

        event = {
            'event_id': f'event_{event_id_counter}',
            'timestamp': fake.date_time_this_year().isoformat(),
            'event_type': event_type,
            'details': details
        }
        events.append(event)
        event_id_counter += 1
    return events

def generate_support_tickets():
    global ticket_id_counter
    tickets = []
    for _ in range(num_tickets):
        messages = [fake.sentence() for _ in range(random.randint(1, 3))]
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(1, 10))

        ticket = {
            'ticket_id': f'ticket_{ticket_id_counter}',
            'user_id': f'user_{random.randint(1, num_users)}',
            'status': random.choice(['open', 'in_progress', 'closed']),
            'issue_type': fake.word(),
            'messages': messages,
            'created_at': created_at.isoformat(),
            'updated_at': updated_at.isoformat()
        }
        tickets.append(ticket)
        ticket_id_counter += 1
    return tickets

def generate_user_recommendations():
    recommendations = []
    for user_id in range(1, num_users + 1):
        recommended_products = [f'product_{random.randint(1, num_products)}' for _ in range(random.randint(1, 5))]
        last_updated = fake.date_time_this_year()

        recommendation = {
            'user_id': f'user_{user_id}',
            'recommended_products': recommended_products,
            'last_updated': last_updated.isoformat()
        }
        recommendations.append(recommendation)

    return recommendations

def generate_moderation_queue():
    global review_id_counter
    reviews = []
    for _ in range(num_reviews):
        review_text = fake.paragraph()
        rating = random.randint(1, 5)

        review = {
            'review_id': f'review_{review_id_counter}',
            'user_id': f'user_{random.randint(1, num_users)}',
            'product_id': f'product_{random.randint(1, num_products)}',
            'review_text': review_text,
            'rating': rating,
            'moderation_status': random.choice(['pending', 'approved', 'rejected']),
            'flags': [fake.word() for _ in range(random.randint(0, 2))],
            'submitted_at': fake.date_time_this_year().isoformat()
        }
        reviews.append(review)
        review_id_counter += 1

    return reviews

def generate_search_queries():
    global query_id_counter
    queries = []
    for _ in range(num_search_queries):
        filters = fake.words(nb=random.randint(1, 3))

        query = {
            'query_id': f'query_{query_id_counter}',
            'user_id': f'user_{random.randint(1, num_users)}',
            'query_text': fake.sentence(),
            'timestamp': fake.date_time_this_year().isoformat(),
            'filters': filters,
            'results_count': random.randint(1, 100)
        }
        queries.append(query)
        query_id_counter += 1

    return queries

if __name__ == "__main__":
    data = {
        'UserSessions': generate_user_sessions(),
        'ProductPriceHistory': generate_product_price_history(),
        'EventLogs': generate_event_logs(),
        'SupportTickets': generate_support_tickets(),
        'UserRecommendations': generate_user_recommendations(),
        'ModerationQueue': generate_moderation_queue(),
        'SearchQueries': generate_search_queries(),
    }

    with open('random_data.json', 'w') as f:
        json.dump(data, f, indent=4)
