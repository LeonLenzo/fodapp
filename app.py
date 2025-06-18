import streamlit as st
import pandas as pd
import numpy as np

# Configure the page
st.set_page_config(
    page_title="FODMAP Food Search",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-optimized styling
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .main-search {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .search-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .search-subtitle {
        color: #6b7280;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }
    
    .food-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .green-card {
        border-left-color: #22c55e;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    
    .amber-card {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    }
    
    .red-card {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    }
    
    .food-name {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .food-category {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 0.75rem;
    }
    
    .fodmap-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.75rem 0;
    }
    
    .fodmap-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: #3b82f6;
        color: white;
        text-transform: uppercase;
    }
    
    .safe-amount {
        font-weight: bold;
        font-size: 1.3rem;
        margin-top: 0.75rem;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .green-amount { 
        color: #059669; 
        background: rgba(34, 197, 94, 0.1);
    }
    .amber-amount { 
        color: #d97706; 
        background: rgba(245, 158, 11, 0.1);
    }
    .red-amount { 
        color: #dc2626; 
        background: rgba(239, 68, 68, 0.1);
    }
    
    .traffic-light-indicator {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.75rem;
    }
    
    .green-light { background-color: #22c55e; }
    .amber-light { background-color: #f59e0b; }
    .red-light { background-color: #ef4444; }
    
    .category-section {
        margin: 2rem 0;
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .category-button {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 600;
        color: #475569;
    }
    
    .category-button:hover {
        background: #e2e8f0;
        border-color: #cbd5e1;
    }
    
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .main-search {
            padding: 1.5rem;
        }
        
        .search-title {
            font-size: 1.7rem;
        }
        
        .food-card {
            padding: 1.25rem;
        }
        
        .food-name {
            font-size: 1.2rem;
        }
        
        .category-grid {
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_fodmap_data():
    """Load FODMAP data from CSV file"""
    try:
        df = pd.read_csv("data.csv")
        # Convert TRUE/FALSE strings to boolean
        boolean_columns = ['fructans', 'gos', 'fructose', 'lactose', 'sorbitol', 'mannitol']
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].map({'TRUE': True, 'FALSE': False, True: True, False: False})
        return df
    except FileNotFoundError:
        st.error("❌ Could not find 'data.csv' file. Please make sure it's in the same directory as your app.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {e}")
        return None

def get_fodmap_badges(row):
    """Generate FODMAP badges for a food item"""
    badges = []
    fodmap_columns = ['fructans', 'gos', 'fructose', 'lactose', 'sorbitol', 'mannitol']
    fodmap_names = ['Fructans', 'GOS', 'Fructose', 'Lactose', 'Sorbitol', 'Mannitol']
    
    for col, name in zip(fodmap_columns, fodmap_names):
        if col in row and row[col]:
            badges.append(f'<span class="fodmap-badge">{name}</span>')
    
    return ''.join(badges) if badges else '<span style="color: #6b7280; font-style: italic;">No FODMAPs detected</span>'

def display_food_card(row):
    """Display a food item as a card"""
    traffic_light = row['traffic_light']
    card_class = f"{traffic_light.lower()}-card"
    amount_class = f"{traffic_light.lower()}-amount"
    light_class = f"{traffic_light.lower()}-light"
    
    # Format safe amount
    if row['safe_amount'] == 'Any':
        amount_text = "✅ Eat freely - any amount"
    elif row['safe_amount'] == 'None':
        amount_text = "❌ Avoid completely"
    else:
        amount_text = f"⚠️ Safe up to: {row['safe_amount']}"
    
    fodmap_badges = get_fodmap_badges(row)
    
    card_html = f"""
    <div class="food-card {card_class}">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span class="traffic-light-indicator {light_class}"></span>
            <div class="food-name">{row['name']}</div>
        </div>
        <div class="food-category">{row['category']}</div>
        <div class="fodmap-badges">{fodmap_badges}</div>
        <div class="safe-amount {amount_class}">{amount_text}</div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def main():
    # Main search interface
    st.markdown("""
    <div class="main-search">
        <div class="search-title">🥗 FODMAP Food Search</div>
        <div class="search-subtitle">Find safe foods and portions for your low-FODMAP diet</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_fodmap_data()
    
    if df is not None:
        # Simple predictive search dropdown
        food_names = [''] + sorted(df['name'].unique().tolist())
        selected_food = st.selectbox(
            "🔍 Search for a food:",
            options=food_names,
            index=0,
            placeholder="Start typing or click to see all foods...",
            help="Click to see all foods, or start typing to filter the list"
        )
        
        # Show selected food details
        if selected_food:
            food_row = df[df['name'] == selected_food].iloc[0]
            display_food_card(food_row)
    
    else:
        st.error("❌ Unable to load FODMAP data. Please check that 'data.csv' exists and is properly formatted.")

if __name__ == "__main__":
    main()