import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="PhoneHub - AI Phone Recommendations",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for immersive dark mode with neon effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(90deg, #00f5ff 0%, #0080ff 50%, #8000ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 245, 255, 0.5); }
        to { text-shadow: 0 0 30px rgba(0, 245, 255, 0.8), 0 0 40px rgba(128, 0, 255, 0.3); }
    }
    
    /* Subtitle */
    .subtitle {
        color: #a0a0a0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Neon cards */
    .neon-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .neon-card:hover {
        border-color: rgba(0, 245, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.2);
        transform: translateY(-5px);
    }
    
    /* Phone cards */
    .phone-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .phone-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .phone-card:hover::before {
        left: 100%;
    }
    
    .phone-card:hover {
        border-color: rgba(0, 245, 255, 0.6);
        box-shadow: 0 15px 40px rgba(0, 245, 255, 0.2);
        transform: translateY(-8px);
    }
    
    /* Phone name styling */
    .phone-name {
        color: #00f5ff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
    }
    
    /* Phone details */
    .phone-details {
        color: #e0e0e0;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Price styling */
    .price {
        color: #00ff88;
        font-size: 1.3rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }
    
    /* Explanation box */
    .explanation {
        background: rgba(0, 245, 255, 0.1);
        border-left: 4px solid #00f5ff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        color: #e0e0e0;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00f5ff 0%, #0080ff 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 245, 255, 0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: rgba(0, 245, 255, 0.2);
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 245, 255, 0.5);
        box-shadow: 0 5px 20px rgba(0, 245, 255, 0.2);
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    .loading::after {
        content: '';
        width: 40px;
        height: 40px;
        border: 4px solid rgba(0, 245, 255, 0.3);
        border-top: 4px solid #00f5ff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .phone-card {
            padding: 1rem;
        }
        
        .phone-name {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Phone database
@st.cache_data
def load_phone_data():
    phones = [
        {
            "name": "iPhone 15 Pro Max",
            "price": 1199,
            "camera": 95,
            "battery": 90,
            "performance": 98,
            "display": 95,
            "brand": "Apple",
            "category": "Flagship",
            "storage": "256GB",
            "ram": "8GB",
            "screen_size": "6.7\"",
            "camera_mp": "48MP",
            "battery_mah": "4441mAh",
            "os": "iOS 17",
            "features": ["A17 Pro chip", "Titanium design", "Action Button", "USB-C"],
            "pros": ["Exceptional performance", "Premium build quality", "Excellent camera system"],
            "cons": ["Very expensive", "No always-on display customization"]
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "price": 1299,
            "camera": 96,
            "battery": 88,
            "performance": 95,
            "display": 98,
            "brand": "Samsung",
            "category": "Flagship",
            "storage": "256GB",
            "ram": "12GB",
            "screen_size": "6.8\"",
            "camera_mp": "200MP",
            "battery_mah": "5000mAh",
            "os": "Android 14",
            "features": ["S Pen included", "200MP camera", "AI features", "Titanium frame"],
            "pros": ["S Pen functionality", "Incredible camera zoom", "Large display"],
            "cons": ["Expensive", "Large size may not suit everyone"]
        },
        {
            "name": "Google Pixel 8 Pro",
            "price": 999,
            "camera": 93,
            "battery": 85,
            "performance": 88,
            "display": 92,
            "brand": "Google",
            "category": "Flagship",
            "storage": "128GB",
            "ram": "12GB",
            "screen_size": "6.7\"",
            "camera_mp": "50MP",
            "battery_mah": "5050mAh",
            "os": "Android 14",
            "features": ["AI-powered photography", "Magic Eraser", "Pure Android", "7 years updates"],
            "pros": ["Best AI photography", "Clean Android experience", "Long software support"],
            "cons": ["Tensor chip heating", "Limited availability"]
        },
        {
            "name": "OnePlus 12",
            "price": 799,
            "camera": 88,
            "battery": 92,
            "performance": 94,
            "display": 93,
            "brand": "OnePlus",
            "category": "Premium",
            "storage": "256GB",
            "ram": "12GB",
            "screen_size": "6.82\"",
            "camera_mp": "50MP",
            "battery_mah": "5400mAh",
            "os": "Android 14",
            "features": ["100W fast charging", "Hasselblad cameras", "120Hz display", "Alert slider"],
            "pros": ["Extremely fast charging", "Great performance", "Competitive pricing"],
            "cons": ["Software updates slower", "Not waterproof rating"]
        },
        {
            "name": "Xiaomi 14 Ultra",
            "price": 1099,
            "camera": 94,
            "battery": 87,
            "performance": 93,
            "display": 91,
            "brand": "Xiaomi",
            "category": "Flagship",
            "storage": "512GB",
            "ram": "16GB",
            "screen_size": "6.73\"",
            "camera_mp": "50MP",
            "battery_mah": "5300mAh",
            "os": "Android 14",
            "features": ["Leica partnership", "Photography kit", "Wireless charging", "IP68 rating"],
            "pros": ["Exceptional camera quality", "High RAM", "Photography-focused"],
            "cons": ["MIUI can be overwhelming", "Limited availability"]
        },
        {
            "name": "Nothing Phone 2",
            "price": 599,
            "camera": 82,
            "battery": 86,
            "performance": 85,
            "display": 88,
            "brand": "Nothing",
            "category": "Mid-range",
            "storage": "256GB",
            "ram": "8GB",
            "screen_size": "6.7\"",
            "camera_mp": "50MP",
            "battery_mah": "4700mAh",
            "os": "Android 14",
            "features": ["Glyph interface", "Transparent design", "Wireless charging", "Clean UI"],
            "pros": ["Unique design", "Great value", "Clean software"],
            "cons": ["Limited availability", "Camera could be better"]
        },
        {
            "name": "iPhone 15",
            "price": 799,
            "camera": 89,
            "battery": 85,
            "performance": 92,
            "display": 90,
            "brand": "Apple",
            "category": "Premium",
            "storage": "128GB",
            "ram": "6GB",
            "screen_size": "6.1\"",
            "camera_mp": "48MP",
            "battery_mah": "3349mAh",
            "os": "iOS 17",
            "features": ["A16 Bionic chip", "Dynamic Island", "USB-C", "Ceramic Shield"],
            "pros": ["Solid performance", "Good camera", "iOS ecosystem"],
            "cons": ["Base storage too low", "No 120Hz display"]
        },
        {
            "name": "Samsung Galaxy A54",
            "price": 449,
            "camera": 78,
            "battery": 88,
            "performance": 75,
            "display": 85,
            "brand": "Samsung",
            "category": "Mid-range",
            "storage": "128GB",
            "ram": "8GB",
            "screen_size": "6.4\"",
            "camera_mp": "50MP",
            "battery_mah": "5000mAh",
            "os": "Android 14",
            "features": ["120Hz AMOLED", "IP67 rating", "Stereo speakers", "Expandable storage"],
            "pros": ["Great display", "Good battery life", "Affordable"],
            "cons": ["Mediocre performance", "Plastic build"]
        },
        {
            "name": "Realme GT 5 Pro",
            "price": 699,
            "camera": 85,
            "battery": 90,
            "performance": 91,
            "display": 89,
            "brand": "Realme",
            "category": "Premium",
            "storage": "256GB",
            "ram": "12GB",
            "screen_size": "6.78\"",
            "camera_mp": "50MP",
            "battery_mah": "5400mAh",
            "os": "Android 14",
            "features": ["150W fast charging", "Periscope zoom", "Curved display", "Gaming mode"],
            "pros": ["Ultra-fast charging", "Great gaming performance", "Competitive price"],
            "cons": ["Software updates inconsistent", "Build quality concerns"]
        },
        {
            "name": "Motorola Edge 50 Pro",
            "price": 549,
            "camera": 83,
            "battery": 89,
            "performance": 80,
            "display": 87,
            "brand": "Motorola",
            "category": "Mid-range",
            "storage": "256GB",
            "ram": "12GB",
            "screen_size": "6.7\"",
            "camera_mp": "50MP",
            "battery_mah": "4500mAh",
            "os": "Android 14",
            "features": ["Curved OLED", "Wireless charging", "Near-stock Android", "IP68 rating"],
            "pros": ["Clean Android experience", "Good build quality", "Reasonable price"],
            "cons": ["Average camera", "Limited software support"]
        }
    ]
    return pd.DataFrame(phones)

# Recommendation engine
def get_recommendations(df, budget, primary_use, brand_pref=None, min_camera=0, min_battery=0):
    filtered_df = df[df['price'] <= budget].copy()
    
    if brand_pref and brand_pref != "Any":
        filtered_df = filtered_df[filtered_df['brand'] == brand_pref]
    
    if min_camera > 0:
        filtered_df = filtered_df[filtered_df['camera'] >= min_camera]
    
    if min_battery > 0:
        filtered_df = filtered_df[filtered_df['battery'] >= min_battery]
    
    # Scoring based on primary use
    if primary_use == "Photography":
        filtered_df['score'] = (filtered_df['camera'] * 0.5 + 
                               filtered_df['display'] * 0.3 + 
                               filtered_df['performance'] * 0.2)
    elif primary_use == "Gaming":
        filtered_df['score'] = (filtered_df['performance'] * 0.5 + 
                               filtered_df['display'] * 0.3 + 
                               filtered_df['battery'] * 0.2)
    elif primary_use == "Battery Life":
        filtered_df['score'] = (filtered_df['battery'] * 0.5 + 
                               filtered_df['performance'] * 0.3 + 
                               filtered_df['camera'] * 0.2)
    else:  # General Use
        filtered_df['score'] = (filtered_df['performance'] * 0.3 + 
                               filtered_df['camera'] * 0.25 + 
                               filtered_df['battery'] * 0.25 + 
                               filtered_df['display'] * 0.2)
    
    return filtered_df.sort_values('score', ascending=False)

def generate_explanation(phone, primary_use, budget):
    explanations = []
    
    if primary_use == "Photography":
        if phone['camera'] >= 90:
            explanations.append(f"📸 Exceptional camera quality ({phone['camera']}/100) perfect for photography enthusiasts")
        elif phone['camera'] >= 80:
            explanations.append(f"📸 Very good camera ({phone['camera']}/100) suitable for most photography needs")
    
    elif primary_use == "Gaming":
        if phone['performance'] >= 90:
            explanations.append(f"🎮 Top-tier performance ({phone['performance']}/100) handles any game smoothly")
        elif phone['performance'] >= 80:
            explanations.append(f"🎮 Good gaming performance ({phone['performance']}/100) for most mobile games")
    
    elif primary_use == "Battery Life":
        if phone['battery'] >= 85:
            explanations.append(f"🔋 Excellent battery life ({phone['battery']}/100) for all-day usage")
        elif phone['battery'] >= 75:
            explanations.append(f"🔋 Good battery life ({phone['battery']}/100) for regular usage")
    
    if phone['price'] <= budget * 0.8:
        explanations.append(f"💰 Great value at ${phone['price']} - well within your ${budget} budget")
    elif phone['price'] <= budget * 0.9:
        explanations.append(f"💰 Good value at ${phone['price']} for the features offered")
    
    if len(phone['features']) > 0:
        explanations.append(f"✨ Key features: {', '.join(phone['features'][:3])}")
    
    return explanations

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">📱 PhoneHub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Phone Recommendations Tailored Just for You</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_phone_data()
    
    # Sidebar filters
    st.sidebar.markdown("## 🎯 Find Your Perfect Phone")
    
    budget = st.sidebar.slider("💰 Budget (USD)", 300, 1500, 800, 50)
    primary_use = st.sidebar.selectbox("🎯 Primary Use", 
                                      ["General Use", "Photography", "Gaming", "Battery Life"])
    brand_pref = st.sidebar.selectbox("📱 Brand Preference", 
                                     ["Any"] + sorted(df['brand'].unique().tolist()))
    
    st.sidebar.markdown("### Advanced Filters")
    min_camera = st.sidebar.slider("📸 Minimum Camera Score", 0, 100, 0, 5)
    min_battery = st.sidebar.slider("🔋 Minimum Battery Score", 0, 100, 0, 5)
    
    # Store filters in session state for use in focus_on_selected_phone
    st.session_state['budget'] = budget
    st.session_state['primary_use'] = primary_use
    st.session_state['brand_pref'] = brand_pref
    st.session_state['min_camera'] = min_camera
    st.session_state['min_battery'] = min_battery
    
    # Show recently viewed phones in sidebar
    show_recently_viewed(df)
    
    # Get recommendations
    recommendations = get_recommendations(df, budget, primary_use, brand_pref, min_camera, min_battery)
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">💰</h3>
            <p style="color: white; margin: 0;">Budget</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">${budget}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">🎯</h3>
            <p style="color: white; margin: 0;">Primary Use</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{primary_use}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">📱</h3>
            <p style="color: white; margin: 0;">Brand</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{brand_pref}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">📊</h3>
            <p style="color: white; margin: 0;">Found</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{len(recommendations)} phones</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Focus on selected phone if set
    focus_on_selected_phone(df)
    
    if len(recommendations) == 0:
        st.markdown("""
        <div class="neon-card">
            <h3 style="color: #ff6b6b; text-align: center;">No phones found matching your criteria</h3>
            <p style="color: #a0a0a0; text-align: center;">Try adjusting your filters or increasing your budget</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display recommendations
    st.markdown("## 🏆 Recommended Phones")
    
    for idx, (_, phone) in enumerate(recommendations.head(5).iterrows()):
        explanations = generate_explanation(phone, primary_use, budget)
        # Add to recently viewed
        add_recently_viewed(phone['name'])
        # Create radar chart for phone specs
        categories = ['Camera', 'Battery', 'Performance', 'Display']
        values = [phone['camera'], phone['battery'], phone['performance'], phone['display']]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=phone['name'],
            line=dict(color='#00f5ff', width=2),
            fillcolor='rgba(0, 245, 255, 0.2)'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    color='white'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    color='white'
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            height=300
        )
        col1, col2 = st.columns([2, 1])
        with col1:
            rank_badge = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx+1}"
            st.markdown(f"""
            <div class="phone-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{rank_badge}</span>
                        <span class="phone-name">{phone['name']}</span>
                    </div>
                    <span class="price">${phone['price']}</span>
                </div>
                <div class="phone-details">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                        <div>📱 <strong>{phone['screen_size']}</strong></div>
                        <div>💾 <strong>{phone['storage']}</strong></div>
                        <div>🧠 <strong>{phone['ram']}</strong></div>
                        <div>📸 <strong>{phone['camera_mp']}</strong></div>
                        <div>🔋 <strong>{phone['battery_mah']}</strong></div>
                        <div>🤖 <strong>{phone['os']}</strong></div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <strong style="color: #00f5ff;">✨ Key Features:</strong><br>
                        {' • '.join(phone['features'])}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <strong style="color: #00ff88;">👍 Pros:</strong><br>
                            {'<br>'.join(['• ' + pro for pro in phone['pros']])}
                        </div>
                        <div>
                            <strong style="color: #ff6b6b;">👎 Cons:</strong><br>
                            {'<br>'.join(['• ' + con for con in phone['cons']])}
                        </div>
                    </div>
                </div>
                <div class="explanation">
                    <strong>🤖 Why this phone is perfect for you:</strong><br>
                    {'<br>'.join(['• ' + exp for exp in explanations])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.plotly_chart(fig, use_container_width=True)
    
    # Add filter summary
    add_filter_summary(budget, primary_use, brand_pref, min_camera, min_battery)
    # Add comparison section
    add_comparison_section(recommendations)
    # Add search functionality
    add_search_functionality(df)
    # Export functionality
    export_recommendations(recommendations)
    # Add feedback section
    st.markdown("## 💬 Feedback")
    col1, col2 = st.columns(2)
    with col1:
        rating = st.select_slider(
            "How helpful were these recommendations?",
            options=['😞 Not helpful', '😐 Somewhat helpful', '😊 Very helpful', '🤩 Extremely helpful'],
            value='😊 Very helpful'
        )
    with col2:
        feedback = st.text_area("Any additional feedback or suggestions?", height=100)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback! It helps us improve our recommendations.")
    # Analytics section
    st.markdown("## 📊 Market Analysis")
    col1, col2 = st.columns(2)
    with col1:
        fig_scatter = px.scatter(
            df, x='price', y='performance', 
            color='brand', size='camera',
            hover_data=['name', 'battery', 'display'],
            title="Price vs Performance Analysis"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(color='#00f5ff', size=16)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col2:
        brand_counts = df['brand'].value_counts()
        fig_pie = px.pie(
            values=brand_counts.values, 
            names=brand_counts.index,
            title="Brand Distribution"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(color='#00f5ff', size=16)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0a0a0; padding: 2rem;">
        <p>🚀 Built with Streamlit • Powered by AI • Made with 💙 for tech enthusiasts</p>
        <p>© 2024 PhoneHub - Your Ultimate Phone Recommendation Assistant</p>
    </div>
    """, unsafe_allow_html=True)

# Additional features and improvements for PhoneHub

# Add after the main function, before if __name__ == "__main__":

def create_comparison_table(phones_df):
    """Create a detailed comparison table for selected phones"""
    if len(phones_df) == 0:
        return None
    
    comparison_data = []
    for _, phone in phones_df.iterrows():
        comparison_data.append({
            'Phone': phone['name'],
            'Price': f"${phone['price']}",
            'Camera Score': f"{phone['camera']}/100",
            'Battery Score': f"{phone['battery']}/100",
            'Performance': f"{phone['performance']}/100",
            'Display': f"{phone['display']}/100",
            'Storage': phone['storage'],
            'RAM': phone['ram'],
            'Screen Size': phone['screen_size'],
            'Overall Score': f"{phone['score']:.1f}/100" if 'score' in phone else "N/A"
        })
    
    return pd.DataFrame(comparison_data)

def add_comparison_section(recommendations):
    """Add a comparison section for top phones"""
    if len(recommendations) > 1:
        st.markdown("## 🔍 Detailed Comparison")
        
        # Allow user to select phones for comparison
        phone_names = recommendations['name'].tolist()
        selected_phones = st.multiselect(
            "Select phones to compare (max 3):",
            phone_names,
            default=phone_names[:3] if len(phone_names) >= 3 else phone_names
        )
        
        if selected_phones:
            selected_data = recommendations[recommendations['name'].isin(selected_phones)]
            comparison_df = create_comparison_table(selected_data)
            
            if comparison_df is not None:
                st.dataframe(
                    comparison_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add comparison charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Performance comparison
                    fig_bar = px.bar(
                        selected_data,
                        x='name',
                        y=['camera', 'battery', 'performance', 'display'],
                        title="Specification Comparison",
                        barmode='group'
                    )
                    fig_bar.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font=dict(color='#00f5ff', size=16),
                        xaxis=dict(tickangle=45)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                with col2:
                    # Price comparison
                    fig_price = px.bar(
                        selected_data,
                        x='name',
                        y='price',
                        title="Price Comparison",
                        color='price',
                        color_continuous_scale='viridis'
                    )
                    fig_price.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font=dict(color='#00f5ff', size=16),
                        xaxis=dict(tickangle=45)
                    )
                    st.plotly_chart(fig_price, use_container_width=True)

def add_search_functionality(df):
    """Add search functionality for specific phone models"""
    st.markdown("## 🔍 Search Specific Models")
    
    search_query = st.text_input("Search for a specific phone model:", placeholder="e.g., iPhone 15, Galaxy S24, Pixel 8")
    
    if search_query:
        filtered_phones = df[df['name'].str.contains(search_query, case=False, na=False)]
        
        if len(filtered_phones) > 0:
            st.success(f"Found {len(filtered_phones)} phone(s) matching '{search_query}'")
            
            for _, phone in filtered_phones.iterrows():
                st.markdown(f"""
                <div class="phone-card">
                    <div class="phone-name">{phone['name']}</div>
                    <div class="phone-details">
                        <strong>Price:</strong> ${phone['price']} | 
                        <strong>Camera:</strong> {phone['camera']}/100 | 
                        <strong>Battery:</strong> {phone['battery']}/100 | 
                        <strong>Performance:</strong> {phone['performance']}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"No phones found matching '{search_query}'")

def add_filter_summary(budget, primary_use, brand_pref, min_camera, min_battery):
    """Add a summary of applied filters"""
    st.markdown("## 🎯 Applied Filters")
    
    filters = []
    if budget < 1500:
        filters.append(f"Budget: Up to ${budget}")
    if primary_use != "General Use":
        filters.append(f"Primary Use: {primary_use}")
    if brand_pref != "Any":
        filters.append(f"Brand: {brand_pref}")
    if min_camera > 0:
        filters.append(f"Min Camera Score: {min_camera}/100")
    if min_battery > 0:
        filters.append(f"Min Battery Score: {min_battery}/100")
    
    if filters:
        filter_text = " | ".join(filters)
        st.markdown(f"""
        <div class="neon-card">
            <p style="color: #00f5ff; margin: 0;"><strong>Active Filters:</strong> {filter_text}</p>
        </div>
        """, unsafe_allow_html=True)

def export_recommendations(recommendations):
    """Add export functionality for recommendations"""
    if len(recommendations) > 0:
        st.markdown("## 📥 Export Recommendations")
        
        export_data = recommendations[['name', 'price', 'camera', 'battery', 'performance', 'display', 'brand', 'storage', 'ram']].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = export_data.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv_data,
                file_name=f"phone_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = export_data.to_json(orient='records', indent=2)
            st.download_button(
                label="📄 Download as JSON",
                data=json_data,
                file_name=f"phone_recommendations_{datetime.now().strftime('%Y%m%d_%M%S')}.json",
                mime="application/json"
            )

# Enhanced main function with additional features
def enhanced_main():
    # All the existing code from main() function goes here...
    # Then add these additional features at the end, before the footer:
    
    # Add the additional features
    add_filter_summary(budget, primary_use, brand_pref, min_camera, min_battery)
    add_comparison_section(recommendations)
    add_search_functionality(df)
    export_recommendations(recommendations)
    
    # Add a feedback section
    st.markdown("## 💬 Feedback")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rating = st.select_slider(
            "How helpful were these recommendations?",
            options=['😞 Not helpful', '😐 Somewhat helpful', '😊 Very helpful', '🤩 Extremely helpful'],
            value='😊 Very helpful'
        )
    
    with col2:
        feedback = st.text_area("Any additional feedback or suggestions?", height=100)
        
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback! It helps us improve our recommendations.")

# Add a 'Recently Viewed' feature using session state
def add_recently_viewed(phone_name):
    """Add phone to recently viewed list"""
    if 'recently_viewed' not in st.session_state:
        st.session_state.recently_viewed = []
    
    if phone_name not in st.session_state.recently_viewed:
        st.session_state.recently_viewed.insert(0, phone_name)
        # Keep only last 5 items
        if len(st.session_state.recently_viewed) > 5:
            st.session_state.recently_viewed = st.session_state.recently_viewed[:5]

def show_recently_viewed(df):
    """Show recently viewed phones in the sidebar and allow focusing on them."""
    if 'recently_viewed' in st.session_state and st.session_state.recently_viewed:
        st.sidebar.markdown("## 🕒 Recently Viewed")
        for phone_name in st.session_state.recently_viewed:
            if st.sidebar.button(f"📱 {phone_name}", key=f"recent_{phone_name}"):
                st.session_state.selected_phone = phone_name
                # Optionally, scroll to or highlight this phone in the main view

# Add a function to focus on a selected phone if set

def focus_on_selected_phone(df):
    if 'selected_phone' in st.session_state:
        phone = df[df['name'] == st.session_state.selected_phone]
        if not phone.empty:
            phone = phone.iloc[0]
            explanations = generate_explanation(phone, st.session_state.get('primary_use', 'General Use'), st.session_state.get('budget', 1500))
            st.markdown(f"""
            <div class="phone-card">
                <div class="phone-name">{phone['name']}</div>
                <div class="phone-details">
                    <strong>Price:</strong> ${phone['price']} | 
                    <strong>Camera:</strong> {phone['camera']}/100 | 
                    <strong>Battery:</strong> {phone['battery']}/100 | 
                    <strong>Performance:</strong> {phone['performance']}/100
                </div>
                <div class="explanation">
                    <strong>🤖 Why this phone is perfect for you:</strong><br>
                    {'<br>'.join(['• ' + exp for exp in explanations])}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Integrate all features in main()
def main():
    # Header
    st.markdown('<h1 class="main-header">📱 PhoneHub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Phone Recommendations Tailored Just for You</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_phone_data()
    
    # Sidebar filters
    st.sidebar.markdown("## 🎯 Find Your Perfect Phone")
    
    budget = st.sidebar.slider("💰 Budget (USD)", 300, 1500, 800, 50)
    primary_use = st.sidebar.selectbox("🎯 Primary Use", 
                                      ["General Use", "Photography", "Gaming", "Battery Life"])
    brand_pref = st.sidebar.selectbox("📱 Brand Preference", 
                                     ["Any"] + sorted(df['brand'].unique().tolist()))
    
    st.sidebar.markdown("### Advanced Filters")
    min_camera = st.sidebar.slider("📸 Minimum Camera Score", 0, 100, 0, 5)
    min_battery = st.sidebar.slider("🔋 Minimum Battery Score", 0, 100, 0, 5)
    
    # Store filters in session state for use in focus_on_selected_phone
    st.session_state['budget'] = budget
    st.session_state['primary_use'] = primary_use
    st.session_state['brand_pref'] = brand_pref
    st.session_state['min_camera'] = min_camera
    st.session_state['min_battery'] = min_battery
    
    # Show recently viewed phones in sidebar
    show_recently_viewed(df)
    
    # Get recommendations
    recommendations = get_recommendations(df, budget, primary_use, brand_pref, min_camera, min_battery)
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">💰</h3>
            <p style="color: white; margin: 0;">Budget</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">${budget}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">🎯</h3>
            <p style="color: white; margin: 0;">Primary Use</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{primary_use}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">📱</h3>
            <p style="color: white; margin: 0;">Brand</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{brand_pref}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f5ff; margin: 0;">📊</h3>
            <p style="color: white; margin: 0;">Found</p>
            <p style="color: #00ff88; font-size: 1.2rem; margin: 0;">{len(recommendations)} phones</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Focus on selected phone if set
    focus_on_selected_phone(df)
    
    if len(recommendations) == 0:
        st.markdown("""
        <div class="neon-card">
            <h3 style="color: #ff6b6b; text-align: center;">No phones found matching your criteria</h3>
            <p style="color: #a0a0a0; text-align: center;">Try adjusting your filters or increasing your budget</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display recommendations
    st.markdown("## 🏆 Recommended Phones")
    
    for idx, (_, phone) in enumerate(recommendations.head(5).iterrows()):
        explanations = generate_explanation(phone, primary_use, budget)
        # Add to recently viewed
        add_recently_viewed(phone['name'])
        # Create radar chart for phone specs
        categories = ['Camera', 'Battery', 'Performance', 'Display']
        values = [phone['camera'], phone['battery'], phone['performance'], phone['display']]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=phone['name'],
            line=dict(color='#00f5ff', width=2),
            fillcolor='rgba(0, 245, 255, 0.2)'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    color='white'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    color='white'
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            height=300
        )
        col1, col2 = st.columns([2, 1])
        with col1:
            rank_badge = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx+1}"
            st.markdown(f"""
            <div class="phone-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{rank_badge}</span>
                        <span class="phone-name">{phone['name']}</span>
                    </div>
                    <span class="price">${phone['price']}</span>
                </div>
                <div class="phone-details">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                        <div>📱 <strong>{phone['screen_size']}</strong></div>
                        <div>💾 <strong>{phone['storage']}</strong></div>
                        <div>🧠 <strong>{phone['ram']}</strong></div>
                        <div>📸 <strong>{phone['camera_mp']}</strong></div>
                        <div>🔋 <strong>{phone['battery_mah']}</strong></div>
                        <div>🤖 <strong>{phone['os']}</strong></div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <strong style="color: #00f5ff;">✨ Key Features:</strong><br>
                        {' • '.join(phone['features'])}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <strong style="color: #00ff88;">👍 Pros:</strong><br>
                            {'<br>'.join(['• ' + pro for pro in phone['pros']])}
                        </div>
                        <div>
                            <strong style="color: #ff6b6b;">👎 Cons:</strong><br>
                            {'<br>'.join(['• ' + con for con in phone['cons']])}
                        </div>
                    </div>
                </div>
                <div class="explanation">
                    <strong>🤖 Why this phone is perfect for you:</strong><br>
                    {'<br>'.join(['• ' + exp for exp in explanations])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.plotly_chart(fig, use_container_width=True)
    
    # Add filter summary
    add_filter_summary(budget, primary_use, brand_pref, min_camera, min_battery)
    # Add comparison section
    add_comparison_section(recommendations)
    # Add search functionality
    add_search_functionality(df)
    # Export functionality
    export_recommendations(recommendations)
    # Add feedback section
    st.markdown("## 💬 Feedback")
    col1, col2 = st.columns(2)
    with col1:
        rating = st.select_slider(
            "How helpful were these recommendations?",
            options=['😞 Not helpful', '😐 Somewhat helpful', '😊 Very helpful', '🤩 Extremely helpful'],
            value='😊 Very helpful'
        )
    with col2:
        feedback = st.text_area("Any additional feedback or suggestions?", height=100)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback! It helps us improve our recommendations.")
    # Analytics section
    st.markdown("## 📊 Market Analysis")
    col1, col2 = st.columns(2)
    with col1:
        fig_scatter = px.scatter(
            df, x='price', y='performance', 
            color='brand', size='camera',
            hover_data=['name', 'battery', 'display'],
            title="Price vs Performance Analysis"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(color='#00f5ff', size=16)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col2:
        brand_counts = df['brand'].value_counts()
        fig_pie = px.pie(
            values=brand_counts.values, 
            names=brand_counts.index,
            title="Brand Distribution"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(color='#00f5ff', size=16)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0a0a0; padding: 2rem;">
        <p>🚀 Built with Streamlit • Powered by AI • Made with 💙 for tech enthusiasts</p>
        <p>© 2024 PhoneHub - Your Ultimate Phone Recommendation Assistant</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()