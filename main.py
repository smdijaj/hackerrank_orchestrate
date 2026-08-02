import pandas as pd

from src.ai.image_reasoner import ImageReasoner
from src.ai.audio_reasoner import AudioReasoner

from src.retrieval.context_builder import ContextBuilder
from src.retrieval.conversation_retriever import ConversationRetriever
from src.retrieval.ranking import EvidenceRanker

from src.ai.notification_engine import NotificationEngine
from src.ai.confidence import ConfidenceEngine
from src.ai.llm_router import LLMRouter

from src.output.output_generator import OutputGenerator


DATASET_PATH = "dataset"

OUTPUT_PATH = "dataset/output.csv"



def main():

    print("[INFO] Loading datasets...")


    messages = pd.read_csv(
        f"{DATASET_PATH}/messages.csv"
    )


    images = pd.read_csv(
        f"{DATASET_PATH}/images.csv"
    )


    try:

        audio_files = pd.read_csv(
            f"{DATASET_PATH}/audio.csv"
        )

    except:

        audio_files = pd.DataFrame()



    print("[INFO] Initializing AI components...")


    image_reasoner = ImageReasoner()

    audio_reasoner = AudioReasoner()



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


        # -------------------------
        # Build context
        # -------------------------

        context = context_builder.build_context(

            user_id=message["user_id"],

            group_id=message["group_id"],

            business_id=message["business_id"]

        )



        # -------------------------
        # Retrieve evidence
        # -------------------------

        history = retriever.retrieve(
            message
        )


        evidence_ids = ranker.rank(

            history["user_history"],

            history["events"]

        )



        # -------------------------
        # MEDIA PROCESSING
        # -------------------------

        media_context = None



        # IMAGE

        if message["media_type"] == "image":


            image_row = images[

                images["image_id"]
                ==
                message["media_id"]

            ]


            if not image_row.empty:


                image_path = (

                    DATASET_PATH
                    +
                    "/"
                    +
                    image_row.iloc[0]["file_path"]

                )


                media_context = image_reasoner.analyze(

                    image_path

                )


                print(
                    "IMAGE:",
                    message["message_id"],
                    media_context
                )



        # AUDIO

        elif message["media_type"] == "voice":


            audio_path = None

            audio_info = None


            if not audio_files.empty:


                audio_row = audio_files[

                    audio_files["audio_id"]
                    ==
                    message["media_id"]

                ]


                if not audio_row.empty:


                    audio_path = (

                        DATASET_PATH
                        +
                        "/"
                        +
                        audio_row.iloc[0]["file_path"]

                    )


                    audio_info = (
                        audio_row.iloc[0]
                        .to_dict()
                    )



            media_context = audio_reasoner.analyze(

                audio_path,

                audio_info

            )


            print(
                "AUDIO:",
                message["message_id"],
                media_context
            )



        # -------------------------
        # AI ROUTING
        # -------------------------

        result = router.predict(

            message,

            context,

            evidence_ids,

            media_context

        )



        # -------------------------
        # SAVE OUTPUT
        # -------------------------

        output.add_result(

            message_id=message["message_id"],

            action=result["action"],

            message_type=result["message_type"],

            reason=result["reason"],

            confidence=result["confidence"],

            evidence_message_ids=
            result["evidence_message_ids"]

        )



        if index % 20 == 0:

            print(
                f"Processed {index} messages"
            )



    output.save()


    print(
        "[INFO] Completed successfully"
    )




if __name__ == "__main__":

    main()