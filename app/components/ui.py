# app/components/ui.py
import streamlit as st

def set_theme(dark_mode=False):
    """Apply CSS theme depending on dark/light mode."""
    if dark_mode:
        # Dark mode CSS
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
                color: #f8fafc;
            }
            .card {
                background: rgba(30, 41, 59, 0.9);
                border-radius: 12px;
                padding: 18px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.6);
                margin-bottom: 12px;
            }
            .big-title {
                font-size:28px;
                font-weight:800;
                color:#38bdf8;
            }
            .muted {
                color:#94a3b8;
            }
            .metric {
                font-size: 22px;
                color: #22c55e;
                font-weight:700;
            }
            </style>
            """, unsafe_allow_html=True
        )
    else:
        # Light mode CSS
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(180deg, #f9fafb 0%, #f1f5f9 50%, #f9fafb 100%);
                color: #0f172a;
            }
            .card {
                background: rgba(255,255,255,0.95);
                border-radius: 12px;
                padding: 18px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.08);
                margin-bottom: 12px;
            }
            .big-title {
                font-size:28px;
                font-weight:800;
                color:#075985;
            }
            .muted {
                color:#475569;
            }
            .metric {
                font-size: 22px;
                color: #16a34a;
                font-weight:700;
            }
            </style>
            """, unsafe_allow_html=True
        )

def header(title="🌱 Crop Yield Predictor", subtitle="Interactive ML tool for sustainable farming"):
    st.markdown(
        f"<div class='card'><div class='big-title'>{title}</div><div class='muted'>{subtitle}</div></div>",
        unsafe_allow_html=True
    )

def footer():
    st.markdown(
        "<div style='text-align:center; color:#94a3b8; margin-top:20px'>🌾 Built with ❤️ for sustainable agriculture 🌍</div>",
        unsafe_allow_html=True
    )
