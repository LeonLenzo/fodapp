import streamlit as st
import pandas as pd
import numpy as np

# Configure the page
st.set_page_config(
    page_title="FODapp",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for feminine, mobile-optimized styling
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 50%, #f3e8ff 100%);
        min-height: 100vh;
    }
    
    .main-search {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(219, 39, 119, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .search-title {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #db2777 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .search-subtitle {
        color: #be185d;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        font-style: italic;
    }
    
    /* Style the search input */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%);
        border: 2px solid #f9a8d4;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        color: #be185d;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #db2777;
        box-shadow: 0 0 0 3px rgba(219, 39, 119, 0.1);
    }
    
    /* Style the dataframe */
    .stDataFrame {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(219, 39, 119, 0.08);
        border: 1px solid #f9a8d4;
    }
    
    /* Fix dataframe styling */
    .stDataFrame > div {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%) !important;
    }
    
    .stDataFrame table {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%) !important;
    }
    
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #f9a8d4 0%, #c084fc 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
        text-align: center !important;
    }
    
    .stDataFrame tbody tr td {
        background: rgba(255, 255, 255, 0.8) !important;
        padding: 1rem !important;
        border-bottom: 1px solid #fce7f3 !important;
        color: #be185d !important;
        text-align: center !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) td {
        background: rgba(253, 242, 248, 0.6) !important;
    }
    
    .stDataFrame tbody tr:hover td {
        background: #fdf2f8 !important;
    }
    
    /* Section headers */
    h3 {
        color: #be185d !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%);
        border: 1px solid #f9a8d4;
        border-radius: 12px;
        color: #be185d;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 1px solid #fca5a5;
        border-radius: 12px;
    }
    
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .main-search {
            padding: 2rem 1.5rem;
        }
        
        .search-title {
            font-size: 1.8rem;
        }
        
        .stTextInput > div > div > input {
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .dataframe th,
        .dataframe td {
            padding: 0.75rem 0.5rem !important;
            font-size: 0.9rem !important;
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

def get_category_emoji(category):
    """Convert category to emoji"""
    category_map = {
        'Vegetables': '🥕',
        'Pulses': '🫘', 
        'Grains': '🌾',
        'Fruits': '🍓',
        'Dairy': '🥛',
        'Condiments': '🧂',
        'Beverages': '🍹',
        'Additives': '✨'
    }
    return category_map.get(category, '🍽️')

def get_fodmap_list(row):
    """Get list of FODMAPs for a food item"""
    fodmaps = []
    fodmap_columns = ['fructans', 'gos', 'fructose', 'lactose', 'sorbitol', 'mannitol']
    fodmap_names = ['Fructans', 'GOS', 'Fructose', 'Lactose', 'Sorbitol', 'Mannitol']
    
    for col, name in zip(fodmap_columns, fodmap_names):
        if col in row and row[col]:
            fodmaps.append(name)
    
    return ', '.join(fodmaps) if fodmaps else 'None detected'

def display_autocomplete_suggestions(search_term, df, max_suggestions=5):
    """Display autocomplete suggestions - REMOVED"""
    return None

def main():
    # Main search interface
    st.markdown("""
    <div class="main-search">
        <div class="search-title">🌸 FODapp 🌸</div>
        <div class="search-subtitle">✨ Safe foods for Caitlin ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_fodmap_data()
    
    if df is not None:
        # Search input
        search_term = st.text_input(
            "🔍 Search:",
            placeholder="Start typing... (e.g., pasta, snacky etc.)",
            help="💕 Type to search for your favorite foods!"
        )
        
        # Show search results in table
        if search_term:
            # Filter foods that contain the search term
            filtered_foods = df[
                df['name'].str.contains(search_term, case=False, na=False)
            ]
            
            if len(filtered_foods) > 0:
                st.markdown(f"### 💖 Found {len(filtered_foods)} fring(s)!")
                
                # Prepare data for table
                table_data = []
                for _, row in filtered_foods.iterrows():
                    traffic_emoji = {"Green": "💚", "Amber": "💛", "Red": "❤️"}
                    fodmaps = get_fodmap_list(row)
                    
                    # Simplified safe amount with traffic light info
                    safe_amount = str(row['safe_amount'])  # Convert to string first
                    if safe_amount == 'Any':
                        safe_amount = "💚 Unlimited"
                    elif safe_amount == 'None' or safe_amount == 'nan' or pd.isna(row['safe_amount']):
                        safe_amount = "❤️ Avoid"
                    else:
                        safe_amount = f"💛 {safe_amount}"  # Show amount with amber emoji
                    
                    table_data.append({
                        "🍽️ Food": row['name'],
                        "🏷️": get_category_emoji(row['category']),
                        "💝 Safe Amount": safe_amount,
                        "🧬 FODMAPs": fodmaps if fodmaps != 'None detected' else ''
                    })
                
                # Create DataFrame and display as table
                results_df = pd.DataFrame(table_data)
                
                # Sort by traffic light priority
                priority_map = {"💚 Unlimited": 0, "💛": 1, "❤️ Avoid": 2}
                # For amber foods, we need to check if it starts with 💛
                def get_priority(safe_amount):
                    if safe_amount == "💚 Unlimited":
                        return 0
                    elif safe_amount == "❤️ Avoid":
                        return 2
                    else:
                        return 1  # All amber foods
                
                results_df['sort_priority'] = results_df['💝 Safe Amount'].apply(get_priority)
                results_df = results_df.sort_values(['sort_priority', '🍽️ Food']).drop('sort_priority', axis=1)
                
                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "🍽️ Food": st.column_config.TextColumn("🍽️ Food", width=140),
                        "🏷️": st.column_config.TextColumn("🏷️", width=40),
                        "💝 Safe Amount": st.column_config.TextColumn("💝 Safe Amount", width=100),
                        "🧬 FODMAPs": st.column_config.TextColumn("🧬 FODMAPs", width=100)
                    }
                )
            else:
                st.info(f"💭 No foods found containing '{search_term}'. Try different keywords, beautiful! 💕")
        else:
            st.markdown("### I love you darling! 💖")
    
    else:
        st.error("❌ Unable to load FODMAP data. Please check that 'data.csv' exists and is properly formatted.")

if __name__ == "__main__":
    main()