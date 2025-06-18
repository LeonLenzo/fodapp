import streamlit as st
import pandas as pd
import numpy as np

# Configure the page
st.set_page_config(
    page_title="FODMAP Food Search",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile experience and styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
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
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .food-category {
        font-size: 0.875rem;
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
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #3b82f6;
        color: white;
        text-transform: uppercase;
    }
    
    .safe-amount {
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 0.75rem;
        padding: 0.5rem;
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
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .green-light { background-color: #22c55e; }
    .amber-light { background-color: #f59e0b; }
    .red-light { background-color: #ef4444; }
    
    .search-results-header {
        color: #374151;
        font-size: 1.1rem;
        margin: 1rem 0;
        font-weight: 600;
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
    st.title("🥗 FODMAP Food Search")
    st.markdown("*Find safe foods and portions for your low-FODMAP diet*")
    
    # Load data from CSV file
    df = load_fodmap_data()
    
    if df is not None:
        # Sidebar filters
        st.sidebar.header("🔍 Search & Filter")
        
        # Predictive search dropdown
        food_names = [''] + sorted(df['name'].unique().tolist())
        selected_food = st.sidebar.selectbox(
            "🔍 Search for foods:",
            options=food_names,
            index=0,
            help="Start typing to find foods quickly"
        )
        
        # Additional text search for partial matches
        search_term = st.sidebar.text_input(
            "Or search by typing:",
            placeholder="e.g., apple, carrot, bread...",
            help="Type any part of a food name for broader search"
        )
        
        # Category filter
        categories = ['All'] + sorted(df['category'].unique().tolist())
        category_filter = st.sidebar.selectbox("Category:", categories)
        
        # Traffic light filter
        traffic_lights = ['All', 'Green', 'Amber', 'Red']
        traffic_filter = st.sidebar.selectbox("Traffic Light:", traffic_lights)
        
        # FODMAP type filter
        fodmap_types = ['All', 'Fructans', 'GOS', 'Fructose', 'Lactose', 'Sorbitol', 'Mannitol']
        fodmap_filter = st.sidebar.selectbox("Contains FODMAP:", fodmap_types)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Predictive search filter (exact match)
        if selected_food:
            filtered_df = filtered_df[filtered_df['name'] == selected_food]
        # Text search filter (partial match) - only apply if no specific food selected
        elif search_term:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Category filter
        if category_filter != 'All':
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        # Traffic light filter
        if traffic_filter != 'All':
            filtered_df = filtered_df[filtered_df['traffic_light'] == traffic_filter]
        
        # FODMAP filter
        if fodmap_filter != 'All':
            fodmap_col = fodmap_filter.lower()
            if fodmap_col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[fodmap_col] == True]
        
        # Display results
        st.markdown(f'<div class="search-results-header">Found {len(filtered_df)} foods</div>', unsafe_allow_html=True)
        
        if len(filtered_df) == 0:
            st.info("No foods found matching your criteria. Try adjusting your search or filters.")
        else:
            # Sort by traffic light (Green, Amber, Red) then by name
            traffic_order = {'Green': 0, 'Amber': 1, 'Red': 2}
            filtered_df['sort_order'] = filtered_df['traffic_light'].map(traffic_order)
            filtered_df = filtered_df.sort_values(['sort_order', 'name'])
            
            # Display cards
            for _, row in filtered_df.iterrows():
                display_food_card(row)
        
        # Summary statistics in sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Quick Stats")
        
        total_foods = len(df)
        green_foods = len(df[df['traffic_light'] == 'Green'])
        amber_foods = len(df[df['traffic_light'] == 'Amber'])
        red_foods = len(df[df['traffic_light'] == 'Red'])
        
        st.sidebar.metric("Total Foods", total_foods)
        col1, col2, col3 = st.sidebar.columns(3)
        with col1:
            st.metric("🟢", green_foods)
        with col2:
            st.metric("🟡", amber_foods)
        with col3:
            st.metric("🔴", red_foods)
    
    else:
        st.error("❌ Unable to load FODMAP data. Please check that 'data.csv' exists and is properly formatted.")

if __name__ == "__main__":
    main()