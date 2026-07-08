import sys
import os
import streamlit as st

# Explicitly add the root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.compiler import PromptCompiler
from llm.gateway import LLMGateway

# Set up page styling and config
st.set_page_config(
    page_title="ContextLint UI",
    page_icon="⚡",
    layout="wide"
)

# --- CUSTOM CSS FOR GLASSMORPHISM & DARK VIBE ---
st.markdown("""
<style>
    /* Main Background Gradient */
    .stApp {
        background: radial-gradient(circle at top, #1a1c23 0%, #0E1117 80%);
    }
    
    /* Glassmorphism for Text Areas and Inputs */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        color: #00FF41 !important; /* Terminal Green */
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    
    /* Glassmorphism for File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border: 1px dashed #00FF41 !important;
        background: rgba(0, 255, 65, 0.05) !important;
    }

    /* Primary Action Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #00FF41 0%, #008F11 100%) !important;
        color: #000000 !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4) !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.6) !important;
    }
    
    /* Metrics Box Glassmorphism */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ ContextLint")
st.caption("The developer tool for stripping bloat and compiling structured LLM prompts.")

# Initialize persistent state variables
if "optimized_prompt" not in st.session_state:
    st.session_state.optimized_prompt = ""
if "metrics" not in st.session_state:
    st.session_state.metrics = None

# Layout splits
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📥 Input Context")
    
    vague_prompt = st.text_area(
        "Define your goal:",
        placeholder="> e.g., Refactor this component to use React hooks...",
        height=150
    )
    
    uploaded_files = st.file_uploader(
        "Drop context files here (code, logs, configs)",
        accept_multiple_files=True
    )
    
    compile_btn = st.button("COMPILE PROMPT", type="primary", use_container_width=True)

if compile_btn:
    if not vague_prompt:
        st.error("Missing input: Please define your goal.")
    else:
        with st.spinner("Compiling context and querying LLM Gateway..."):
            temp_paths = []
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    temp_paths.append(temp_path)
            
            try:
                compiler = PromptCompiler()
                compiled_payload = compiler.compile(vague_prompt=vague_prompt, file_paths=temp_paths)
                
                gateway = LLMGateway(provider="gemini")
                final_markdown = gateway.generate_optimized_prompt(compiled_payload)
                
                st.session_state.optimized_prompt = final_markdown
                st.session_state.metrics = compiled_payload["metrics"]
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
            finally:
                for path in temp_paths:
                    if os.path.exists(path):
                        os.remove(path)

with col_right:
    st.subheader("📤 Output")
    
    if st.session_state.metrics:
        m = st.session_state.metrics
        st.metric(
            label="Tokens Sent to Gateway", 
            value=m['compiled_payload_tokens'], 
            delta=f"Base Input: {m['raw_input_tokens']} tokens",
            delta_color="off"
        )
        
    if st.session_state.optimized_prompt:
        st.text_area(
            "Compiled Markdown (Ready to Copy):",
            value=st.session_state.optimized_prompt,
            height=400
        )
    else:
        st.info("Awaiting compilation. Input context and execute.")