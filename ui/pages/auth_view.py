import streamlit as st
from ui.components import icon_svg
from database.models import UserModel


def _hero():
    points = [
        ("message", "Grounded AI tutor", "Answers cite the exact page of your own notes, so you can verify every claim."),
        ("target", "Adaptive practice", "Quizzes, flashcards and mock exams that adjust to what you actually get wrong."),
        ("chart", "Progress you can see", "Track mastery, weak topics and study time in one place."),
    ]
    items = "".join(
        f'<div class="sm-auth-point"><div class="sm-icon">{icon_svg(i)}</div>'
        f'<div><b>{t}</b><span>{d}</span></div></div>'
        for i, t, d in points
    )
    st.markdown(f"""
    <div class="sm-auth-hero">
        <div class="sm-brand" style="padding-left:0;">
            <div class="sm-brand-mark">{icon_svg("brain")}</div>
            <div>
                <div class="sm-brand-name">StudyMind</div>
                <div class="sm-brand-tag">AI Personal Learning OS</div>
            </div>
        </div>
        <h1>Turn your study material into a <span>personal AI tutor.</span></h1>
        <p class="lead">Upload lecture notes, PDFs and slides. Ask questions, practise with quizzes and track your progress, all grounded in your own content.</p>
        <div class="sm-auth-points">{items}</div>
    </div>
    """, unsafe_allow_html=True)


def render_auth_page():
    st.write("")
    col_hero, _, col_form = st.columns([1.15, 0.1, 1])

    with col_hero:
        _hero()

    with col_form:
        with st.container(border=True):
            tab_login, tab_register = st.tabs(["Sign in", "Create account"])

            with tab_login:
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                st.markdown("### Welcome back")
                st.caption("Sign in to continue to your workspace.")
                with st.form("login_form", border=False):
                    email = st.text_input("Email address", placeholder="you@university.edu")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    submit_login = st.form_submit_button("Sign in", type="primary", width="stretch")

                    if submit_login:
                        if not email or not password:
                            st.error("Please enter both email and password.")
                        else:
                            user, msg = UserModel.authenticate(email, password)
                            if user:
                                st.session_state["authenticated_user"] = user
                                st.rerun()
                            else:
                                st.error(msg)

                st.markdown(
                    "<div style='display:flex;align-items:center;gap:12px;margin:6px 0 14px;color:var(--text-faint);font-size:0.78rem;'>"
                    "<div style='flex:1;height:1px;background:var(--border)'></div>or"
                    "<div style='flex:1;height:1px;background:var(--border)'></div></div>",
                    unsafe_allow_html=True,
                )
                if st.button("Continue with demo account", key="btn_demo_login", icon=":material/bolt:", width="stretch"):
                    demo_user = UserModel.get_user(1)
                    st.session_state["authenticated_user"] = demo_user
                    st.rerun()

            with tab_register:
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                st.markdown("### Create your account")
                st.caption("Free, private and stored locally on this machine.")
                with st.form("register_form", border=False):
                    reg_name = st.text_input("Full name", placeholder="Alex Morgan")
                    reg_email = st.text_input("Email address", placeholder="you@university.edu")
                    reg_pwd = st.text_input("Password", type="password", placeholder="At least 4 characters")
                    reg_pwd_confirm = st.text_input("Confirm password", type="password", placeholder="Repeat your password")
                    submit_reg = st.form_submit_button("Create account", type="primary", width="stretch")

                    if submit_reg:
                        if not reg_name or not reg_email or not reg_pwd:
                            st.error("All fields are required.")
                        elif reg_pwd != reg_pwd_confirm:
                            st.error("Passwords do not match.")
                        elif len(reg_pwd) < 4:
                            st.error("Password must be at least 4 characters long.")
                        else:
                            user, msg = UserModel.register(reg_name, reg_email, reg_pwd)
                            if user:
                                st.session_state["authenticated_user"] = user
                                st.rerun()
                            else:
                                st.error(msg)
