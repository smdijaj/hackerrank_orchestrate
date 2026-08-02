from src.ai.llm_router import LLMRouter
from src.ai.notification_engine import NotificationEngine
from src.ai.confidence import ConfidenceEngine


router = LLMRouter(
    NotificationEngine(),
    ConfidenceEngine()
)


message = {
    "message_text":
    "Your OTP is 123456. Do not share",
    "conversation_type":
    "personal",
    "media_type":""
}


context = {
    "user":{
        "notifications_dismissed_30d":5
    }
}


result = router.predict(
    message,
    context,
    ["msg_10","msg_20"]
)


print(result)