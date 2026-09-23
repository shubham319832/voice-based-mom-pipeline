from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def format_timestamp(seconds):
    """Convert seconds into MM:SS format."""

    seconds = float(seconds)

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    return f"{minutes:02d}:{remaining_seconds:02d}"


def generate_pdf(result, output_file="data/results/meeting_mom.pdf"):
    """
    Generate a professional Minutes of Meeting PDF
    from the pipeline result dictionary.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=6,
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    # ========================================================
    # STORY
    # ========================================================

    story = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "Minutes of Meeting",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Voice-Based Meeting Analysis Report",
            ParagraphStyle(
                "Subtitle",
                parent=body_style,
                alignment=TA_CENTER,
                fontSize=10,
            )
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ========================================================
    # MEETING INFORMATION
    # ========================================================

    language = result.get(
        "language",
        "Unknown"
    )

    language_probability = result.get(
        "language_probability",
        0
    )

    transcript = result.get(
        "transcript",
        []
    )

    speaker_statistics = result.get(
        "speaker_statistics",
        {}
    )

    meeting_analysis = result.get(
        "meeting_analysis",
        {}
    )

    language_table = Table(
        [
            [
                Paragraph(
                    "<b>Detected Language</b>",
                    body_style
                ),
                Paragraph(
                    str(language).upper(),
                    body_style
                ),
            ],
            [
                Paragraph(
                    "<b>Language Probability</b>",
                    body_style
                ),
                Paragraph(
                    f"{language_probability:.2%}",
                    body_style
                ),
            ],
            [
                Paragraph(
                    "<b>Total Transcript Segments</b>",
                    body_style
                ),
                Paragraph(
                    str(len(transcript)),
                    body_style
                ),
            ],
            [
                Paragraph(
                    "<b>Total Speakers</b>",
                    body_style
                ),
                Paragraph(
                    str(len(speaker_statistics)),
                    body_style
                ),
            ],
        ],
        colWidths=[
            65 * mm,
            105 * mm
        ],
    )

    language_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ]
        )
    )

    story.append(
        language_table
    )

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # SPEAKER STATISTICS
    # ========================================================

    story.append(
        Paragraph(
            "1. Speaker Statistics",
            heading_style
        )
    )

    statistics_data = [
        [
            Paragraph("<b>Speaker</b>", small_style),
            Paragraph("<b>Speaking Time</b>", small_style),
            Paragraph("<b>Segments</b>", small_style),
            Paragraph("<b>Speaking %</b>", small_style),
        ]
    ]

    for speaker, stats in speaker_statistics.items():

        statistics_data.append(
            [
                Paragraph(
                    str(speaker),
                    small_style
                ),
                Paragraph(
                    f"{stats.get('speaking_duration_seconds', 0)} sec",
                    small_style
                ),
                Paragraph(
                    str(stats.get('segment_count', 0)),
                    small_style
                ),
                Paragraph(
                    f"{stats.get('speaking_percentage', 0)}%",
                    small_style
                ),
            ]
        )

    statistics_table = Table(
        statistics_data,
        colWidths=[
            50 * mm,
            45 * mm,
            35 * mm,
            40 * mm,
        ],
        repeatRows=1,
    )

    statistics_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
            ]
        )
    )

    story.append(
        statistics_table
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "2. Meeting Summary",
            heading_style
        )
    )

    summary = meeting_analysis.get(
        "summary",
        "No summary available."
    )

    story.append(
        Paragraph(
            str(summary),
            body_style
        )
    )

    # ========================================================
    # KEY DISCUSSION POINTS
    # ========================================================

    story.append(
        Paragraph(
            "3. Key Discussion Points",
            heading_style
        )
    )

    key_points = meeting_analysis.get(
        "key_discussion_points",
        []
    )

    if key_points:

        for point in key_points:

            if isinstance(point, dict):

                text = point.get(
                    "text",
                    ""
                )

                speaker = point.get(
                    "speaker",
                    "UNKNOWN"
                )

                timestamp = point.get(
                    "timestamp",
                    {}
                )

                start = format_timestamp(
                    timestamp.get("start", 0)
                )

                end = format_timestamp(
                    timestamp.get("end", 0)
                )

                story.append(
                    Paragraph(
                        f"• <b>{speaker}</b> "
                        f"[{start} - {end}]: "
                        f"{text}",
                        body_style
                    )
                )

            else:

                story.append(
                    Paragraph(
                        f"• {point}",
                        body_style
                    )
                )

    else:

        story.append(
            Paragraph(
                "No key discussion points detected.",
                body_style
            )
        )

    # ========================================================
    # DECISIONS
    # ========================================================

    story.append(
        Paragraph(
            "4. Decisions",
            heading_style
        )
    )

    decisions = meeting_analysis.get(
        "decisions",
        []
    )

    if decisions:

        for decision in decisions:

            if isinstance(decision, dict):

                text = decision.get(
                    "text",
                    ""
                )

                speaker = decision.get(
                    "speaker",
                    "UNKNOWN"
                )

                timestamp = decision.get(
                    "timestamp",
                    {}
                )

                start = format_timestamp(
                    timestamp.get("start", 0)
                )

                end = format_timestamp(
                    timestamp.get("end", 0)
                )

                story.append(
                    Paragraph(
                        f"• <b>{speaker}</b> "
                        f"[{start} - {end}]: "
                        f"{text}",
                        body_style
                    )
                )

            else:

                story.append(
                    Paragraph(
                        f"• {decision}",
                        body_style
                    )
                )

    else:

        story.append(
            Paragraph(
                "No explicit decisions detected.",
                body_style
            )
        )

    # ========================================================
    # ACTION ITEMS
    # ========================================================

    story.append(
        Paragraph(
            "5. Action Items",
            heading_style
        )
    )

    action_items = meeting_analysis.get(
        "action_items",
        []
    )

    if action_items:

        for action in action_items:

            if isinstance(action, dict):

                text = action.get(
                    "text",
                    ""
                )

                speaker = action.get(
                    "speaker",
                    "UNKNOWN"
                )

                timestamp = action.get(
                    "timestamp",
                    {}
                )

                start = format_timestamp(
                    timestamp.get("start", 0)
                )

                end = format_timestamp(
                    timestamp.get("end", 0)
                )

                story.append(
                    Paragraph(
                        f"• <b>{speaker}</b> "
                        f"[{start} - {end}]: "
                        f"{text}",
                        body_style
                    )
                )

            else:

                story.append(
                    Paragraph(
                        f"• {action}",
                        body_style
                    )
                )

    else:

        story.append(
            Paragraph(
                "No explicit action items detected.",
                body_style
            )
        )

    # ========================================================
    # FULL TRANSCRIPT
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "6. Speaker-Wise Transcript",
            heading_style
        )
    )

    transcript_data = [
        [
            Paragraph("<b>Time</b>", small_style),
            Paragraph("<b>Speaker</b>", small_style),
            Paragraph("<b>Transcript</b>", small_style),
            Paragraph("<b>Log Probability</b>", small_style),
        ]
    ]

    for item in transcript:

        start = format_timestamp(
            item.get("start", 0)
        )

        end = format_timestamp(
            item.get("end", 0)
        )

        speaker = item.get(
            "speaker",
            "UNKNOWN"
        )

        text = item.get(
            "text",
            ""
        )

        confidence = item.get(
            "confidence",
            "N/A"
        )

        transcript_data.append(
            [
                Paragraph(
                    f"{start} - {end}",
                    small_style
                ),
                Paragraph(
                    str(speaker),
                    small_style
                ),
                Paragraph(
                    str(text),
                    small_style
                ),
                Paragraph(
                    str(confidence),
                    small_style
                ),
            ]
        )

    transcript_table = Table(
        transcript_data,
        colWidths=[
            30 * mm,
            32 * mm,
            93 * mm,
            25 * mm,
        ],
        repeatRows=1,
    )

    transcript_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
            ]
        )
    )

    story.append(
        transcript_table
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )

    print(
        f"\nPDF generated successfully: "
        f"{output_path}"
    )

    return output_path


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import json

    result_file = Path(
        "data/results/meeting_result.json"
    )

    if not result_file.exists():

        raise FileNotFoundError(
            "meeting_result.json was not found. "
            "Run the meeting pipeline first."
        )

    with open(
        result_file,
        "r",
        encoding="utf-8"
    ) as file:

        result = json.load(file)

    generate_pdf(
        result
    )