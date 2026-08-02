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
from pathlib import Path

DATASET_PATH = "dataset"
MEDIA_PATH = Path("dataset/media")
OUTPUT_PATH = "dataset/output.csv"


 
def main():

    print("[INFO] Loading messages...")

    messages = pd.read_csv(
        f"{DATASET_PATH}/messages.csv"
    )
    images = pd.read_csv(
    f"{DATASET_PATH}/images.csv"
    )


    voice_notes = pd.read_csv(
    f"{DATASET_PATH}/voice_notes.csv"
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
    image_reasoner = ImageReasoner()

    audio_reasoner = AudioReasoner()

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

            history["events"],
            message
        )
        media_context = None


        if message["media_type"] == "image":
        
            image_row = images[
                images["image_id"] == message["media_id"]
            ]
        
        
            if not image_row.empty:
            
                image_file = (
                    MEDIA_PATH /
                    image_row.iloc[0]["file_path"]
                )
        
        
                media_context = image_reasoner.analyze(
                    str(image_file)
                )
        
        
        
        elif message["media_type"] == "voice":
        
            voice_row = voice_notes[
                voice_notes["voice_note_id"] == message["media_id"]
            ]
        
        
            if not voice_row.empty:
            
                voice_file = (
                    MEDIA_PATH /
                    voice_row.iloc[0]["file_path"]
                )
        
        
                media_context = audio_reasoner.analyze(
                    str(voice_file)
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