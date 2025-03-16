from enum import Enum
from transformers import pipeline

MONGO_URL = "mongodb://root:123456@www.vcrostin.space:27017"

DATABASE = "database"
DEVICES = ""


class DataBases(Enum):
    UserSessions = "user_sessions"
    ProductPriceHistory = "product_price_history"
    EventLogs = "event_logs"
    SupportTickets = "support_tickets"
    UserRecommendations = "user_recommendations"
    ModerationQueue = "moderation_queue"
    SearchQueries = "search_queries"


model = pipeline("text-generation", model = "gpt2")