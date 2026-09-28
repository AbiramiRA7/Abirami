import base64
import json
from typing import Any

from google import genai

from ..config import get_settings
from ..utils.prompts import SYSTEM_PROMPT, build_prompt
from ..utils.helpers import total_cost
from .marketplace_service import PLATFORMS, search_url
from .fallback_service import (
    home_fallback,
    party_fallback,
    jewelry_fallback,
)


class GeminiService:
    def __init__(self):
        self.settings = get_settings()

        self.client = (
            genai.Client(api_key=self.settings.gemini_api_key)
            if self.settings.gemini_api_key
            else None
        )

    def generate(
        self,
        planner: str,
        data: Any,
        image_bytes: bytes | None = None,
        mime_type: str | None = None,
    ):
        """
        Generate AI recommendations using Gemini.

        Supports:
        - Home planner: text input
        - Party planner: text input
        - Jewelry planner: text input + optional image

        If Gemini fails for any reason, the local fallback
        recommendation engine is used.
        """

        fallback_map = {
            "home": home_fallback,
            "party": party_fallback,
            "jewelry": jewelry_fallback,
        }

        # Safety check for unsupported planner types.
        if planner not in fallback_map:
            raise ValueError(f"Unsupported planner: {planner}")

        # Generate fallback recommendations first.
        fallback = fallback_map[planner](data)

        # ---------------------------------------------------------
        # GEMINI NOT CONFIGURED
        # ---------------------------------------------------------
        if not self.client:
            return self.package(
                planner=planner,
                data=data,
                recs=fallback,
                source="fallback",
                summary=(
                    "Gemini is not configured; "
                    "using the local fallback engine."
                ),
            )

        # ---------------------------------------------------------
        # BUILD PROMPT
        # ---------------------------------------------------------
        prompt = build_prompt(
            planner,
            data.model_dump(),
            PLATFORMS[planner],
        )

        # ---------------------------------------------------------
        # BUILD GEMINI INPUT
        # ---------------------------------------------------------
        #
        # For text-only requests:
        #
        #     input="some text"
        #
        # For multimodal requests:
        #
        #     input=[
        #         {"type": "text", ...},
        #         {"type": "image", ...}
        #     ]
        #
        # This matches the current Interactions API format.
        # ---------------------------------------------------------

        if image_bytes and mime_type:
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            gemini_input = [
                {
                    "type": "text",
                    "text": (
                        prompt
                        + "\n\n"
                        + "Use the uploaded outfit image only for "
                        "color, formality, and style coordination. "
                        "Do not identify the person."
                    ),
                },
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": mime_type,
                },
            ]

        else:
            gemini_input = prompt

        # ---------------------------------------------------------
        # CALL GEMINI
        # ---------------------------------------------------------
        try:
            interaction = self.client.interactions.create(
                model=self.settings.gemini_model,
                system_instruction=SYSTEM_PROMPT,
                input=gemini_input,
            )

            # Current Interactions API convenience property.
            raw_text = interaction.output_text

            if not raw_text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            # -----------------------------------------------------
            # PARSE JSON
            # -----------------------------------------------------
            raw = self.parse_json_response(raw_text)

            # -----------------------------------------------------
            # BUILD RECOMMENDATIONS
            # -----------------------------------------------------
            recs = []

            recommendations = raw.get(
                "recommendations",
                [],
            )

            if not isinstance(recommendations, list):
                raise ValueError(
                    "Gemini recommendations field is not a list."
                )

            for item in recommendations:
                if not isinstance(item, dict):
                    continue

                # ---------------------------------------------
                # PLATFORM
                # ---------------------------------------------
                platform = item.get("platform")

                if platform not in PLATFORMS[planner]:
                    platform = PLATFORMS[planner][0]

                # ---------------------------------------------
                # TITLE
                # ---------------------------------------------
                title = str(
                    item.get(
                        "title",
                        "Recommended option",
                    )
                ).strip()

                if not title:
                    title = "Recommended option"

                # ---------------------------------------------
                # PRICE
                # ---------------------------------------------
                try:
                    estimated_price = float(
                        item.get(
                            "estimated_price",
                            0,
                        )
                    )
                except (TypeError, ValueError):
                    estimated_price = 0.0

                estimated_price = max(
                    0.0,
                    estimated_price,
                )

                # ---------------------------------------------
                # QUANTITY
                # ---------------------------------------------
                try:
                    quantity = int(
                        item.get(
                            "quantity",
                            1,
                        )
                    )
                except (TypeError, ValueError):
                    quantity = 1

                quantity = max(
                    1,
                    quantity,
                )

                # ---------------------------------------------
                # CATEGORY
                # ---------------------------------------------
                category = str(
                    item.get(
                        "category",
                        "General",
                    )
                ).strip()

                if not category:
                    category = "General"

                # ---------------------------------------------
                # RATIONALE
                # ---------------------------------------------
                rationale = str(
                    item.get(
                        "rationale",
                        "Budget-aware suggestion.",
                    )
                ).strip()

                if not rationale:
                    rationale = "Budget-aware suggestion."

                # ---------------------------------------------
                # MARKETPLACE SEARCH URL
                # ---------------------------------------------
                marketplace_url = search_url(
                    platform,
                    title,
                    getattr(
                        data,
                        "city",
                        "",
                    ),
                )

                # ---------------------------------------------
                # FINAL RECOMMENDATION
                # ---------------------------------------------
                recs.append(
                    {
                        "category": category,
                        "title": title,
                        "platform": platform,
                        "estimated_price": estimated_price,
                        "quantity": quantity,
                        "rationale": rationale,
                        "search_url": marketplace_url,
                    }
                )

            # Gemini didn't give usable recommendations.
            if not recs:
                raise ValueError(
                    "Gemini returned no usable recommendations."
                )

            # -----------------------------------------------------
            # SUCCESS
            # -----------------------------------------------------
            return self.package(
                planner=planner,
                data=data,
                recs=recs,
                source="gemini",
                summary=str(
                    raw.get(
                        "summary",
                        "Gemini-generated recommendations.",
                    )
                ),
                allocations=raw.get(
                    "allocations",
                    {},
                ),
            )

        # ---------------------------------------------------------
        # GEMINI FAILED → FALLBACK
        # ---------------------------------------------------------
        except Exception as exc:
            print(
                "\n"
                "[GeminiService] Gemini request failed\n"
                f"Type: {type(exc).__name__}\n"
                f"Error: {exc}\n"
            )

            return self.package(
                planner=planner,
                data=data,
                recs=fallback,
                source="fallback",
                summary=(
                    "Gemini was unavailable or returned "
                    "invalid output; using fallback "
                    "recommendations."
                ),
            )

    # =============================================================
    # JSON PARSER
    # =============================================================

    @staticmethod
    def parse_json_response(raw_text: str) -> dict:
        """
        Parse Gemini's JSON response.

        Handles:
        1. Normal JSON
        2. Markdown ```json ... ``` responses
        """

        text = raw_text.strip()

        # Remove markdown code fences if Gemini returned them.
        if text.startswith("```"):
            lines = text.splitlines()

            # Remove first line: ```json
            if lines:
                lines = lines[1:]

            # Remove final ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini returned invalid JSON: {exc}"
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                "Gemini JSON response must be an object."
            )

        return parsed

    # =============================================================
    # PACKAGE RESULT
    # =============================================================

    def package(
        self,
        planner,
        data,
        recs,
        source,
        summary,
        allocations=None,
    ):
        """
        Convert Gemini/fallback recommendations into
        the response structure expected by the rest
        of PocketSmart AI.
        """

        budget = float(data.budget)

        total = total_cost(recs)

        return {
            "planner": planner,
            "budget": budget,
            "total_estimate": total,
            "budget_remaining": round(
                budget - total,
                2,
            ),
            "source": source,
            "summary": summary,
            "allocations": allocations or {},
            "recommendations": recs,
        }