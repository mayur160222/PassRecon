import streamlit as st
import pandas as pd
import numpy as np
from zxcvbn import zxcvbn
from datetime import datetime
import itertools
import base64
import math
import re 

# Set page configuration
st.set_page_config(
    page_title="PassRecon",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --primary: #3498db;
        --secondary: #2c3e50;
        --danger: #e74c3c;
        --success: #2ecc71;
        --warning: #f39c12;
        --dark: #34495e;
        --light: #ecf0f1;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
     body {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
        color: #000000; /* Changed to black for better contrast */
    }
    
    .header {
    text-align: center;
    padding: 30px 0;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: #000000; /* Changed to black */
    border-radius: 15px;
    margin-bottom: 30px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
    
    .header h1 {
        font-size: 3.2rem;
        margin-bottom: 10px;
             text-shadow: 0 1px 3px rgba(255,255,255,0.5);
        font-weight: 800;
    }
    
    .header p {
        font-size: 1.3rem;
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto;
             text-shadow: 0 1px 3px rgba(255,255,255,0.5);
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        color: #000000; /* Added black text color */
    }
    
    .card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transform: translateY(-5px);
    }
    
    .section-title {
        color: #000000; /* Changed to black */
        border-bottom: 3px solid var(--primary);
        padding-bottom: 12px;
        margin-bottom: 20px;
        font-weight: 700;
        font-size: 1.8rem;
    }
    .strength-meter {
        height: 24px;
        background: #ecf0f1;
        border-radius: 12px;
        margin: 20px 0;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .meter-fill {
        height: 100%;
        border-radius: 12px;
        transition: width 0.8s cubic-bezier(0.22, 0.61, 0.36, 1);
    }
    
    .btn {
        background: linear-gradient(135deg, var(--primary) 0%, #1d6fa5 100%);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .btn:hover {
        background: linear-gradient(135deg, #2980b9 0%, #1d6fa5 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .btn-danger {
        background: linear-gradient(135deg, var(--danger) 0%, #c0392b 100%);
    }
    
    .btn-success {
        background: linear-gradient(135deg, var(--success) 0%, #27ae60 100%);
    }
    
    .result-box {
        background: #f8f9fa;
        border-left: 5px solid var(--primary);
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin: 20px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #000000; /* Added black text color */
    }
    .warning {
        color: var(--danger);
        font-weight: 600;
    }
    
    .success {
        color: var(--success);
        font-weight: 600;
    }
    
   .info-box {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border-left: 4px solid var(--primary);
        color: #000000; /* Added black text color */
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 25px;
        color: #7f8c8d;
        font-size: 0.95rem;
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
    }
    
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
        font-size: 16px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2) !important;
    }
    
    .tab-content {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .password-input {
        position: relative;
    }
    
    .password-toggle {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        color: #7f8c8d;
        font-size: 18px;
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        margin-left: 5px;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 250px;
        background-color: var(--dark);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        font-weight: normal;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        color: #000000; /* Added black text color */
    }
    
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #6c757d;
    }
    
    .highlight {
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'wordlist' not in st.session_state:
    st.session_state.wordlist = []
if 'show_password' not in st.session_state:
    st.session_state.show_password = False
if 'generate_policy' not in st.session_state:
    st.session_state.generate_policy = False

# Password Analysis Functions
def analyze_password(password):
    """Analyze password strength using zxcvbn with error handling"""
    if not password:
        return None
    
    try:
        result = zxcvbn(password)
        
        # Safely extract values with fallbacks
        score = result.get('score', 0)
        entropy = result.get('entropy', 0)
        
        crack_time = '?'
        crack_times = result.get('crack_times_display', {})
        if crack_times:
            crack_time = crack_times.get('offline_slow_hashing_1e4_per_second', '?')
        
        feedback = result.get('feedback', {})
        suggestions = feedback.get('suggestions', ['No suggestions available'])
        warnings = feedback.get('warning', '')
        
        # Calculate custom entropy
        char_set = 0
        if re.search(r'[a-z]', password): char_set += 26
        if re.search(r'[A-Z]', password): char_set += 26
        if re.search(r'[0-9]', password): char_set += 10
        if re.search(r'[^a-zA-Z0-9]', password): char_set += 32
        
        custom_entropy = len(password) * math.log2(char_set) if char_set > 0 else 0
        
        return {
            'score': score,
            'entropy': entropy,
            'custom_entropy': custom_entropy,
            'crack_time': crack_time,
            'suggestions': suggestions,
            'warnings': warnings,
            'match_sequence': result.get('sequence', [])
        }
    except Exception as e:
        st.error(f"Password analysis failed: {str(e)}")
        return None

# Wordlist Generation Functions
def apply_leetspeak(word):
    """Apply common leetspeak substitutions"""
    substitutions = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7'],
        'b': ['8'],
        'g': ['9'],
        'l': ['1'],
        'z': ['2']
    }
    
    # Generate all possible leet combinations
    variations = [word]
    for char in word.lower():
        new_variations = []
        for variant in variations:
            if char in substitutions:
                for sub in substitutions[char]:
                    new_variations.append(variant.replace(char, sub, 1))
            else:
                new_variations.append(variant)
        variations = new_variations
    
    return list(set(variations))

def generate_wordlist(base_words, start_year=1900, end_year=None, use_leet=False, add_common=True, add_patterns=True):
    """Generate custom wordlist based on user inputs"""
    if not base_words:
        return []
    
    if end_year is None:
        end_year = datetime.now().year
        
    wordlist = set()
    
    # Add base words
    for word in base_words:
        if word:
            word = word.strip()
            if not word:
                continue
            wordlist.add(word.lower())
            wordlist.add(word.title())
            wordlist.add(word.upper())
    
    # Add years (4-digit and 2-digit)
    years_4d = [str(y) for y in range(start_year, end_year + 1)]
    years_2d = [y[-2:] for y in years_4d]
    
    # Add common number suffixes
    common_nums = ['', '123', '!', '@', '#', '$', '%', '?', '0', '1', '00', '69', '007', '1234', '111', '000'] if add_common else ['']
    
    # Add common patterns
    patterns = []
    if add_patterns:
        patterns = ['', '!', '@', '#', '$', '%', '^', '&', '*', '?', '_', '~']
    
    # Generate combinations
    new_combinations = set()
    
    for word in wordlist.copy():
        # Apply leetspeak
        leet_variations = [word]
        if use_leet:
            leet_variations = apply_leetspeak(word)
        
        # Generate combinations for each variation
        for variation in leet_variations:
            for year in years_4d + years_2d:
                for num in common_nums:
                    for pattern in patterns:
                        # Basic combinations
                        new_combinations.add(variation + year + num + pattern)
                        new_combinations.add(year + variation + num + pattern)
                        new_combinations.add(num + pattern + variation + year)
                        new_combinations.add(variation + num + pattern + year)
                        
                        # Pattern variations
                        new_combinations.add(pattern + variation + year + num)
                        new_combinations.add(variation + pattern + year + num)
    
    # Add new combinations to wordlist
    wordlist |= new_combinations
    
    return sorted(wordlist)

def create_download_link(content, filename="wordlist.txt"):
    """Generate a download link for the wordlist"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a class="btn" href="data:file/txt;base64,{b64}" download="{filename}">Download Wordlist</a>'
    return href

# Header section
st.markdown("""
<div class="header">
    <h1>🔒 PassRecon </h1>
    <p>Analyze password strength & generate custom wordlists for security testing</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different functionality
tab1, tab2, tab3 = st.tabs(["🔐 Password Analysis", "📝 Wordlist Generator", "🛡️ Password Policy"])

with tab1:
    st.markdown("""
    <div class="card">
        <h2 class="section-title">Password Strength Analyzer</h2>
        <p>Test the strength of your passwords using zxcvbn and custom entropy calculations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Analyze Password</h3>
            <p>Enter a password to evaluate its strength:</p>
        """, unsafe_allow_html=True)
        
        # Password input with toggle
        password_container = st.empty()
        password = password_container.text_input("Password:", type="password", key="password_input", 
                                                help="Enter the password you want to analyze")
        
        # Toggle button
        toggle_col, btn_col = st.columns([1, 3])
        with toggle_col:
            if st.button("👁️ Show Password" if not st.session_state.show_password else "👁️ Hide Password"):
                st.session_state.show_password = not st.session_state.show_password
                
        with btn_col:
            analyze_btn = st.button("Analyze Password", key="analyze_btn", use_container_width=True)
        
        # Re-render password field based on toggle state
        if st.session_state.show_password:
            password = password_container.text_input("Password:", value=password, type="default", key="password_visible")
        else:
            password = password_container.text_input("Password:", value=password, type="password", key="password_hidden")
        
        if analyze_btn and password:
            with st.spinner("Analyzing password strength..."):
                result = analyze_password(password)
                
                if result:
                    st.markdown("""
                    <div class="result-box">
                        <h3>🔎 Analysis Results</h3>
                    """, unsafe_allow_html=True)
                    
                    # Strength meter
                    score = result['score']
                    strength_labels = {
                        0: "Very Weak",
                        1: "Weak",
                        2: "Fair",
                        3: "Strong",
                        4: "Very Strong"
                    }
                    
                    colors = {
                        0: "#e74c3c",
                        1: "#e67e22",
                        2: "#f1c40f",
                        3: "#2ecc71",
                        4: "#27ae60"
                    }
                    
                    st.markdown(f"""
                    <div>
                        <h4>Password Strength: <span style="color:{colors[score]}">{strength_labels[score]}</span></h4>
                        <div class="strength-meter">
                            <div class="meter-fill" style="width:{20 + (score*20)}%; background:{colors[score]};"></div>
                        </div>
                        <p>Score: {score}/4</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Entropy and crack time
                    st.markdown(f"""
                    <div style="margin-top: 20px;">
                        <p><strong>zxcvbn Entropy:</strong> {result['entropy']:.2f} bits</p>
                        <p><strong>Custom Entropy:</strong> {result['custom_entropy']:.2f} bits</p>
                        <p><strong>Estimated Crack Time:</strong> <span class="highlight">{result['crack_time']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Warnings
                    if result['warnings']:
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>⚠️ Security Warning</h4>
                            <p class="warning">{result['warnings']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Suggestions
                    if result['suggestions']:
                        st.markdown("""
                        <div style="margin-top: 20px;">
                            <h4>🔧 Suggestions for Improvement</h4>
                        """, unsafe_allow_html=True)
                        
                        for suggestion in result['suggestions']:
                            st.markdown(f"<p>• {suggestion}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("Failed to analyze password. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>💡 Password Security Tips</h3>
            <div class="info-box">
                <h4>Creating Strong Passwords</h4>
                <p>• Use at least 12 characters</p>
                <p>• Combine uppercase, lowercase, numbers, and symbols</p>
                <p>• Avoid dictionary words and personal information</p>
                <p>• Use unique passwords for each account</p>
            </div>
            
            
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="card">
        <h2 class="section-title">Custom Wordlist Generator</h2>
        <p>Create targeted wordlists based on personal information for security testing</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔧 Configure Wordlist</h3>
        """, unsafe_allow_html=True)
        
        base_words = st.text_area(
            "Base Words (comma separated):", 
            "john, mary, fluffy, spot",
            help="Enter words related to the target (names, pets, hobbies, etc.)",
            height=120
        )
        
        base_words_list = [word.strip() for word in base_words.split(',') if word.strip()]
        
        col_year1, col_year2 = st.columns(2)
        with col_year1:
            start_year = st.number_input(
                "Start Year:", 
                min_value=1900, 
                max_value=datetime.now().year,
                value=1980
            )
        with col_year2:
            end_year = st.number_input(
                "End Year:", 
                min_value=1900, 
                max_value=datetime.now().year+10,
                value=datetime.now().year
            )
        
        st.markdown("**Generation Options:**")
        use_leet = st.checkbox("Apply Leetspeak Substitutions (e.g., p@ssw0rd)", value=True)
        add_common = st.checkbox("Add Common Number/Symbol Suffixes (123, !, @, etc.)", value=True)
        add_patterns = st.checkbox("Add Special Character Patterns (!@#$)", value=True)
        
        generate_btn = st.button("Generate Wordlist", key="generate_btn", use_container_width=True)
        
        if generate_btn:
            if not base_words_list:
                st.warning("Please enter at least one base word")
            else:
                with st.spinner("Generating wordlist. This may take a moment..."):
                    st.session_state.wordlist = generate_wordlist(
                        base_words_list,
                        start_year,
                        end_year,
                        use_leet,
                        add_common,
                        add_patterns
                    )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📋 Generated Wordlist</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.wordlist:
            wordlist_size = len(st.session_state.wordlist)
            wordlist_text = "\n".join(st.session_state.wordlist)
            file_size = len(wordlist_text) / (1024 * 1024)  # in MB
            
            st.success(f"✅ Generated {wordlist_size:,} words")
            
            # Stats cards
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.markdown("""
                <div class="stat-card">
                    <div class="stat-value">{:,}</div>
                    <div class="stat-label">Total Words</div>
                </div>
                """.format(wordlist_size), unsafe_allow_html=True)
                
            with col_stat2:
                st.markdown("""
                <div class="stat-card">
                    <div class="stat-value">{:.2f}</div>
                    <div class="stat-label">File Size (MB)</div>
                </div>
                """.format(file_size), unsafe_allow_html=True)
                
            with col_stat3:
                st.markdown("""
                <div class="stat-card">
                    <div class="stat-value">{}</div>
                    <div class="stat-label">Years Included</div>
                </div>
                """.format(end_year - start_year + 1), unsafe_allow_html=True)
            
            # Show sample of the wordlist
            st.markdown("**Sample of generated words (first 50):**")
            sample_size = min(50, len(st.session_state.wordlist))
            sample_df = pd.DataFrame({
                "Word": st.session_state.wordlist[:sample_size]
            })
            st.dataframe(sample_df, height=300, use_container_width=True)
            
            # Download button
            st.markdown(create_download_link(wordlist_text, "custom_wordlist.txt"), unsafe_allow_html=True)
            
        else:
            st.info("Generate a wordlist to see results here")
            st.markdown("""
            <div class="info-box">
                <h4>Wordlist Generation Tips</h4>
                <p>• Include personal details: names, pets, hobbies</p>
                <p>• Add birth years and other significant dates</p>
                <p>• Enable leetspeak for common substitutions</p>
                <p>• Use common suffixes like 123, !, and 007</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
with tab3:
    st.markdown("""
    <div class="card">
        <h2 class="section-title">Password Policy Generator</h2>
        <p>Create custom password policies and generate regex patterns for validation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔧 Policy Configuration</h3>
            <p>Set your password requirements:</p>
        """, unsafe_allow_html=True)
        
        min_length = st.slider("Minimum Length", 6, 20, 8, help="Minimum number of characters required")
        max_length = st.slider("Maximum Length", min_length, 30, 20, help="Maximum allowed characters")
        require_upper = st.checkbox("Require Uppercase Letters (A-Z)", True)
        require_lower = st.checkbox("Require Lowercase Letters (a-z)", True)
        require_digits = st.checkbox("Require Digits (0-9)", True)
        require_symbols = st.checkbox("Require Symbols (!@#$%^&*)", True)
        consecutive_chars = st.checkbox("Prevent Consecutive Identical Characters", True)
        sequential_chars = st.checkbox("Prevent Sequential Characters (abc, 123)", True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate policy button
        if st.button("Generate Password Policy", key="policy_btn", use_container_width=True):
            st.session_state.generate_policy = True
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📋 Generated Policy</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.generate_policy:
            # Generate regex pattern based on requirements
            regex_parts = []
            lookaheads = []
            
            # Length requirement
            regex_parts.append(f".{{{min_length},{max_length}}}")
            
            # Character type requirements
            if require_upper:
                lookaheads.append("(?=.*[A-Z])")
            if require_lower:
                lookaheads.append("(?=.*[a-z])")
            if require_digits:
                lookaheads.append("(?=.*\\d)")
            if require_symbols:
                lookaheads.append("(?=.*[!@#$%^&*])")
            
            # Combine lookaheads
            regex = f"^{''.join(lookaheads)}{''.join(regex_parts)}$"
            
            # Additional constraints
            constraints = []
            if consecutive_chars:
                constraints.append("• No consecutive identical characters")
                regex = regex[:-1] + "(?!.*(.)\\1)" + regex[-1]
            if sequential_chars:
                constraints.append("• No sequential characters (abc, 123)")
                regex = regex[:-1] + "(?!.*(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890))" + regex[-1]
            
            # Display results
            st.markdown("""
            <div class="result-box">
                <h4>🔐 Your Password Policy</h4>
                <p><strong>Password must meet these requirements:</strong></p>
                <ul>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<li>• Length: {min_length} to {max_length} characters</li>", unsafe_allow_html=True)
            if require_upper:
                st.markdown("<li>• At least one uppercase letter (A-Z)</li>", unsafe_allow_html=True)
            if require_lower:
                st.markdown("<li>• At least one lowercase letter (a-z)</li>", unsafe_allow_html=True)
            if require_digits:
                st.markdown("<li>• At least one digit (0-9)</li>", unsafe_allow_html=True)
            if require_symbols:
                st.markdown("<li>• At least one symbol (!@#$%^&*)</li>", unsafe_allow_html=True)
            for constraint in constraints:
                st.markdown(f"<li>{constraint}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul>", unsafe_allow_html=True)
            
            # Display regex pattern
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <h4>🔍 Validation Regex Pattern</h4>
                <div style="background: #f8f9fa,"color: #000000; padding: 15px; border-radius: 8px; font-family: monospace; word-wrap: break-word;">
                    {regex}
                </div>
                <p style="margin-top: 10px; font-size: 0.9em;"><em>Use this regex pattern to validate passwords in your applications</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Configure your password requirements and click 'Generate Password Policy'")
            st.markdown("""
            <div class="info-box">
                <h4>Password Policy Tips</h4>
                <p>• Longer passwords are more secure (12+ characters recommended)</p>
                <p>• Require multiple character types for better security</p>
                <p>• Consider preventing common patterns like sequences</p>
                <p>• NIST recommends focusing on length rather than complexity</p>
            </div>
            
            <div class="info-box">
                <h4>Using the Regex Pattern</h4>
                <p>• Copy the generated regex pattern</p>
                <p>• Use it in your code for password validation</p>
                <p>• Test with various passwords to ensure it works as expected</p>
                <p>• Adjust requirements as needed for your security needs</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Password Toolkit v1.1 | Created with Streamlit | For educational and security testing purposes only</p>
    <p>Always obtain proper authorization before testing systems. Never use this tool for unauthorized access.</p>
</div>
""", unsafe_allow_html=True)