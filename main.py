import pandas as pd
from src.ai.image_reasoner import ImageReasoner
from src.ai.audio_reasoner import AudioReasoner
from src.preprocessing.audio_preprocessor import AudioPreprocessor

from src.retrieval.context_builder import ContextBuilder
from src.retrieval.conversation_retriever import ConversationRetriever
from src.retrieval.ranking import EvidenceRanker

from src.ai.notification_engine import NotificationEngine
from src.ai.confidence import ConfidenceEngine
from src.ai.llm_router import LLMRouter

from src.output.output_generator import OutputGenerator


DATASET_PATH = "dataset"

OUTPUT_PATH = "dataset/output.csv"


image_reasoner = ImageReasoner()

audio_reasoner = AudioReasoner()

audio_processor = AudioPreprocessor()
def main():

    print("[INFO] Loading messages...")

    messages = pd.read_csv(
        f"{DATASET_PATH}/messages.csv"
    )


    print("[INFO] Initializing components...")


    context_builder = ContextBuilder(
        DATASET_PATH
    )


    retriever = ConversationRetriever(
        DATASET_PATH
    )


    ranker = EvidenceRanker(
        top_k=5
    )


    router = LLMRouter(
        NotificationEngine(),
        ConfidenceEngine()
    )


    output = OutputGenerator(
        OUTPUT_PATH
    )


    print(
        f"[INFO] Processing {len(messages)} messages"
    )


    for index, message in messages.iterrows():


        # Build user context

        context = context_builder.build_context(

            user_id=message["user_id"],

            group_id=message["group_id"],

            business_id=message["business_id"]

        )


        # Retrieve historical messages

        history = retriever.retrieve(
            message
        )


        # Select evidence

        evidence_ids = ranker.rank(

            history["user_history"],

            history["events"]

        )
        media_context = None


        if message["media_type"] == "image":
        
            image_path = None

            media_context = image_reasoner.analyze(
                image_path
            )


        elif message["media_type"] == "voice":
        
            voice_path = None

            audio_info = None

            media_context = audio_reasoner.analyze(
                voice_path,
                audio_info
            )
        
        # AI decision

        result = router.predict(
            message,
            context,
            evidence_ids,
            media_context
        )

        # Save result

        output.add_result(

            message_id=message["message_id"],

            action=result["action"],

            message_type=result["message_type"],

            reason=result["reason"],

            confidence=result["confidence"],

            evidence_message_ids=
            result["evidence_message_ids"]

        )


        if index % 100 == 0:
            print(
                f"Processed {index} messages"
            )


    output.save()


    print("[INFO] Completed successfully")



if __name__ == "__main__":

    main()