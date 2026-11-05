import html
import streamlit as st
from ui.components import UIComponents, icon_svg
from features.analytics import AnalyticsFeature
from features.study_plan import StudyPlanFeature
from database.models import UserModel, DocumentModel, WeakTopicModel

# (icon, title, description, button label, target nav key)
QUICK_LAUNCH = [
    ("message", "AI Tutor", "Ask questions and get grounded answers with source citations.", "Open tutor", "💬 AI Tutor"),
    ("book", "My Library", "Upload and manage PDFs, notes and textbook chapters.", "Open library", "📚 My Library"),
    ("search", "Semantic Search", "Vector similarity search across your uploaded documents.", "Open search", "🔎 Semantic Search"),
    ("file", "Summarizer", "Generate executive, medium or detailed study guides.", "Open summarizer", "📝 Summarize"),
    ("target", "Quiz Generator", "Generate custom questions and test your understanding.", "Start a quiz", "🎯 Quiz Generator"),
    ("layers", "Flashcards", "Revise key terms with spaced-repetition cards.", "Study cards", "🃏 Flashcards"),
    ("clipboard", "Mock Exam", "Simulate a timed university exam under pressure.", "Take an exam", "🧪 Mock Exam"),
    ("calendar", "Study Planner", "A personalised daily schedule and task tracker.", "View schedule", "📅 Study Planner"),
]


def render_dashboard_page():
    user = st.session_state.get("authenticated_user", {})
    user_id = user.get("id", 1)
    db_user = UserModel.get_user(user_id=user_id)
    first_name = html.escape(str(db_user.get("name", "Student")).split()[0])

    UIComponents.render_header(
        title=f"Welcome back, {first_name}",
        subtitle="Your learning overview: study metrics, recommendations and shortcuts to every tool.",
        badge="Dashboard",
    )

    metrics = AnalyticsFeature.get_dashboard_metrics(user_id=user_id)

    # Key stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        UIComponents.render_metric_card("book", "Knowledge base", f"{metrics['doc_count']} docs", "Indexed study materials")
    with col2:
        UIComponents.render_metric_card("flame", "Study streak", f"{metrics['streak']} days", "Consecutive active days")
    with col3:
        UIComponents.render_metric_card("target", "Quiz accuracy", f"{metrics['quiz_accuracy']}%", "Average across attempts")
    with col4:
        UIComponents.render_metric_card("clock", "Focus time", f"{metrics['study_hours']} hrs", "Logged learning sessions")

    st.write("")

    # Insight + rank
    col_left, col_right = st.columns([1.65, 1])

    with col_left:
        UIComponents.render_section_title("AI learning insight")

        user_docs = DocumentModel.get_all_documents(user_id=user_id)
        weak_topics = WeakTopicModel.get_weak_topics(user_id=user_id)

        if not user_docs:
            insight_title = "Get started with StudyMind"
            insight_text = (
                "You haven't uploaded any study materials yet. Head to <b>My Library</b> to add your course PDFs, "
                "lecture notes or syllabus. StudyMind will then generate flashcards, quizzes and grounded tutor answers from them."
            )
        elif weak_topics:
            top_weak = weak_topics[0]
            insight_title = f"Focus area: {html.escape(str(top_weak['topic']))}"
            insight_text = (
                f"Based on your recent quiz attempts, your lowest-accuracy topic is <b>{html.escape(str(top_weak['topic']))}</b> "
                f"({top_weak['accuracy_percentage']}% accuracy). Use the <b>AI Tutor</b> or <b>Flashcards</b> "
                "to practise it before your next exam."
            )
        else:
            doc_names = ", ".join(f"<code>{html.escape(str(d['filename']))}</code>" for d in user_docs[:3])
            insight_title = "Your library is ready"
            insight_text = (
                f"You have <b>{len(user_docs)} study materials</b> indexed ({doc_names}). "
                "Try a practice quiz or ask the <b>AI Tutor</b> a question to test your knowledge."
            )

        UIComponents.render_ai_insight_card(title=insight_title, content=insight_text)

    with col_right:
        UIComponents.render_section_title("Student rank")
        level = metrics["level"]
        xp = metrics["xp_points"]
        level_target = max(level * 100, 1)
        next_xp = max(0, level_target - xp)
        pct = max(0, min(100, round(xp / level_target * 100)))
        st.markdown(f"""
        <div class="sm-card">
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="sm-icon">{icon_svg("award")}</div>
                <div>
                    <div style="font-size:1rem; font-weight:650; color:var(--text);">Level {level}</div>
                    <div style="font-size:0.78rem; color:var(--text-muted);">Knowledge Seeker</div>
                </div>
                <div style="margin-left:auto; font-size:0.85rem; font-weight:600; color:#C7D2FE;">{xp} XP</div>
            </div>
            <div class="sm-progress"><div style="width:{pct}%"></div></div>
            <div style="margin-top:10px; font-size:0.78rem; color:var(--text-muted);">
                <b style="color:var(--text);">{next_xp} XP</b> to reach Level {level + 1}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Quick launch grid
    UIComponents.render_section_title("Quick launch")
    for row_start in range(0, len(QUICK_LAUNCH), 4):
        cols = st.columns(4)
        for col, (icon, title, desc, btn, target) in zip(cols, QUICK_LAUNCH[row_start:row_start + 4]):
            with col:
                with st.container(border=True):
                    st.markdown(
                        f'<div class="sm-icon">{icon_svg(icon)}</div>'
                        f'<div class="sm-feature-title">{title}</div>'
                        f'<p class="sm-feature-desc">{desc}</p>',
                        unsafe_allow_html=True,
                    )
                    if st.button(btn, key=f"dash_nav_{row_start}_{title}", width="stretch"):
                        st.session_state["active_nav"] = target
                        st.rerun()

    st.write("")

    # Today's schedule
    UIComponents.render_section_title("Today's study schedule")
    plans = StudyPlanFeature.get_plans()

    if not plans:
        st.info("No study tasks scheduled for today. Generate a personalised plan in the Study Planner.")
    else:
        with st.container(border=True):
            for task in plans[:4]:
                task_id = task["id"]
                is_done = task["status"] == "completed"
                label = f"**{task['time_slot']}** — {task['title']} (`{task['topic']}`)"

                checked = st.checkbox(label, value=is_done, key=f"dash_task_{task_id}")
                if checked != is_done:
                    StudyPlanFeature.toggle_task(task_id, task["status"])
                    st.rerun()
