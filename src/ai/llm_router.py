class LLMRouter:
    """
    Builds reasoning input and manages AI decision flow.
    """

    def __init__(
        self,
        notification_engine,
        confidence_engine
    ):

        self.notification_engine = notification_engine
        self.confidence_engine = confidence_engine


    def build_prompt(
        self,
        message,
        context,
        evidence_ids,
        media_context=None
    ):
        """
        Prepare structured reasoning information.
        """

        prompt = {

            "message": {
                "text": message.get(
                    "message_text",
                    ""
                ),

                "type":
                message.get(
                    "conversation_type"
                ),

                "media":
                message.get(
                    "media_type"
                )
            },


            "user_context":
            context.get(
                "user"
            ),


            "group_context":
            context.get(
                "group"
            ),


            "business_context":
            context.get(
                "business"
            ),


            "history_evidence":
            evidence_ids,


            "media_analysis":
            media_context

        }


        return prompt



    def predict(
        self,
        message,
        context,
        evidence_ids=None,
        media_context=None
    ):
        """
        Complete routing pipeline.
        """


        # Prepare reasoning input
        reasoning_input = self.build_prompt(
            message,
            context,
            evidence_ids,
            media_context
        )


        # Decision engine
        result = self.notification_engine.route(
            message,
            context,
            media_context,
            evidence_ids
        )


        # Confidence
        confidence = self.confidence_engine.calculate(
            action=result["action"],
            message_type=result["message_type"],
            context=context,
            evidence_ids=evidence_ids
        )


        result["confidence"] = confidence


        result["evidence_message_ids"] = (
            ";".join(evidence_ids)
            if evidence_ids
            else "none"
        )


        result["reasoning_input"] = reasoning_input


        return result