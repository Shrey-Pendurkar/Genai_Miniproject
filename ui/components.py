import html
import streamlit as st

# Feather/Lucide-style stroke icons (24x24 viewBox). Used instead of emoji for a
# consistent, professional look. Unknown names fall back to rendering the text.
_ICONS = {
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "clipboard": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "bulb": '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2V17h6v-.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/>',
}


def icon_svg(name):
    """Returns inline SVG markup for a named icon, or the raw text as a fallback."""
    body = _ICONS.get(name)
    if body is None:
        return html.escape(str(name))
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{body}</svg>'


def _clean_nav_label(label):
    """'🏠 Dashboard' -> 'Dashboard' (drops the leading emoji used as a routing key)."""
    if not label:
        return "StudyMind"
    parts = label.split(" ", 1)
    return parts[1] if len(parts) == 2 and not parts[0].isalnum() else label


class UIComponents:
    @staticmethod
    def render_header(title, subtitle=None, icon=None, badge=None):
        """Page header: small section eyebrow, title and optional subtitle.

        `icon` is accepted for backwards compatibility but no longer rendered.
        """
        eyebrow = badge or _clean_nav_label(st.session_state.get("active_nav"))
        sub = f'<p class="sm-page-sub">{subtitle}</p>' if subtitle else ""
        st.markdown(f"""
        <div class="sm-page-header">
            <span class="sm-eyebrow">{html.escape(str(eyebrow))}</span>
            <h1 class="sm-page-title">{title}</h1>
            {sub}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_section_title(text):
        st.markdown(f'<div class="sm-section-title">{html.escape(text)}</div>', unsafe_allow_html=True)

    @staticmethod
    def render_icon_tile(name):
        """Standalone icon tile (HTML string) for use inside custom markup."""
        return f'<div class="sm-icon">{icon_svg(name)}</div>'

    @staticmethod
    def render_metric_card(icon, label, value, subtext=None):
        sub = f'<div class="sm-stat-sub">{subtext}</div>' if subtext else ""
        st.markdown(f"""
        <div class="sm-stat">
            <div class="sm-stat-top">
                <div class="sm-stat-label">{label}</div>
                <div class="sm-icon">{icon_svg(icon)}</div>
            </div>
            <div class="sm-stat-value">{value}</div>
            {sub}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_ai_insight_card(title, content, button_key="explain_insight"):
        st.markdown(f"""
        <div class="sm-card-accent">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <div class="sm-icon">{icon_svg("bulb")}</div>
                <div style="font-size:1.02rem; font-weight:650; color:var(--text); letter-spacing:-0.01em;">{title}</div>
            </div>
            <p style="color:var(--text-muted); font-size:0.93rem; margin:0;">{content}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_source_chips(sources):
        if not sources:
            return
        UIComponents.render_section_title("Sources")
        chips_html = ""
        for s in sources:
            chips_html += (
                '<span class="sm-chip">'
                f'<span>{html.escape(str(s["filename"]))}</span>'
                f'<span class="sm-chip-page">p. {html.escape(str(s["page_number"]))}</span>'
                f'<span class="sm-chip-score">{int(s["score"] * 100)}% match</span>'
                '</span>'
            )
        st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)

    @staticmethod
    def render_transparency_accordion(transparency_data):
        if not transparency_data:
            return
        with st.expander("How StudyMind answered · retrieval & grounding details"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Passages retrieved", transparency_data.get("retrieved_count"))
            c2.metric("Grounding confidence", f"{round((transparency_data.get('grounding_confidence') or 0) * 100)}%")
            c3.metric("Mode · Level", f"{transparency_data.get('tutor_mode')} · {transparency_data.get('level')}")
            st.write(f"**Query processed:** `{transparency_data.get('query')}`")
            st.write("**Top similarity scores:**", transparency_data.get("similarity_scores"))
            st.write("**System prompt context:**")
            st.code(transparency_data.get("system_prompt_sample"), language="markdown")
