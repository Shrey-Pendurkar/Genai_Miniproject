import html
import streamlit as st
import logging

# Page Config must be first Streamlit call
st.set_page_config(
    page_title="StudyMind | AI Personal Learning OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.styles import inject_custom_css
from ui.components import icon_svg
from utils.seed_demo_data import seed_demo_data_if_needed
from database.models import UserModel

# Import page views
from ui.pages.auth_view import render_auth_page
from ui.pages.dashboard_view import render_dashboard_page
from ui.pages.library_view import render_library_page
from ui.pages.tutor_view import render_tutor_page
from ui.pages.search_view import render_search_page
from ui.pages.summarize_view import render_summarize_page
from ui.pages.quiz_view import render_quiz_page
from ui.pages.flashcards_view import render_flashcards_page
from ui.pages.mock_exam_view import render_mock_exam_page
from ui.pages.study_planner_view import render_study_planner_page
from ui.pages.analytics_view import render_analytics_page
from ui.pages.weak_topics_view import render_weak_topics_page
from ui.pages.responsible_ai_view import render_responsible_ai_page
from ui.pages.settings_view import render_settings_page
from ui.pages.professor_demo_view import render_professor_demo_page

logger = logging.getLogger(__name__)

# Display-only Material icons for the sidebar menu, keyed by the routing label.
NAV_ICONS = {
    "🏠 Dashboard": ":material/space_dashboard:",
    "📚 My Library": ":material/library_books:",
    "💬 AI Tutor": ":material/forum:",
    "🔎 Semantic Search": ":material/search:",
    "📝 Summarize": ":material/summarize:",
    "🎯 Quiz Generator": ":material/quiz:",
    "🃏 Flashcards": ":material/style:",
    "🧪 Mock Exam": ":material/assignment:",
    "📅 Study Planner": ":material/calendar_month:",
    "📊 Analytics": ":material/monitoring:",
    "🧠 Weak Topics": ":material/trending_down:",
    "⚖️ Responsible AI": ":material/verified_user:",
    "🧪 How It Works (Viva)": ":material/account_tree:",
    "⚙ Settings": ":material/settings:",
}

@st.cache_resource(show_spinner="Preparing demo study materials (first start only)...")
def _bootstrap_demo_data():
    """Seeds the demo study notes (DB rows + vector index) once per server process.

    The database, vector index and uploads are git-ignored, so a fresh deployment starts
    empty. seed_demo_data_if_needed() is a no-op when the demo documents already exist.
    """
    seed_demo_data_if_needed()
    return True

def main():
    # Inject Custom CSS
    inject_custom_css()

    # Make sure the demo account has its study notes (fresh deployments start empty)
    _bootstrap_demo_data()

    # Check Authentication Gate
    user = st.session_state.get("authenticated_user")
    if not user:
        render_auth_page()
        return

    # Sidebar Header Branding
    with st.sidebar:
        st.markdown(f"""
        <div class="sm-brand">
            <div class="sm-brand-mark">{icon_svg("brain")}</div>
            <div>
                <div class="sm-brand-name">StudyMind</div>
                <div class="sm-brand-tag">AI Personal Learning OS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Options
        nav_options = [
            "🏠 Dashboard",
            "📚 My Library",
            "💬 AI Tutor",
            "🔎 Semantic Search",
            "📝 Summarize",
            "🎯 Quiz Generator",
            "🃏 Flashcards",
            "🧪 Mock Exam",
            "📅 Study Planner",
            "📊 Analytics",
            "🧠 Weak Topics",
            "⚖️ Responsible AI",
            "🧪 How It Works (Viva)",
            "⚙ Settings"
        ]

        # Handle navigation state
        default_nav = st.session_state.get("active_nav", "🏠 Dashboard")
        default_idx = nav_options.index(default_nav) if default_nav in nav_options else 0

        # Routing keys stay as-is (other pages set `active_nav` with them);
        # only the displayed label changes to a clean text + Material icon.
        selected_nav = st.radio(
            "Main Navigation",
            nav_options,
            index=default_idx,
            label_visibility="collapsed",
            format_func=lambda key: f"{NAV_ICONS.get(key, ':material/circle:')}  {key.split(' ', 1)[1]}",
        )
        st.session_state["active_nav"] = selected_nav

        st.markdown("---")

        # Logged In User Profile & Logout
        user_name = html.escape(str(user.get('name', 'Student')))
        initials = "".join(w[0] for w in user_name.split()[:2]).upper() or "S"
        st.markdown(f"""
        <div class="sm-user">
            <div class="sm-avatar">{initials}</div>
            <div style="min-width:0;">
                <div class="sm-user-name">{user_name}</div>
                <div class="sm-user-meta">Level {user.get('level', 1)} · {user.get('xp_points', 150)} XP</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        if st.button("Sign out", key="btn_logout", icon=":material/logout:", width="stretch"):
            st.session_state["authenticated_user"] = None
            st.session_state["active_nav"] = "🏠 Dashboard"
            st.rerun()

    # Route to Selected Page View
    if selected_nav == "🏠 Dashboard":
        render_dashboard_page()
    elif selected_nav == "📚 My Library":
        render_library_page()
    elif selected_nav == "💬 AI Tutor":
        render_tutor_page()
    elif selected_nav == "🔎 Semantic Search":
        render_search_page()
    elif selected_nav == "📝 Summarize":
        render_summarize_page()
    elif selected_nav == "🎯 Quiz Generator":
        render_quiz_page()
    elif selected_nav == "🃏 Flashcards":
        render_flashcards_page()
    elif selected_nav == "🧪 Mock Exam":
        render_mock_exam_page()
    elif selected_nav == "📅 Study Planner":
        render_study_planner_page()
    elif selected_nav == "📊 Analytics":
        render_analytics_page()
    elif selected_nav == "🧠 Weak Topics":
        render_weak_topics_page()
    elif selected_nav == "⚖️ Responsible AI":
        render_responsible_ai_page()
    elif selected_nav == "🧪 How It Works (Viva)":
        render_professor_demo_page()
    elif selected_nav == "⚙ Settings":
        render_settings_page()

if __name__ == "__main__":
    main()
