import html
import streamlit as st

from story_engine import generate_story

DEFAULT_MAX_ITERATIONS = 3
PRESET_TONES = [
    "Warm bedtime",
    "Playful",
    "Gentle humor",
    "Calm & cozy",
]
CUSTOM_TONE_OPTION = "Custom"
TWEAK_HINTS = {
    "Cozy bedtime vibe": "Layer in extra bedtime imagery—warm blankets, hushed voices, sleepy yawns.",
    "More sensory detail": "Describe gentle sounds, scents, and textures so the world feels vivid but calm.",
    "Friendly dialogue": "Add a few short lines of dialogue between the characters to show their bond.",
    "Clearer lesson": "Highlight the gentle feeling or takeaway the characters bring home at the end.",
}
CUSTOM_FEEDBACK_OPTION = "Custom change"
FEEDBACK_CHOICES = list(TWEAK_HINTS.keys()) + [CUSTOM_FEEDBACK_OPTION]

st.set_page_config(page_title="Bedtime Story Studio", page_icon="🌙", layout="wide")

CUSTOM_CSS = """
<style>
body {
    background: radial-gradient(circle at 0% 0%, rgba(255,255,255,0.92), #f6f7fb 65%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #1f2937;
}
.block-container {
    padding: 0 2rem 3rem 2rem;
}
.card {
    background: #fff;
    border-radius: 14px;
    padding: 1.5rem;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 24px rgba(17,24,39,0.05);
}
.setup-pane {
    position: sticky;
    top: 1rem;
}
.story-reader {
    font-family: 'Source Serif Pro', Georgia, 'Times New Roman', serif;
    font-size: 1.1rem;
    line-height: 1.75;
    max-width: 62ch;
    margin: 0 auto 1.25rem auto;
}
.story-reader p {
    margin-bottom: 1rem;
}
.story-meta {
    color: #6b7280;
    font-size: 0.92rem;
}
.story-status {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #eef2ff;
    color: #4338ca;
    border-radius: 999px;
    padding: 0.1rem 0.75rem;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}
.skeleton {
    background: #f5f7ff;
    border-radius: 16px;
    padding: 1.5rem;
    animation: pulse 1.5s ease infinite;
}
@keyframes pulse {
  0% { opacity: 0.9; }
  50% { opacity: 0.5; }
  100% { opacity: 0.9; }
}
textarea, input, .stNumberInput input {
    border-radius: 10px !important;
    border: 1.5px solid #d6d9f5;
}
textarea:focus-visible, input:focus-visible {
    outline: 2px solid #6b5bff !important;
    outline-offset: 2px;
}
.stNumberInput button {
    padding: 0.3rem 0.65rem;
    border-radius: 10px !important;
    background: transparent;
    color: #7c3aed;
    border: 1px solid #7c3aed;
}
.stNumberInput button:hover {
    background: rgba(124,58,237,0.12) !important;
    color: #4f46e5 !important;
    border-color: #4f46e5 !important;
    box-shadow: none !important;
}
.stNumberInput button:focus,
.stNumberInput button:focus-visible,
.stNumberInput button:active {
    background: rgba(124,58,237,0.16) !important;
    color: #fff !important;
    border-color: #4f46e5 !important;
    outline: none !important;
    box-shadow: none !important;
}
input[type="radio"] {
    accent-color: #7c3aed !important;
}
input[type="radio"]:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}
.stRadio > div {
    gap: 0.35rem;
    flex-wrap: wrap;
}
.stRadio label {
    border: 1.5px solid #d6d9f5;
    border-radius: 999px;
    padding: 0.3rem 0.95rem;
    min-height: 44px;
    cursor: pointer;
}
[role="radio"] label:hover {
    border-color: #7c3aed;
    color: #7c3aed;
}
[role="radio"] {
    box-shadow: none !important;
}
[role="radio"]:focus-visible {
    outline: none !important;
}
[role="radio"]:focus-visible label {
    box-shadow: 0 0 0 2px rgba(79,70,229,0.35);
    border-color: #4f46e5;
}
[role="radio"][aria-checked="true"] label {
    background: #edeaff;
    border-color: #4f46e5;
    color: #312e81;
    font-weight: 600;
}
.stRadio input[type="radio"]:checked {
    accent-color: #7c3aed !important;
    background-color: #7c3aed !important;
    border-color: #7c3aed !important;
}
.stRadio [role="radio"] svg,
.stRadio [role="radio"] svg * {
    color: #7c3aed !important;
    fill: #7c3aed !important;
    stroke: #7c3aed !important;
}
.stRadio [role="radio"][aria-checked="true"] svg,
.stRadio [role="radio"][aria-checked="true"] svg * {
    color: #7c3aed !important;
    fill: #7c3aed !important;
    stroke: #7c3aed !important;
}
.stRadio [role="radio"] > div:first-child {
    border-radius: 50% !important;
    border: 1.5px solid #d6d9f5 !important;
    background: #fff !important;
    box-shadow: none !important;
    transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}
.stRadio [role="radio"]:hover > div:first-child,
.stRadio [role="radio"]:focus-visible > div:first-child {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.2) !important;
}
.stRadio [role="radio"][aria-checked="true"] > div:first-child {
    background: #7c3aed !important;
    border-color: #7c3aed !important;
    box-shadow: inset 0 0 0 3px #fff !important;
}
.story-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #f1f5f9;
    margin-bottom: 1rem;
}
.story-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}
.stButton button {
    background: #4f46e5;
    color: #fff;
    border: none;
    border-radius: 12px;
    min-width: 120px;
    height: 42px;
}
.stButton button:hover {
    background: #4338ca;
}
.stDownloadButton button {
    background: transparent;
    border: 1.5px solid #c7d2fe;
    color: #4f46e5;
    border-radius: 12px;
    min-width: 120px;
    height: 42px;
}
.stDownloadButton button:hover {
    border-color: #4338ca;
    color: #4338ca;
}
.chip-row button {
    width: 100%;
    border-radius: 999px !important;
    border: 1.5px solid #dee4ff !important;
    background: #fff !important;
    color: #6b7280 !important;
    height: 40px;
}
.chip-row button:hover {
    border-color: #4f46e5 !important;
    color: #4f46e5 !important;
}
.safety-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    border-radius: 999px;
    padding: 0.2rem 0.75rem;
    font-size: 0.85rem;
    border: 1px solid #bbf7d0;
    color: #166534;
    background: #ecfdf5;
}
.safety-pill.danger {
    border-color: #fecaca;
    color: #b91c1c;
    background: #fff1f2;
}
.placeholder-card {
    border: 1px dashed #d1d5db;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    background: rgba(124,58,237,0.06);
    color: #4b5563;
    text-align: center;
}
.primary-btn button {
    background: linear-gradient(90deg, #4f46e5, #6d28d9);
    color: #fff;
    border: none;
    border-radius: 12px;
    height: 46px;
    font-weight: 600;
}
.primary-btn button:hover {
    background: linear-gradient(90deg, #4338ca, #5b21b6);
}
.primary-btn button:disabled {
    opacity: 0.7;
}
@media (max-width: 1100px) {
    .setup-pane {
        position: static;
    }
    .block-container {
        padding: 1rem;
    }
    .story-actions {
        justify-content: flex-start;
    }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
if "story_history" not in st.session_state:
    st.session_state.story_history = []
if "user_settings" not in st.session_state:
    st.session_state.user_settings = {}
if "active_version_idx" not in st.session_state:
    st.session_state.active_version_idx = -1
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "feedback_choice" not in st.session_state:
    st.session_state.feedback_choice = None
if "custom_feedback_note" not in st.session_state:
    st.session_state.custom_feedback_note = ""
if "feedback_reset_pending" not in st.session_state:
    st.session_state.feedback_reset_pending = False
if "story_status_message" not in st.session_state:
    st.session_state.story_status_message = ""


def format_story_html(text: str) -> str:
    escaped = html.escape(text)
    paragraphs = escaped.split("\n\n")
    return "".join(f"<p>{p}</p>" for p in paragraphs if p.strip()) or "<p></p>"


def render_skeleton():
    st.markdown(
        """
        <div class="skeleton">
            <div style="height:18px;width:40%;background:#e0e3ff;border-radius:12px;margin-bottom:1rem"></div>
            <div style="height:10px;width:90%;background:#e0e3ff;border-radius:12px;margin-bottom:0.6rem"></div>
            <div style="height:10px;width:85%;background:#e0e3ff;border-radius:12px;margin-bottom:0.6rem"></div>
            <div style="height:10px;width:80%;background:#e0e3ff;border-radius:12px;margin-bottom:0.6rem"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_generation(trigger: str, feedback_request: str = "", previous_state=None):
    saved = st.session_state.user_settings
    idea = st.session_state.get("idea_input", "").strip()
    tone_choice = st.session_state.get("tone_choice", PRESET_TONES[0])
    custom_tone_value = st.session_state.get("custom_tone_value", "").strip()
    age_value = int(st.session_state.get("age_input", saved.get("age", 7)))

    if trigger != "generate" and previous_state is None:
        st.warning("Generate a story before requesting changes.")
        return

    if trigger != "generate":
        idea = idea or saved.get("idea", "")
        tone_value = saved.get("tone", custom_tone_value or tone_choice)
    else:
        tone_value = custom_tone_value if tone_choice == CUSTOM_TONE_OPTION else tone_choice

    if not idea:
        st.warning("Please enter a seed idea (1–8 words) and generate a story first.")
        return
    if tone_value in ("", CUSTOM_TONE_OPTION):
        st.warning("Please provide a custom tone or pick one of the presets.")
        return

    st.session_state.is_loading = True
    try:
        with st.spinner("Generating bedtime story…"):
            state, story_text = generate_story(
                user_input=idea,
                age=age_value,
                tone=tone_value,
                max_iterations=DEFAULT_MAX_ITERATIONS,
                previous_state=previous_state if trigger != "generate" else None,
                feedback_request=feedback_request or None,
            )
    except Exception as exc:
        st.session_state.is_loading = False
        st.exception(exc)
        return
    st.session_state.is_loading = False

    if not story_text:
        st.error("No story was generated. Please try again.")
        return

    entry = {
        "version": len(st.session_state.story_history) + 1,
        "story": story_text,
        "state": state,
        "tone": tone_value,
        "age": age_value,
        "trigger": trigger,
    }
    st.session_state.story_history.append(entry)
    st.session_state.user_settings = {
        "idea": idea,
        "age": age_value,
        "tone": tone_value,
    }
    st.session_state.active_version_idx = len(st.session_state.story_history) - 1
    if trigger == "generate":
        st.session_state.story_status_message = "New story ready."
    elif trigger == "user_feedback":
        st.session_state.story_status_message = "Story updated with your feedback."
    else:
        st.session_state.story_status_message = "Story refreshed."


layout = st.container()
setup_col, story_col = layout.columns([0.42, 0.58], gap="large")

with setup_col:
    st.markdown('<div class="card setup-pane">', unsafe_allow_html=True)
    st.markdown("### Bedtime Story Studio")
    st.text_input(
        "Tell me a story about…",
        placeholder="first day at space camp",
        max_chars=60,
        key="idea_input",
    )
    st.number_input(
        "Listener age",
        min_value=5,
        max_value=10,
        step=1,
        value=st.session_state.get("age_input", 7),
        key="age_input",
    )
    tone_choice = st.radio(
        "Tone",
        PRESET_TONES + [CUSTOM_TONE_OPTION],
        horizontal=True,
        key="tone_choice",
    )
    if tone_choice == CUSTOM_TONE_OPTION:
        st.text_input(
            "Custom tone",
            placeholder="e.g., dreamy lullaby",
            key="custom_tone_value",
        )
    st.caption("Stories are ~300 words and safe for ages 5–10. Takes ~3–5 seconds.")
    button_label = "Generating…" if st.session_state.is_loading else "Generate Story"
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    generate_clicked = st.button(
        button_label,
        use_container_width=True,
        disabled=st.session_state.is_loading,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if generate_clicked:
        run_generation("generate")
    st.markdown("</div>", unsafe_allow_html=True)

with story_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    history = st.session_state.story_history
    if st.session_state.is_loading and not history:
        render_skeleton()
    elif not history:
        st.markdown(
            '<div class="placeholder-card">Describe a seed idea and generate to see your story here.</div>',
            unsafe_allow_html=True,
        )
    else:
        active_idx = st.session_state.active_version_idx
        if active_idx < 0 or active_idx >= len(history):
            active_idx = len(history) - 1
            st.session_state.active_version_idx = active_idx
        entry = history[active_idx]
        judge = entry["state"].judge_result or {}

        if st.session_state.is_loading:
            render_skeleton()
        else:
            story_html = format_story_html(entry["story"])
            st.markdown('<div class="story-header">', unsafe_allow_html=True)
            header_meta, header_actions = st.columns([0.6, 0.4])
            with header_meta:
                st.markdown("#### Your Story")
                st.markdown(
                    f'<div class="story-meta">Age {entry["age"]} · {entry["tone"]}</div>',
                    unsafe_allow_html=True,
                )
                if st.session_state.story_status_message:
                    st.markdown(
                        f"<div class='story-status'>{st.session_state.story_status_message}</div>",
                        unsafe_allow_html=True,
                    )
            with header_actions:
                st.markdown('<div class="story-actions">', unsafe_allow_html=True)
                st.download_button(
                    "Download",
                    data=entry["story"],
                    file_name="bedtime_story.txt",
                    mime="text/plain",
                    key="download_btn",
                    use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                "<div style='height:1px;background:#f1f5f9;margin-bottom:1rem;'></div>",
                unsafe_allow_html=True,
            )

            st.markdown(f'<div class="story-reader">{story_html}</div>', unsafe_allow_html=True)

            info_cols = st.columns([0.6, 0.4])
            with info_cols[0]:
                word_count = len(entry["story"].split())
                st.write(f"Word count: **{word_count}**")
            with info_cols[1]:
                if entry["state"].safety_notes:
                    st.markdown(
                        "<span class='safety-pill danger'>Safety: Needs edits</span>",
                        unsafe_allow_html=True,
                    )
                # else:
                #     st.markdown(
                #         "<span class='safety-pill'>Safety: Passed</span>",
                #         unsafe_allow_html=True,
                #     )

            st.markdown("#### Request changes")
            st.caption("Pick a quick tweak or write your own note.")
            if st.session_state.feedback_reset_pending:
                st.session_state.feedback_choice = None
                st.session_state.custom_feedback_note = ""
                st.session_state.feedback_reset_pending = False
            feedback_choice = st.radio(
                "Quick tweak buttons",
                FEEDBACK_CHOICES,
                horizontal=True,
                key="feedback_choice",
                index=None,
                label_visibility="collapsed",
            )
            custom_feedback_note = ""
            if feedback_choice == CUSTOM_FEEDBACK_OPTION:
                custom_feedback_note = st.text_input(
                    "Custom change request",
                    key="custom_feedback_note",
                    placeholder="e.g., add a lesson about kindness",
                )

            selected_feedback = ""
            if feedback_choice in TWEAK_HINTS:
                selected_feedback = TWEAK_HINTS[feedback_choice]
            elif feedback_choice == CUSTOM_FEEDBACK_OPTION:
                selected_feedback = custom_feedback_note.strip()

            apply_feedback = st.button(
                "Apply feedback",
                disabled=(
                    not selected_feedback
                    or st.session_state.is_loading
                ),
                key="apply_feedback_btn",
            )
            if apply_feedback and selected_feedback:
                instruction = f"Revise the story using this reader feedback: {selected_feedback}"
                run_generation(
                    "user_feedback",
                    instruction,
                    previous_state=entry["state"],
                )
                st.session_state.feedback_reset_pending = True

    st.markdown("</div>", unsafe_allow_html=True)
