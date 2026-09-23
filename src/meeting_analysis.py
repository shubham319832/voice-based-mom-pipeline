import re


# ============================================================
# TEXT UTILITIES
# ============================================================

def clean_text(text):
    """
    Clean unnecessary whitespace from transcript text.
    """

    if not text:
        return ""

    return " ".join(text.split())


def normalize_text(text):
    """
    Convert text to lowercase for matching.
    """

    return clean_text(text).lower()


# ============================================================
# SUMMARY
# ============================================================

def create_summary(transcript):
    """
    Create a simple extractive summary.

    The function selects the first meaningful sentences
    from the meeting transcript.
    """

    if not transcript:
        return "No transcript available."

    sentences = []

    for segment in transcript:

        text = clean_text(segment.get("text", ""))

        if not text:
            continue

        # Split long transcript segments into sentences
        parts = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        for part in parts:

            part = clean_text(part)

            if len(part) >= 10:
                sentences.append(part)

    if not sentences:
        return "No meaningful transcript content available."

    # Remove duplicates while preserving order
    unique_sentences = []

    seen = set()

    for sentence in sentences:

        key = sentence.lower()

        if key not in seen:

            seen.add(key)
            unique_sentences.append(sentence)

    # Keep the first 5 meaningful sentences
    summary_sentences = unique_sentences[:5]

    return " ".join(summary_sentences)


# ============================================================
# KEY DISCUSSION POINTS
# ============================================================

def extract_key_points(transcript):
    """
    Extract likely discussion points using keywords.
    """

    key_points = []

    keywords = [
        "discuss",
        "discussed",
        "discussion",
        "topic",
        "important",
        "focus",
        "cover",
        "covered",
        "learn",
        "learning",
        "explain",
        "explained",
        "plan",
        "planned",
        "project",
        "problem",
        "issue",
        "challenge",
        "solution",
        "level",
        "process"
    ]

    seen = set()

    for segment in transcript:

        text = clean_text(
            segment.get("text", "")
        )

        if not text:
            continue

        normalized = normalize_text(text)

        matched = any(
            keyword in normalized
            for keyword in keywords
        )

        if matched:

            key = normalized

            if key not in seen:

                seen.add(key)

                key_points.append({
                    "speaker": segment.get(
                        "speaker",
                        "UNKNOWN"
                    ),
                    "timestamp": {
                        "start": segment.get(
                            "start",
                            0
                        ),
                        "end": segment.get(
                            "end",
                            0
                        )
                    },
                    "text": text
                })

    return key_points[:10]


# ============================================================
# DECISIONS
# ============================================================

def extract_decisions(transcript):
    """
    Extract sentences that appear to contain decisions.
    """

    decisions = []

    decision_patterns = [
        r"\bwe decided\b",
        r"\bdecided to\b",
        r"\bwe have decided\b",
        r"\bwe will\b",
        r"\bwe are going to\b",
        r"\bagreed to\b",
        r"\bwe agreed\b",
        r"\bthe decision is\b",
        r"\bthe decision was\b",
        r"\bfinal decision\b",
        r"\bwe chose\b",
        r"\bwe selected\b"
    ]

    seen = set()

    for segment in transcript:

        text = clean_text(
            segment.get("text", "")
        )

        if not text:
            continue

        normalized = normalize_text(text)

        matched = False

        for pattern in decision_patterns:

            if re.search(
                pattern,
                normalized
            ):

                matched = True
                break

        if matched:

            key = normalized

            if key not in seen:

                seen.add(key)

                decisions.append({
                    "speaker": segment.get(
                        "speaker",
                        "UNKNOWN"
                    ),
                    "timestamp": {
                        "start": segment.get(
                            "start",
                            0
                        ),
                        "end": segment.get(
                            "end",
                            0
                        )
                    },
                    "text": text
                })

    return decisions[:10]


# ============================================================
# ACTION ITEMS
# ============================================================

def extract_action_items(transcript):
    """
    Extract likely action items.

    Action items are identified using phrases such as:
    - need to
    - should
    - must
    - next step
    - action item
    - will prepare
    - will complete
    - will send
    """

    action_items = []

    action_patterns = [
        r"\bneed to\b",
        r"\bneeds to\b",
        r"\bshould\b",
        r"\bmust\b",
        r"\baction item\b",
        r"\bnext step\b",
        r"\bto do\b",
        r"\bwill prepare\b",
        r"\bwill complete\b",
        r"\bwill finish\b",
        r"\bwill send\b",
        r"\bwill create\b",
        r"\bwill update\b",
        r"\bwill review\b",
        r"\bwill check\b",
        r"\bwill implement\b",
        r"\bprepare\b",
        r"\bcomplete\b",
        r"\bfinish\b",
        r"\bsend\b",
        r"\bcreate\b",
        r"\bupdate\b",
        r"\breview\b",
        r"\bcheck\b",
        r"\bimplement\b"
    ]

    seen = set()

    for segment in transcript:

        text = clean_text(
            segment.get("text", "")
        )

        if not text:
            continue

        normalized = normalize_text(text)

        matched = False

        for pattern in action_patterns:

            if re.search(
                pattern,
                normalized
            ):

                matched = True
                break

        if matched:

            key = normalized

            if key not in seen:

                seen.add(key)

                action_items.append({
                    "speaker": segment.get(
                        "speaker",
                        "UNKNOWN"
                    ),
                    "timestamp": {
                        "start": segment.get(
                            "start",
                            0
                        ),
                        "end": segment.get(
                            "end",
                            0
                        )
                    },
                    "text": text
                })

    return action_items[:10]


# ============================================================
# COMPLETE MEETING ANALYSIS
# ============================================================

def analyze_meeting(transcript):
    """
    Perform complete local meeting analysis.
    """

    if not transcript:

        return {
            "summary": "No transcript available.",
            "key_discussion_points": [],
            "decisions": [],
            "action_items": []
        }

    result = {
        "summary": create_summary(
            transcript
        ),
        "key_discussion_points": extract_key_points(
            transcript
        ),
        "decisions": extract_decisions(
            transcript
        ),
        "action_items": extract_action_items(
            transcript
        )
    }

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_transcript = [

        {
            "start": 0.0,
            "end": 5.0,
            "speaker": "SPEAKER_00",
            "text": "Today we will discuss the AI project."
        },

        {
            "start": 5.0,
            "end": 10.0,
            "speaker": "SPEAKER_01",
            "text": "We decided to complete the project this week."
        },

        {
            "start": 10.0,
            "end": 15.0,
            "speaker": "SPEAKER_00",
            "text": "The team will prepare the final documentation."
        },

        {
            "start": 15.0,
            "end": 20.0,
            "speaker": "SPEAKER_01",
            "text": "The next step is to review the implementation."
        }
    ]

    result = analyze_meeting(
        test_transcript
    )

    print("\n================================")
    print("MEETING ANALYSIS TEST")
    print("================================")

    print("\nSUMMARY:")
    print(
        result["summary"]
    )

    print("\nKEY DISCUSSION POINTS:")

    for point in result[
        "key_discussion_points"
    ]:

        print(
            f"- {point['speaker']}: "
            f"{point['text']}"
        )

    print("\nDECISIONS:")

    for decision in result[
        "decisions"
    ]:

        print(
            f"- {decision['speaker']}: "
            f"{decision['text']}"
        )

    print("\nACTION ITEMS:")

    for action in result[
        "action_items"
    ]:

        print(
            f"- {action['speaker']}: "
            f"{action['text']}"
        )

    print(
        "\n================================"
    )

    print(
        "MEETING ANALYSIS TEST COMPLETE"
    )

    print(
        "================================"
    )