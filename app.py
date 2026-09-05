import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path

st.set_page_config(page_title="MedRAG AI", page_icon="M", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --accent: #0097a7;
    --accent2: #00bcd4;
    --accent3: #006064;
    --txt: #0d2137;
    --txt2: #37474f;
    --txt3: #607d8b;
    --brd: rgba(0,151,167,0.15);
}

body, p, span, div, h1, h2, h3, h4, h5, h6, li, label, input, textarea, select {
    font-family: 'Inter', sans-serif !important;
}

html, body, #root {
    background: #f0f9ff !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box;
}

[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
.main,
.block-container,
[data-testid="stSidebar"],
header,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
section.main,
div.main,
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="column"],
div[data-testid="chatInputContainer"],
div[data-testid="stChatInputFooter"],
div[data-testid="stBottom"],
div[data-testid="ScrollToBottomContainer"],
div[style*="background"],
div[style*="background-color"] {
    background-color: #f0f9ff !important;
    background: #f0f9ff !important;
}

header[data-testid="stHeader"], header[data-testid="stHeader"] * {
    background: #f0f9ff !important;
}
[data-testid="stToolbar"] { background: #f0f9ff !important; }
.stDeployButton button { background: transparent !important; color: var(--txt3) !important; }
.main .block-container { background: transparent !important; padding-top: 1rem; max-width: 800px; margin: 0 auto; }

[data-testid="stSidebar"] {
    background: #f0f9ff !important;
    border-right: 1px solid var(--brd) !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    transition: width 0.3s ease, min-width 0.3s ease, max-width 0.3s ease, transform 0.3s ease !important;
}
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] section,
[data-testid="stSidebar"] article,
[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"],
[data-testid="stSidebar"] [data-testid="column"],
[data-testid="stSidebar"] [data-testid="column"] > div {
    background: #f0f9ff !important;
}
[data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
    font-family: 'Inter', sans-serif !important;
    color: var(--txt) !important;
}
[data-testid="stSidebar"] * {
    transition: none !important;
    transform: none !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"] button,
[data-testid="stSidebarHeader"] [data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebar"] [data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}

[data-testid="stSidebarHeader"] {
    padding: 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    overflow: hidden !important;
}

.block-container {
    transition: padding-left 0.3s ease, max-width 0.3s ease !important;
}

.sidebar-hamburger {
    position: absolute !important;
    top: 16px !important;
    left: 16px !important;
    z-index: 1001 !important;
    width: 40px !important;
    height: 40px !important;
    background: rgba(0,151,167,0.08) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.15s ease !important;
}
.sidebar-hamburger:hover {
    background: rgba(0,151,167,0.15) !important;
    border-color: var(--accent2) !important;
}
.sidebar-hamburger:active {
    transform: scale(0.93) !important;
}
.sidebar-hamburger .bar {
    display: block !important;
    width: 20px !important;
    height: 2px !important;
    background: var(--accent3) !important;
    border-radius: 2px !important;
    transition: transform 0.3s ease, opacity 0.3s ease !important;
    position: absolute !important;
    left: 10px !important;
}
.sidebar-hamburger .bar:nth-child(1) { top: 13px !important; }
.sidebar-hamburger .bar:nth-child(2) { top: 19px !important; }
.sidebar-hamburger .bar:nth-child(3) { top: 25px !important; }

body.sidebar-open .sidebar-hamburger .bar:nth-child(1) {
    top: 19px !important;
    transform: rotate(45deg) !important;
}
body.sidebar-open .sidebar-hamburger .bar:nth-child(2) {
    opacity: 0 !important;
}
body.sidebar-open .sidebar-hamburger .bar:nth-child(3) {
    top: 19px !important;
    transform: rotate(-45deg) !important;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 1;
    padding: 0 4px;
}

[data-testid="stSidebar"] .stButton { margin: 0 !important; padding: 0 !important; }
[data-testid="stSidebar"] .stButton > button {
    all: unset !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    width: calc(100% - 16px) !important;
    margin: 5px 8px !important;
    padding: 11px 16px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--txt2) !important;
    background: #ffffff !important;
    border: 1px solid var(--brd) !important;
    cursor: pointer !important;
    text-align: left !important;
    transition: background 150ms ease, color 150ms ease, padding 0.3s ease, margin 0.3s ease, justify-content 0.3s ease, border-radius 0.3s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,151,167,0.08) !important;
    border-color: var(--accent2) !important;
    color: var(--accent) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
}
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
}

.nav-ico {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 20px !important;
    height: 20px !important;
    flex-shrink: 0 !important;
}
.nav-ico svg {
    width: 18px !important;
    height: 18px !important;
    color: var(--txt3) !important;
    stroke: currentColor !important;
    fill: none !important;
    stroke-width: 1.5 !important;
}
.nav-label {
    transition: opacity 0.2s ease, width 0.3s ease, max-width 0.3s ease, margin 0.3s ease, padding 0.3s ease, overflow 0.3s ease !important;
    white-space: nowrap !important;
}

body.sidebar-collapsed [data-testid="stSidebar"] {
    width: 70px !important;
    min-width: 70px !important;
    max-width: 70px !important;
}
body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button {
    justify-content: center !important;
    padding: 11px 0 !important;
    margin: 5px 6px !important;
    border-radius: 10px !important;
}
body.sidebar-collapsed .nav-label {
    opacity: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}
body.sidebar-collapsed .sidebar-brand-name {
    opacity: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}
body.sidebar-collapsed .doc-name,
body.sidebar-collapsed .doc-meta {
    opacity: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}
body.sidebar-collapsed .doc-item {
    justify-content: center !important;
    padding: 8px 4px !important;
    margin: 0 2px 2px !important;
}
body.sidebar-collapsed .sec-label {
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}
body.sidebar-collapsed .sidebar-footer {
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}
body.sidebar-collapsed .sidebar-brand {
    justify-content: center !important;
    padding: 4px 0 12px !important;
}

body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button {
    position: relative !important;
}
body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button .nav-ico {
    position: relative !important;
}
body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button .nav-ico::after {
    content: attr(data-tooltip) !important;
    position: absolute !important;
    left: calc(100% + 12px) !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    background: var(--accent3) !important;
    color: #ffffff !important;
    padding: 6px 12px !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    opacity: 0 !important;
    pointer-events: none !important;
    transition: opacity 0.2s ease !important;
    z-index: 9999 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}
body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button:hover .nav-ico::after {
    opacity: 1 !important;
}
body.sidebar-collapsed [data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,151,167,0.08) !important;
}

.sep { height: 1px; background: var(--brd); margin: 8px 16px; }
body.sidebar-collapsed .sep { margin: 8px 8px !important; }
.sec-label { font-size: 11px; font-weight: 600; color: var(--txt3); text-transform: uppercase; letter-spacing: 0.8px; padding: 0 16px; margin: 12px 0 8px; transition: opacity 0.2s ease, height 0.3s ease, overflow 0.3s ease !important; }

.doc-item { display: flex; align-items: center; gap: 10px; padding: 8px 14px; margin: 0 12px 2px; transition: justify-content 0.3s ease, padding 0.3s ease, margin 0.3s ease !important; }
.doc-ico { width: 28px; height: 28px; background: #e0f2f1; border: 1px solid var(--brd); border-radius: 6px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.doc-ico svg { width: 14px; height: 14px; color: var(--accent) !important; }
.doc-name { font-size: 13px; font-weight: 500; transition: opacity 0.2s ease, width 0.3s ease, max-width 0.3s ease, overflow 0.3s ease !important; }
.doc-meta { font-size: 11px; color: var(--txt3) !important; transition: opacity 0.2s ease, width 0.3s ease, max-width 0.3s ease, overflow 0.3s ease !important; }

.sidebar-footer { padding: 12px 16px; border-top: 1px solid var(--brd); transition: opacity 0.2s ease, height 0.3s ease, overflow 0.3s ease, padding 0.3s ease !important; }
.footer-row { display: flex; align-items: center; gap: 8px; padding: 6px 0; color: var(--txt3); font-size: 12px; }
.footer-row svg { width: 14px; height: 14px; }
.status-row { display: flex; align-items: center; gap: 6px; font-size: 10px; color: var(--txt3); padding-top: 8px; margin-top: 8px; border-top: 1px solid var(--brd); }
.status-dot { width: 6px; height: 6px; background: var(--accent2); border-radius: 50%; }

.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 4px 0 12px; transition: justify-content 0.3s ease !important; }
.brand-box {
    width: 32px; height: 32px; flex-shrink: 0;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 8px rgba(0,151,167,0.2);
}
.brand-box svg { width: 18px; height: 18px; color: #fff !important; }
.brand-name { font-size: 15px; font-weight: 600; color: var(--accent3) !important; transition: opacity 0.2s ease, width 0.3s ease, max-width 0.3s ease, overflow 0.3s ease !important; }

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] > div > div > div,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] button,
[data-testid="stChatInput"] [data-testid="stChatInputTextArea"],
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stChatInputFooter"],
[data-testid="stBottom"],
[data-testid="ScrollToBottomContainer"],
[data-testid="stBottomBlockContainer"],
[data-testid="chatInputFooter"],
[data-testid="chatInputContainer"] {
    background: #ffffff !important;
    color: var(--txt) !important;
    background-color: #ffffff !important;
}
[data-testid="stChatInput"] {
    border-top: 1px solid var(--brd) !important;
    background: #ffffff !important;
}
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: var(--txt) !important;
}

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    position: relative !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #e0f2f1 !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300897b' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4.418 3.582-8 8-8s8 3.582 8 8'/%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 22px 22px !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: #e0f7fa !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230097a7' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='2' x2='12' y2='5'/%3E%3Ccircle cx='12' cy='2' r='1' fill='%230097a7' stroke='none'/%3E%3Crect x='5' y='5' width='14' height='12' rx='4'/%3E%3Ccircle cx='9' cy='11' r='1.5' fill='%230097a7' stroke='none'/%3E%3Ccircle cx='15' cy='11' r='1.5' fill='%230097a7' stroke='none'/%3E%3Cline x1='8.5' y1='15' x2='15.5' y2='15'/%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 22px 22px !important;
}
[data-testid="stChatMessageAvatarUser"] > *,
[data-testid="stChatMessageAvatarAssistant"] > * {
    font-size: 0 !important;
    color: transparent !important;
    line-height: 0 !important;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}

.main-header {
    background: linear-gradient(90deg, var(--accent3), var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    font-weight: 700;
}
.src-box { background: rgba(0,151,167,0.06); border-left: 3px solid var(--accent); padding: 8px 12px; margin: 6px 0; font-size: 12px; border-radius: 0 6px 6px 0; color: var(--txt2); }
.stAlert { background: rgba(255,255,255,0.9) !important; border: 1px solid var(--brd) !important; border-radius: 10px !important; }
.stWarning { border-left: 4px solid var(--accent) !important; }
.stSuccess { border-left: 4px solid #10b981 !important; }
.stInfo { border-left: 4px solid var(--accent2) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--accent3) !important; }
p,span,li { color: var(--txt2); }
[data-testid="stSidebarNav"] { display: none; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--brd); border-radius: 3px; }

@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
    }
    body.sidebar-collapsed [data-testid="stSidebar"] {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
(function() {
    function syncSidebarState() {
        var sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;
        var expanded = sidebar.getAttribute('aria-expanded') !== 'false';
        if (expanded) {
            document.body.classList.add('sidebar-open');
            document.body.classList.remove('sidebar-collapsed');
        } else {
            document.body.classList.add('sidebar-collapsed');
            document.body.classList.remove('sidebar-open');
        }
    }

    function hideDefaultButtons() {
        var selectors = [
            '[data-testid="stSidebarCollapseButton"]',
            '[data-testid="stSidebarHeader"] button',
            '[data-testid="stSidebarHeader"] [data-testid="stBaseButton-headerNoPadding"]',
            '[data-testid="stSidebar"] [data-testid="stBaseButton-headerNoPadding"]'
        ];
        selectors.forEach(function(sel) {
            document.querySelectorAll(sel).forEach(function(el) {
                el.style.display = 'none';
            });
        });
    }

    function createHamburger() {
        var existing = document.querySelector('.sidebar-hamburger');
        if (existing) existing.remove();

        var sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        var btn = document.createElement('div');
        btn.className = 'sidebar-hamburger';
        btn.title = 'Toggle sidebar';
        btn.innerHTML = '<span class="bar"></span><span class="bar"></span><span class="bar"></span>';
        btn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            var collapseBtn = document.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (collapseBtn) {
                collapseBtn.click();
            } else {
                var expandBtn = document.querySelector('[data-testid="stExpandSidebarButton"]');
                if (expandBtn) expandBtn.click();
            }
        };
        sidebar.style.position = 'relative';
        sidebar.appendChild(btn);
    }

    function init() {
        hideDefaultButtons();
        createHamburger();
        syncSidebarState();
    }

    init();
    var debounceTimer;
    var observer = new MutationObserver(function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            hideDefaultButtons();
            createHamburger();
            syncSidebarState();
        }, 50);
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['aria-expanded']
    });
})();
</script>
""", unsafe_allow_html=True)

ICONS = {
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "docs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "pdf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "help": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "brand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
}

def init():
    for k, v in [("messages", []), ("pipeline", None), ("documents_processed", False), ("active_page", "chat"), ("uploaded_docs", [])]:
        if k not in st.session_state:
            st.session_state[k] = v

def save_file(f):
    try:
        from src.config import MEDICAL_DOCS_DIR
        MEDICAL_DOCS_DIR.mkdir(parents=True, exist_ok=True)
        p = MEDICAL_DOCS_DIR / f.name
        p.write_bytes(f.getvalue())
        st.session_state.uploaded_docs.append({"name": f.name, "size": f.size, "path": p, "pages": 0})
        return p
    except Exception as e:
        st.error(str(e))
        return None

def process_docs():
    try:
        with st.spinner("Loading AI models (this may take a minute on first run)..."):
            from src.rag_pipeline import MedicalRAGPipeline
            from src.config import MEDICAL_DOCS_DIR
            pipeline = MedicalRAGPipeline()
            n = pipeline.ingest_documents(MEDICAL_DOCS_DIR)
            st.session_state.pipeline = pipeline
            st.session_state.documents_processed = True
            return n
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return 0

def sidebar():
    with st.sidebar:
        st.markdown(f'''
        <div class="sidebar-brand">
            <div class="brand-box">{ICONS["brand"]}</div>
            <span class="sidebar-brand-name brand-name">MedRAG AI</span>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

        nav_items = [
            ("chat", "Chat", ICONS["chat"]),
            ("documents", "Documents", ICONS["docs"]),
            ("settings", "Settings", ICONS["settings"]),
        ]
        for key, label, icon in nav_items:
            if st.button(f"  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.active_page = key
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-label">Documents</div>', unsafe_allow_html=True)

        for d in st.session_state.uploaded_docs[-5:]:
            st.markdown(f'''
            <div class="doc-item">
                <div class="doc-ico">{ICONS["pdf"]}</div>
                <div><div class="doc-name">{d["name"]}</div><div class="doc-meta">{d.get("pages","-")} pages</div></div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

        if st.button(f"  Help", key="nav_help", use_container_width=True):
            st.session_state.active_page = "help"
            st.rerun()
        if st.button(f"  About", key="nav_about", use_container_width=True):
            st.session_state.active_page = "about"
            st.rerun()

        st.markdown(f'''
        <div class="sidebar-footer">
            <div class="status-row"><div class="status-dot"></div>Medical assistant v1.0</div>
        </div>
        ''', unsafe_allow_html=True)

page_icons = {"chat": ICONS["chat"], "documents": ICONS["docs"], "settings": ICONS["settings"], "help": ICONS["help"], "about": ICONS["info"]}
page_tooltips = {"chat": "Chat", "documents": "Documents", "settings": "Settings", "help": "Help", "about": "About"}
st.markdown(f"""
<script>
(function() {{
    function injectNavIcons() {{
        var iconMap = { {k: v.replace('<svg', '<svg class="nav-svg"') for k, v in page_icons.items() if k in ["chat","documents","settings"]} };
        var tooltipMap = {page_tooltips};
        document.querySelectorAll('[data-testid="stSidebar"] .stButton > button').forEach(function(btn) {{
            var text = btn.textContent.trim();
            var existing = btn.querySelector('.nav-ico');
            if (existing) existing.remove();
            var iconKey = null;
            if (text.includes('Chat')) iconKey = 'chat';
            else if (text.includes('Documents')) iconKey = 'documents';
            else if (text.includes('Settings')) iconKey = 'settings';
            else if (text.includes('Help')) iconKey = 'help';
            else if (text.includes('About')) iconKey = 'about';
            if (iconKey && iconMap[iconKey]) {{
                var icoSpan = document.createElement('span');
                icoSpan.className = 'nav-ico';
                icoSpan.setAttribute('data-tooltip', tooltipMap[iconKey] || '');
                icoSpan.innerHTML = iconMap[iconKey];
                btn.insertBefore(icoSpan, btn.firstChild);
            }}
        }});
    }}
    injectNavIcons();
    var debounce;
    new MutationObserver(function() {{
        clearTimeout(debounce);
        debounce = setTimeout(injectNavIcons, 100);
    }}).observe(document.body, {{childList: true, subtree: true}});
}})();
</script>
""", unsafe_allow_html=True)

def chat_page():
    st.markdown("<h1 class='main-header'>Medical Information Assistant</h1>", unsafe_allow_html=True)
    if not st.session_state.documents_processed:
        st.info("Upload medical PDFs in the sidebar, then ask questions here.")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "sources" in m:
                for s in m["sources"]:
                    st.markdown(f'<div class="src-box">{s["document_name"]} - Page {s["page_number"]}</div>', unsafe_allow_html=True)
    if q := st.chat_input("Ask a medical question..."):
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)
        if not st.session_state.pipeline:
            r = "Please upload and process documents first."
            st.session_state.messages.append({"role": "assistant", "content": r})
            with st.chat_message("assistant"):
                st.markdown(r)
            return
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                try:
                    res = st.session_state.pipeline.answer_question(q)
                    st.markdown(res["answer"])
                    for s in res["sources"]:
                        st.markdown(f'<div class="src-box">{s["document_name"]} - Page {s["page_number"]}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": res["answer"], "sources": res["sources"]})
                except Exception as e:
                    st.error(str(e))

def docs_page():
    st.markdown("<h1 class='main-header'>Documents</h1>", unsafe_allow_html=True)
    st.markdown("Upload your medical PDF files to build the knowledge base.")
    st.markdown("")

    st.markdown('''<style>
    div[data-testid="stFileUploader"] label{font-size:0 !important;height:0 !important;overflow:hidden !important;margin:0 !important;padding:0 !important}
    div[data-testid="stFileUploader"] section{border:2px dashed rgba(0,151,167,0.3) !important;border-radius:12px !important;background:#f0f9ff !important;padding:24px 20px !important;display:flex !important;flex-direction:column !important;align-items:center !important;justify-content:center !important;min-height:180px !important}
    div[data-testid="stFileUploader"] section:hover{border-color:#0097a7 !important;background:#e0f7fa !important}
    div[data-testid="stFileUploader"] section p{color:#37474f !important;font-family:Inter,sans-serif !important;text-align:center !important;margin-bottom:4px !important}
    div[data-testid="stFileUploader"] section small{color:#607d8b !important;text-align:center !important}
    div[data-testid="stFileUploader"] section button{background:#0097a7 !important;color:#0097a7 !important;border:none !important;border-radius:8px !important;font-family:Inter,sans-serif !important;font-weight:600 !important;padding:8px 24px !important;text-indent:-9999px !important;position:relative !important;overflow:hidden !important;min-width:130px !important;margin-top:12px !important}
    div[data-testid="stFileUploader"] section button::after{content:"Browse Files" !important;position:absolute !important;left:0 !important;top:0 !important;width:100% !important;text-indent:0 !important;color:#fff !important;font-size:13px !important;display:flex !important;align-items:center !important;justify-content:center !important;height:100% !important}
    div[data-testid="stFileUploader"] section button:hover{background:#00bcd4 !important}
    </style>''', unsafe_allow_html=True)

    files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if files:
        st.markdown(f"**{len(files)} file(s) selected**")
        if st.button("Process Documents", type="primary"):
            saved = [save_file(f) for f in files if save_file(f)]
            if saved:
                n = process_docs()
                if n:
                    st.success(f"Processed {len(saved)} files into {n} chunks")

    if st.session_state.uploaded_docs:
        st.markdown("---")
        st.subheader("Uploaded Documents")
        for d in st.session_state.uploaded_docs:
            st.markdown(f"**{d['name']}** - {d.get('pages','-')} pages")

def settings_page():
    st.markdown("<h1 class='main-header'>Settings</h1>", unsafe_allow_html=True)
    if st.session_state.pipeline:
        info = st.session_state.pipeline.get_pipeline_info()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Embedding Model**")
            st.info(info["embedding_model"])
        with c2:
            st.markdown("**LLM Model**")
            st.info(info["llm_model"])
        st.markdown(f"**Documents in DB:** {info['vector_store']['document_count']}")
    st.warning("Educational purposes only. Not medical advice.")

def help_page():
    st.markdown("<h1 class='main-header'>Help</h1>", unsafe_allow_html=True)
    st.markdown("### How to Use MedRAG AI")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**1. Upload Documents**")
        st.markdown("Go to **Documents** and upload your medical PDFs.")
        st.markdown("**2. Process Documents**")
        st.markdown("Click **Process Documents** to index your PDFs.")
    with c2:
        st.markdown("**3. Ask Questions**")
        st.markdown("Go to **Chat** and type your medical question.")
        st.markdown("**4. View Sources**")
        st.markdown("Check source references for verification.")
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("- **RAG Technology**: Document retrieval + AI generation")
    st.markdown("- **Source Citations**: Answers with page references")
    st.markdown("- **Local Processing**: Documents stay on your computer")
    st.markdown("- **Multiple PDFs**: Search across many documents")
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("- Be specific with your questions for better results")
    st.markdown("- Upload relevant documents before asking questions")

def about_page():
    st.markdown("<h1 class='main-header'>About</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**MedRAG AI - Medical Information Assistant** v1.0.0")
    st.markdown("---")
    st.markdown("A Retrieval-Augmented Generation (RAG) chatbot for searching and understanding medical documents.")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Technology**")
        st.markdown("- Frontend: Streamlit")
        st.markdown("- AI: Ollama (local LLM)")
        st.markdown("- Embeddings: Sentence Transformers")
    with c2:
        st.markdown("**Stack**")
        st.markdown("- Vector DB: ChromaDB")
        st.markdown("- Documents: PyMuPDF")
        st.markdown("- Processing: Local only")
    st.markdown("---")
    st.warning("For educational purposes only. Not medical advice. Always consult a healthcare provider.")
    st.info("All processing happens locally. No data is sent externally.")

def main():
    init()
    sidebar()
    {"chat": chat_page, "documents": docs_page, "settings": settings_page, "help": help_page, "about": about_page}[st.session_state.active_page]()

if __name__ == "__main__":
    main()
