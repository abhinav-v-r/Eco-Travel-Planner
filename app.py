"""
Eco-Travel AI Planner
A Carbon Footprint & Sustainable Travel Calculator powered by Google Gemini AI
"""

import streamlit as st
import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables using absolute path
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path, override=True)

# =============================================================================
# CONFIGURATION
# =============================================================================
# The API key is loaded from the .env file for security.
# Copy .env.example to .env and add your key there.
API_KEY = os.getenv("GOOGLE_API_KEY")

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Eco-Travel Planner",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CUSTOM STYLING
# =============================================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #0f4c3a 0%, #1a7f5a 50%, #2ecc71 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(46, 204, 113, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Input Card Styling */
    .input-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 204, 113, 0.2);
        margin-bottom: 1.5rem;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f0fff4);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 4px solid #2ecc71;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(46, 204, 113, 0.15);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f4c3a;
    }
    
    .metric-unit {
        font-size: 1rem;
        color: #888;
        font-weight: 400;
    }
    
    /* Transport Cards */
    .transport-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .transport-card.recommended {
        border-color: #2ecc71;
        background: linear-gradient(145deg, #f0fff4, #ffffff);
        box-shadow: 0 4px 20px rgba(46, 204, 113, 0.2);
    }
    
    .transport-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .transport-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .transport-emission {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f4c3a;
    }
    
    /* Eco Fact Box */
    .eco-fact {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #4caf50;
        margin-top: 1.5rem;
    }
    
    .eco-fact-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2e7d32;
        margin-bottom: 0.5rem;
    }
    
    .eco-fact-text {
        color: #1b5e20;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin-top: 2rem;
        font-size: 0.85rem;
        color: #e65100;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a7f5a 0%, #2ecc71 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
    }
    
    /* Savings Badge */
    .savings-badge {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2ecc71;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# AI PROMPT ENGINEERING
# =============================================================================
def create_eco_prompt(origin: str, destination: str, travelers: int) -> str:
    """
    Creates a strictly structured prompt for the AI to calculate carbon footprint.
    Uses standard emission factors to prevent hallucination.
    """
    system_prompt = f"""You are an expert environmental scientist specializing in transportation carbon footprint analysis.

TASK: Calculate the carbon footprint for travel from {origin} to {destination} for {travelers} traveler(s).

STANDARD EMISSION FACTORS (use these exact values):
- Personal Car (Petrol): 0.19 kg CO2 per km per vehicle (divide by average 2 passengers if carpooling)
- Public Bus: 0.089 kg CO2 per km per passenger
- Electric Vehicle: 0.05 kg CO2 per km per vehicle
- Train: 0.041 kg CO2 per km per passenger

INSTRUCTIONS:
1. Estimate the road/rail distance between the two cities in kilometers. Use realistic distances.
2. Calculate CO2 emissions for each transport mode for ALL {travelers} traveler(s).
3. For Car and EV: Assume all travelers share one vehicle. Multiply distance by emission factor.
4. For Bus and Train: Multiply distance by emission factor by number of travelers.
5. Recommend the most eco-friendly option.
6. Provide a fun, educational eco-fact related to this journey or region.

CRITICAL: Return your response ONLY as a valid JSON object with this exact structure:
{{
    "origin": "{origin}",
    "destination": "{destination}",
    "travelers": {travelers},
    "distance_km": <number>,
    "emissions": {{
        "car": <number in kg>,
        "bus": <number in kg>,
        "ev": <number in kg>,
        "train": <number in kg>
    }},
    "recommendation": "<transport mode name>",
    "recommendation_reason": "<brief explanation>",
    "eco_fact": "<fun educational fact about eco-travel or the region>",
    "car_vs_train_savings": <number in kg - how much CO2 saved by taking train instead of car>
}}

Return ONLY the JSON object, no additional text or markdown formatting."""

    return system_prompt


def query_gemini(prompt: str) -> dict:
    """
    Sends a prompt to Google Gemini and returns the parsed response.
    Includes dynamic model discovery to prevent 404 errors.
    """
    try:
        genai.configure(api_key=API_KEY)
        
        # 1. Dynamically discover models supported by your API key
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except Exception as e:
            st.error(f"Failed to list models: {e}")
            return None

        if not available_models:
            st.error("No models found that support content generation for this API key.")
            return None

        # 2. Prioritize "Flash" models as they are faster, then Pro
        def get_priority(name):
            if 'flash-2.0' in name.lower() or '2.0-flash' in name.lower(): return 0
            if 'flash' in name.lower(): return 1
            if 'pro' in name.lower(): return 2
            return 3

        sorted_models = sorted(available_models, key=get_priority)
        
        # 3. Try top 5 best matching models
        response = None
        last_error = None
        
        for model_full_name in sorted_models[:8]: # Try more models to find one with quota
            # Try both 'models/name' and just 'name'
            short_name = model_full_name.replace('models/', '')
            for target_name in [model_full_name, short_name]:
                try:
                    model = genai.GenerativeModel(target_name)
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.1,
                            max_output_tokens=2048,
                            response_mime_type="application/json"
                        )
                    )
                    if response: break
                except Exception as e:
                    err_text = str(e).lower()
                    if "429" in err_text or "quota" in err_text:
                        # If quota exceeded, skip this model and try next one
                        last_error = e
                        continue 
                    elif "404" in err_text:
                        continue # Try short/long name alternative
                    else:
                        last_error = e
                        continue
            if response: break
        
        if not response:
            # Diagnostic: List models if all attempts fail
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.error(f"Could not connect to preferred models. Your API key has access to: {', '.join(available_models)}")
            except:
                pass
            raise last_error if last_error else ValueError("Failed to get response from any model")
            
        # Extract JSON from response
        response_text = response.text.strip()
        
        def repair_json(text):
            """Attempts to fix common AI JSON formatting issues."""
            # 1. Basic cleaning
            t = text.strip()
            # 2. Fix unescaped quotes inside JSON strings (common cause of 'Unterminated string')
            # Look for double quotes that aren't preceding a colon or following a comma/brace
            # This is a bit complex for regex, so we'll try basic closing instead first
            
            # 3. Fix truncated JSON (missing closing braces)
            open_braces = t.count('{')
            close_braces = t.count('}')
            if open_braces > close_braces:
                t += '}' * (open_braces - close_braces)
            
            return t

        try:
            # First attempt: find JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
            else:
                json_str = response_text
                
            return json.loads(repair_json(json_str))
        except json.JSONDecodeError:
            # Second attempt: more aggressive cleaning
            cleaned = re.sub(r',\s*([\]}])', r'\1', response_text) # Trailing commas
            return json.loads(repair_json(cleaned))
            
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            st.error("Model Not Found (404). This usually means the model name or API version is incorrect for your region/key.")
        else:
            st.error(f"AI Error: {error_msg}")
        return None


# =============================================================================
# UI COMPONENTS
# =============================================================================
def render_header():
    """Renders the main header section."""
    st.markdown("""
    <div class="main-header">
        <h1>🌿 Eco-Travel Planner</h1>
        <p>Calculate your carbon footprint & discover sustainable travel options</p>
    </div>
    """, unsafe_allow_html=True)


def render_transport_card(icon: str, name: str, emission: float, is_recommended: bool = False):
    """Renders a transport mode card with emission data."""
    recommended_class = "recommended" if is_recommended else ""
    badge = '<span class="savings-badge">🏆 Best Choice</span>' if is_recommended else ""
    
    return f"""
    <div class="transport-card {recommended_class}">
        <div class="transport-icon">{icon}</div>
        <div class="transport-name">{name}</div>
        <div class="transport-emission">{emission:.1f} <span class="metric-unit">kg CO₂</span></div>
        {badge}
    </div>
    """


def render_results(data: dict):
    """Renders the calculation results in a visually appealing format."""
    
    st.markdown("---")
    st.markdown("## 📊 Your Travel Carbon Footprint")
    
    # Distance and Journey Info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📍 Distance</div>
            <div class="metric-value">{data['distance_km']:,.0f} <span class="metric-unit">km</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">👥 Travelers</div>
            <div class="metric-value">{data['travelers']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        savings = data.get('car_vs_train_savings', 
                          data['emissions']['car'] - data['emissions']['train'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🌱 Potential Savings</div>
            <div class="metric-value">{savings:.1f} <span class="metric-unit">kg CO₂</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Transport Options
    st.markdown("### 🚗 Transport Options Comparison")
    
    emissions = data['emissions']
    recommended = data['recommendation'].lower()
    
    transport_config = [
        ("🚗", "Personal Car", emissions['car'], 'car'),
        ("🚌", "Public Bus", emissions['bus'], 'bus'),
        ("⚡", "Electric Vehicle", emissions['ev'], 'ev'),
        ("🚂", "Train", emissions['train'], 'train')
    ]
    
    cols = st.columns(4)
    for i, (icon, name, emission, key) in enumerate(transport_config):
        is_rec = key in recommended or recommended in key.lower() or recommended in name.lower()
        with cols[i]:
            st.markdown(
                render_transport_card(icon, name, emission, is_rec),
                unsafe_allow_html=True
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendation
    st.success(f"🎯 **Recommendation:** {data['recommendation']} — {data.get('recommendation_reason', 'The most sustainable choice for your journey!')}")
    
    # Eco Fact
    st.markdown(f"""
    <div class="eco-fact">
        <div class="eco-fact-title">🌍 Did You Know?</div>
        <div class="eco-fact-text">{data['eco_fact']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsible AI Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Disclaimer:</strong> Estimates are generated by AI for awareness purposes and may vary from actual values. 
        Calculations are based on average emission factors and do not account for specific vehicle efficiency, 
        occupancy rates, or route conditions.
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    render_header()
    
    # Check API Key
    if not API_KEY:
        st.warning("⚠️ Google API Key not found!")
        st.info("""
        **To set up your API Key:**
        1. Create a `.env` file in the project folder.
        2. Add `GOOGLE_API_KEY=your_key_here` to it.
        3. Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
        """)
        st.stop()
    
    # Input Section
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Plan Your Journey")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        origin = st.text_input(
            "🚀 Origin City",
            placeholder="e.g., Bangalore",
            help="Enter your starting city"
        )
    
    with col2:
        destination = st.text_input(
            "📍 Destination City",
            placeholder="e.g., Mysore",
            help="Enter your destination city"
        )
    
    with col3:
        travelers = st.number_input(
            "👥 Travelers",
            min_value=1,
            max_value=50,
            value=1,
            help="Number of people traveling"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        calculate_btn = st.button(
            "🌿 Calculate Sustainability",
            use_container_width=True,
            type="primary"
        )
    
    # Process Request
    if calculate_btn:
        if not origin or not destination:
            st.error("Please enter both origin and destination cities.")
            return
        
        with st.spinner("🌍 Analyzing your eco-friendly travel options..."):
            prompt = create_eco_prompt(origin, destination, travelers)
            result = query_gemini(prompt)
            
            if result:
                render_results(result)
            else:
                st.error("Failed to calculate. Please check your API key and try again.")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
        "Built with 💚 for a sustainable future | Powered by Google Gemini AI"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
