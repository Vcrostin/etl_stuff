from dataclasses import dataclass, asdict
from pymongo import MongoClient
import uuid
import random
import logging

from common import MONGO_URL, DataBases, DATABASE, model


def generate_id(num : int) -> list[str]:
    users_id = []
    for _ in range(num):
        users_id.append(str(uuid.uuid4()))
    return users_id


@dataclass
class UserSessionsGen:
    session_id: str
    user_id: str
    start_time: int
    end_time: int
    pages_visited: int
    device: str
    actions: list[str]

    @staticmethod
    def gen_class(users_id : list[str], _ : list[str]):
        user_sessions = []
        for user_id in users_id:
            start_time = random.randint(0, 1000)
            user_sessions.append(
                UserSessionsGen(
                    session_id=str(uuid.uuid4()),
                    user_id=user_id,
                    start_time=start_time,
                    end_time=random.randint(start_time, start_time+100),
                    pages_visited=random.randint(1, 10),
                    device=random.choice(["touch", "desktop"]),
                    actions=["Did sth"],
                )
            )
        return user_sessions


@dataclass
class ProductPriceHistoryGen:
    product_id: str
    price_changes: list[tuple[int, int]]
    current_price: int
    currency: str

    @staticmethod
    def gen_class(_ : list[str], products_id : list[str]):
        product_price_histories = []
        for product_id in products_id:
            start_time = random.randint(0, 1000)
            price_changes = []
            prev_time = 0
            for i in range(random.randint(1, 10)):
                new_time = random.randint(prev_time, prev_time + 100)
                price_changes.append(tuple([new_time, random.randint(1, 1000)]))
                prev_time = new_time
            product_price_histories.append(
                ProductPriceHistoryGen(
                    product_id=product_id,
                    price_changes=price_changes,
                    current_price=random.randint(1, 1000),
                    currency=random.choice(["₽", "$", "€"])
                )
            )
        return product_price_histories


@dataclass
class EventLogsGen:
    event_id: str
    timestamp: int
    event_type: int
    details: str

    @staticmethod
    def gen_class(_ : list[str], __ : list[str]):
        event_logs = []
        details_sent = model("New occured event",
            do_sample=True, top_k=50,
            temperature=0.9, max_length=15, truncation=True)
        details = []
        for i in details_sent:
            details.append(i["generated_text"])
        for _ in range(random.randint(100, 500)):
            event_logs.append(
                EventLogsGen(
                    event_id=str(uuid.uuid4()),
                    timestamp=random.randint(100, 2000),
                    event_type=random.choice(["Access", "Share", "Sth idk"]),
                    details="".join(details),
                )
            )
        return event_logs


@dataclass
class SupportTicketsGen:
    ticket_id: str
    user_id: str
    status: str
    issue_type: str
    messages: list[str]
    created_at: int
    updated_at: int

    @staticmethod
    def gen_class(user_id : list[str], _ : list[str]):
        support_tickets = []
        messages_model = model("I have a new problem with",
            do_sample=True, top_k=50,
            temperature=0.9, max_length=100, truncation=True)
        messages = []
        for i in messages_model:
            messages.append(i["generated_text"])
        for user_id in user_id:
            support_tickets.append(
                SupportTicketsGen(
                    ticket_id=str(uuid.uuid4()),
                    user_id=user_id,
                    status=random.choice(["done", "open", "in progress"]),
                    issue_type=random.choice(["task", "Q&A", "epic"]),
                    messages="".join(messages),
                    created_at=random.randint(1, 1000),
                    updated_at=random.randint(1000, 2000),
                )
            )
        return support_tickets


@dataclass
class UserRecommendationsGen:
    user_id: str
    recomended_products: list[str]
    last_updated: int

    @staticmethod
    def gen_class(user_id : list[str], products_id : list[str]):
        user_recomendations = []
        for user_id in user_id:
            user_recomendations.append(
                UserRecommendationsGen(
                    user_id=user_id,
                    recomended_products=random.choices(products_id, k=random.randint(1, 10)),
                    last_updated=random.randint(1, 1000),
                )
            )
        return user_recomendations


@dataclass
class ModerationQueueGen:
    review_id: str
    user_id: str
    product_id: str
    review_text: str
    rating: int
    moderation_status: str
    flags: list[bool]
    submitted_at: int

    @staticmethod
    def gen_class(user_id : list[str], products_id : list[str]):
        moderation_queue = []
        messages_model = model("Review on product went",
            do_sample=True, top_k=50,
            temperature=0.9, max_length=100, truncation=True)
        review_text = []
        for i in messages_model:
            review_text.append(i["generated_text"])
        for user_id in user_id:
            moderation_queue.append(
                ModerationQueueGen(
                    review_id=str(uuid.uuid4()),
                    user_id=user_id,
                    product_id=random.choice(products_id),
                    review_text=review_text,
                    rating=random.randint(1, 5),
                    moderation_status=random.choice(["done", "on review", "failed"]),
                    flags=[True, False, False],  # i have no clue what it is
                    submitted_at=random.randint(1, 1000),
                )
            )
        return moderation_queue


@dataclass
class SearchQueriesGen:
    query_id: str
    user_id: str
    query_text: str
    timestamp: int
    filters: list[str]
    results_count: int

    @staticmethod
    def gen_class(user_id : list[str], _ : list[str]):
        search_queries = []
        messages_model = model("How to do",
            do_sample=True, top_k=50,
            temperature=0.9, max_length=100, truncation=True)
        query_text = []
        for i in messages_model:
            query_text.append(i["generated_text"])
        for user_id in user_id:
            search_queries.append(
                SearchQueriesGen(
                    query_id=str(uuid.uuid4()),
                    user_id=user_id,
                    query_text=query_text,
                    timestamp=random.randint(1, 1000),
                    filters=random.choices(["date", "attribute", "tier"], k=random.randint(0, 3)),
                    results_count=random.randint(1, 10000),
                )
            )
        return search_queries

gen_mapping = {
    DataBases.UserSessions: UserSessionsGen,
    DataBases.ProductPriceHistory: ProductPriceHistoryGen,
    DataBases.EventLogs: EventLogsGen,
    DataBases.SupportTickets: SupportTicketsGen,
    DataBases.UserRecommendations: UserRecommendationsGen,
    DataBases.ModerationQueue: ModerationQueueGen,
    DataBases.SearchQueries: SearchQueriesGen,
}

def generate_data():
    users_id = generate_id(100)
    products_id = generate_id(10000)
    with MongoClient(MONGO_URL) as connection:
        db = connection[DATABASE]
        for k, v in gen_mapping.items():
            collection = db[k.value]
            gen_data = v.gen_class(users_id, products_id)
            data_as_dict = [asdict(data) for data in gen_data]
            res = collection.insert_many(data_as_dict)
            logging.info(f"For {k} collection {len(res.inserted_ids)} id's were inserted")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_data()
