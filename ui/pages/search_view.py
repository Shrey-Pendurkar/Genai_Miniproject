import streamlit as st
from ui.components import UIComponents
from database.models import DocumentModel
from core.vector_store import global_vector_store

def render_search_page():
    UIComponents.render_header(
        title="Semantic Search Engine",
        subtitle="Search across your study materials using deep vector similarity embeddings."
    )

    user = st.session_state.get("authenticated_user", {})
    user_id = user.get("id", 1)

    docs = DocumentModel.get_all_documents(user_id=user_id)
    doc_filter_options = ["All Uploaded Documents"] + [d["filename"] for d in docs] if docs else ["All Uploaded Documents"]

    col_q, col_doc, col_k = st.columns([3, 2, 1])
    with col_q:
        query = st.text_input("Enter search concept or phrase", placeholder="e.g. 'deadlock avoidance banker algorithm'...")
    with col_doc:
        selected_doc_filter = st.selectbox("Scope Filter", doc_filter_options)
    with col_k:
        top_k = st.number_input("Max Results", min_value=1, max_value=15, value=5)

    if query:
        with st.spinner("Executing vector embedding search across indexed passages..."):
            results = global_vector_store.search(query, top_k=top_k, user_id=user_id)

            # Optional document scope filtering
            if selected_doc_filter != "All Uploaded Documents":
                results = [r for r in results if r.get("filename") == selected_doc_filter]

        if not results:
            st.warning("No relevant passages found matching your search concept. Try uploading your study notes in **My Library (📚)**!")
        else:
            st.markdown(f"### 🎯 Found {len(results)} Relevant Passages")
            for idx, res in enumerate(results):
                score_pct = int(res['score'] * 100)
                score_color = "#34D399" if score_pct >= 70 else "#FBBF24" if score_pct >= 40 else "#FB7185"

                with st.container():
                    col_info, col_btn = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"""
                        <div class="sm-card" style="padding: 16px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-weight: 600; color: var(--text);">{res['filename']} <span style="color: var(--text-muted); font-weight: 500;">· page {res['page_number']}</span></span>
                                <span style="background: {score_color}22; color: {score_color}; font-weight: 600; font-size: 0.78rem; padding: 3px 10px; border-radius: 999px; border: 1px solid {score_color}44;">
                                    {score_pct}% match
                                </span>
                            </div>
                            <p style="color: var(--text); font-size: 0.92rem; line-height: 1.55; background: var(--surface-2); padding: 12px 14px; border-radius: 8px; border-left: 3px solid var(--accent); margin: 0;">
                                "{res['content']}"
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        st.write("")
                        st.write("")
                        if st.button("Ask tutor", key=f"btn_ask_tutor_{idx}", icon=":material/forum:", width="stretch"):
                            st.session_state["chat_history"] = st.session_state.get("chat_history", [])
                            st.session_state["chat_history"].append({
                                "role": "user",
                                "content": f"Explain this concept from '{res['filename']}': {res['content'][:150]}..."
                            })
                            st.session_state["active_nav"] = "💬 AI Tutor"
                            st.rerun()
                st.divider()
