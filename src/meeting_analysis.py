import re


def clean_text(text):
    return " ".join(text.strip().split())


def normalize_text(text):
    return text.lower().strip()


def create_summary(aligned_segments, max_sentences=5):
    sentences = []

    for segment in aligned_segments:
        text = clean_text(segment["text"])

        if not text:
            continue

        if text not in sentences:
            sentences.append(text)

        if len(sentences) >= max_sentences:
            break

    return " ".join(sentences)


def extract_key_points(aligned_segments):
    keywords = [
        "discuss",
        "discussion",
        "topic",
        "plan",
        "project",
        "level",
        "ai",
        "machine learning",
        "deadline",
        "requirement",
        "issue",
        "problem",
        "training",
        "course",
    ]

    key_points = []

    for segment in aligned_segments:
        text = clean_text(segment["text"])
        normalized = normalize_text(text)

        if any(keyword in normalized for keyword in keywords):
            key_points.append({
                "speaker": segment["speaker"],
                "timestamp": {
                    "start": segment["start"],
                    "end": segment["end"]
                },
                "text": text
            })

    return key_points[:10]


def extract_decisions(aligned_segments):
    decision_patterns = [
        r"\bfinal decision\b",
        r"\bwe decided\b",
        r"\bthe decision is\b",
        r"\bit was decided\b",
        r"\bagreed that\b",
        r"\bagreed to\b",
        r"\bwe agreed\b",
        r"\bwe chose\b",
        r"\bwe selected\b",
        r"\bapproved\b",
        r"\bconfirmed\b",
    ]

    decisions = []

    for segment in aligned_segments:
        text = clean_text(segment["text"])
        normalized = normalize_text(text)

        if any(re.search(pattern, normalized) for pattern in decision_patterns):
            decisions.append({
                "speaker": segment["speaker"],
                "timestamp": {
                    "start": segment["start"],
                    "end": segment["end"]
                },
                "text": text
            })

    return decisions[:10]


def extract_action_items(aligned_segments):
    action_patterns = [
        r"\baction item\b",
        r"\bnext step\b",
        r"\bneed to\b",
        r"\bmust\b",
        r"\bshould\b",
        r"\bwill prepare\b",
        r"\bwill complete\b",
        r"\bwill finish\b",
        r"\bwill send\b",
        r"\bwill create\b",
        r"\bwill update\b",
        r"\bwill review\b",
        r"\bwill check\b",
        r"\bwill implement\b",
    ]

    action_items = []

    for segment in aligned_segments:
        text = clean_text(segment["text"])
        normalized = normalize_text(text)

        if any(re.search(pattern, normalized) for pattern in action_patterns):
            action_items.append({
                "speaker": segment["speaker"],
                "timestamp": {
                    "start": segment["start"],
                    "end": segment["end"]
                },
                "text": text
            })

    return action_items[:10]


def analyze_meeting(aligned_segments):
    return {
        "summary": create_summary(aligned_segments),
        "key_discussion_points": extract_key_points(aligned_segments),
        "decisions": extract_decisions(aligned_segments),
        "action_items": extract_action_items(aligned_segments)
    }


if __name__ == "__main__":
    test_segments = [
        {
            "start": 0.0,
            "end": 5.0,
            "speaker": "SPEAKER_00",
            "text": "We discussed the project requirements."
        },
        {
            "start": 5.0,
            "end": 10.0,
            "speaker": "SPEAKER_01",
            "text": "We agreed to complete the project by Friday."
        },
        {
            "start": 10.0,
            "end": 15.0,
            "speaker": "SPEAKER_00",
            "text": "I will prepare the documentation."
        }
    ]

    result = analyze_meeting(test_segments)

    print("\n==============================")
    print("MEETING ANALYSIS TEST")
    print("==============================")

    print("\nSummary:")
    print(result["summary"])

    print("\nKey Discussion Points:")
    for item in result["key_discussion_points"]:
        print(item)

    print("\nDecisions:")
    for item in result["decisions"]:
        print(item)

    print("\nAction Items:")
    for item in result["action_items"]:
        print(item)