import streamlit as st
import plotly.express as px
from pathlib import Path

from src.meeting_pipeline import process_meeting


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Voice-Based Minutes of Meeting",
    page_icon="🎙️",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🎙️ Voice-Based Minutes of Meeting")

st.write(
    "Upload a meeting recording to generate a structured transcript, "
    "speaker statistics, speaker timeline, and meeting analysis."
)

st.divider()


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload Meeting Audio / Video",
    type=[
        "mp4",
        "wav",
        "mp3",
        "m4a",
        "webm"
    ]
)


# ============================================================
# PROCESS UPLOADED FILE
# ============================================================

if uploaded_file is not None:

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )

    file_size_mb = uploaded_file.size / (1024 * 1024)

    st.write(
        f"File size: {file_size_mb:.2f} MB"
    )

    # --------------------------------------------------------
    # PROCESS BUTTON
    # --------------------------------------------------------

    if st.button("🚀 Process Meeting"):

        upload_directory = Path(
            "data/uploads"
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        input_path = (
            upload_directory /
            uploaded_file.name
        )

        # Save uploaded file
        with open(
            input_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        st.success(
            "Meeting file saved successfully."
        )

        # ----------------------------------------------------
        # RUN PIPELINE
        # ----------------------------------------------------

        try:

            with st.spinner(
                "Processing meeting... This may take some time."
            ):

                result = process_meeting(
                    input_file=input_path
                )

            st.success(
                "🎉 Meeting processing completed!"
            )

            # =================================================
            # LANGUAGE
            # =================================================

            st.subheader(
                "🌐 Detected Language"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Language",
                    result["language"]
                )

            with col2:

                st.metric(
                    "Language Confidence",
                    f"{result['language_probability']:.2%}"
                )


            # =================================================
            # SPEAKER STATISTICS
            # =================================================

            st.subheader(
                "👥 Speaker Statistics"
            )

            for (
                speaker,
                statistics
            ) in result[
                "speaker_statistics"
            ].items():

                with st.expander(
                    speaker,
                    expanded=True
                ):

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Speaking Time",
                            f"{statistics['speaking_duration_seconds']} sec"
                        )

                    with col2:

                        st.metric(
                            "Segments",
                            statistics["segment_count"]
                        )

                    with col3:

                        st.metric(
                            "Speaking %",
                            f"{statistics['speaking_percentage']}%"
                        )


            # =================================================
            # SPEAKER TIMELINE
            # =================================================

            st.subheader(
                "📊 Speaker Timeline"
            )

            timeline_data = []

            for item in result["transcript"]:

                timeline_data.append(
                    {
                        "Speaker": item["speaker"],
                        "Start": item["start"],
                        "End": item["end"],
                        "Duration": round(
                            item["end"] - item["start"],
                            2
                        )
                    }
                )


            if timeline_data:

                fig = px.timeline(
                    timeline_data,
                    x_start="Start",
                    x_end="End",
                    y="Speaker",
                    color="Speaker",
                    hover_data=[
                        "Duration"
                    ],
                    title="Speaker Activity Timeline"
                )

                fig.update_yaxes(
                    autorange="reversed"
                )

                fig.update_xaxes(
                    title="Time (seconds)"
                )

                fig.update_layout(
                    height=400
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No timeline data available."
                )


            # =================================================
            # SPEAKER-WISE TRANSCRIPT
            # =================================================

            st.subheader(
                "📝 Speaker-Wise Transcript"
            )

            for item in result["transcript"]:

                st.write(
                    f"**[{item['start']:.2f}s - "
                    f"{item['end']:.2f}s] "
                    f"{item['speaker']}**"
                )

                st.write(
                    item["text"]
                )

                # ---------------------------------------------
                # TRANSCRIPTION LOG PROBABILITY
                # ---------------------------------------------

                if "confidence" in item:

                    st.caption(
                        f"Transcription log probability: "
                        f"{item['confidence']}"
                    )

                st.divider()


            # =================================================
            # MEETING ANALYSIS
            # =================================================

            analysis = result[
                "meeting_analysis"
            ]


            # =================================================
            # SUMMARY
            # =================================================

            st.subheader(
                "📋 Meeting Summary"
            )

            st.write(
                analysis["summary"]
            )


            # =================================================
            # KEY DISCUSSION POINTS
            # =================================================

            st.subheader(
                "💡 Key Discussion Points"
            )

            if analysis[
                "key_discussion_points"
            ]:

                for point in analysis[
                    "key_discussion_points"
                ]:

                    st.write(
                        f"- {point}"
                    )

            else:

                st.info(
                    "No key discussion points detected."
                )


            # =================================================
            # DECISIONS
            # =================================================

            st.subheader(
                "✅ Decisions"
            )

            if analysis[
                "decisions"
            ]:

                for decision in analysis[
                    "decisions"
                ]:

                    st.write(
                        f"- {decision}"
                    )

            else:

                st.info(
                    "No explicit decisions detected."
                )


            # =================================================
            # ACTION ITEMS
            # =================================================

            st.subheader(
                "📌 Action Items"
            )

            if analysis[
                "action_items"
            ]:

                for action in analysis[
                    "action_items"
                ]:

                    st.write(
                        f"- **{action['speaker']}**: "
                        f"{action['text']}"
                    )

            else:

                st.info(
                    "No explicit action items detected."
                )


            # =================================================
            # DOWNLOAD JSON RESULT
            # =================================================

            result_file = Path(
                result["result_file"]
            )

            if result_file.exists():

                st.subheader(
                    "💾 Download Result"
                )

                with open(
                    result_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download JSON Result",
                        data=file,
                        file_name="meeting_result.json",
                        mime="application/json"
                    )


        # =====================================================
        # ERROR HANDLING
        # =====================================================

        except Exception as error:

            st.error(
                "An error occurred while processing the meeting."
            )

            st.exception(
                error
            )