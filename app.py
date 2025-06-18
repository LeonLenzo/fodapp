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
    
    .autocomplete-suggestion {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .autocomplete-suggestion:hover {
        background: #e2e8f0;
        border-color: #cbd5e1;
    }
    
    .traffic-light {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .green-light { background-color: #22c55e; }
    .amber-light { background-color: #f59e0b; }
    .red-light { background-color: #ef4444; }
    
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }
    
    .results-table th {
        background: #f8fafc;
        padding: 1rem;
        text-align: left;
        border-bottom: 2px solid #e2e8f0;
        font-weight: 600;
    }
    
    .results-table td {
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .results-table tr:hover {
        background: #f8fafc;
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
        
        .results-table th,
        .results-table td {
            padding: 0.75rem 0.5rem;
            font-size: 0.9rem;
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
    """Display autocomplete suggestions"""
    if not search_term or len(search_term) < 2:
        return None
    
    # Filter foods that start with or contain the search term
    starts_with = df[df['name'].str.lower().str.startswith(search_term.lower())]['name'].tolist()
    contains = df[df['name'].str.lower().str.contains(search_term.lower()) & 
                 ~df['name'].str.lower().str.startswith(search_term.lower())]['name'].tolist()
    
    suggestions = starts_with[:max_suggestions] + contains[:max_suggestions - len(starts_with)]
    suggestions = suggestions[:max_suggestions]
    
    if suggestions:
        st.markdown("**Suggestions:**")
        for suggestion in suggestions:
            food_info = df[df['name'] == suggestion].iloc[0]
            traffic_color = food_info['traffic_light'].lower()
            
            suggestion_html = f"""
            <div class="autocomplete-suggestion" onclick="document.querySelector('input[aria-label=\\"🔍 Search for foods:\\"]').value='{suggestion}'; document.querySelector('input[aria-label=\\"🔍 Search for foods:\\"]').dispatchEvent(new Event('input', {{bubbles: true}}));">
                <span class="traffic-light {traffic_color}-light"></span>
                <strong>{suggestion}</strong> - {food_info['category']} - {food_info['safe_amount']}
            </div>
            """
            st.markdown(suggestion_html, unsafe_allow_html=True)
    
    return suggestions

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
        # Search input
        search_term = st.text_input(
            "🔍 Search for foods:",
            placeholder="Start typing... (e.g., wheat, apple, dairy)",
            help="Type to search and see suggestions"
        )
        
        # Show autocomplete suggestions
        if search_term and len(search_term) >= 2:
            suggestions = display_autocomplete_suggestions(search_term, df)
        
        # Show search results in table
        if search_term:
            # Filter foods that contain the search term
            filtered_foods = df[
                df['name'].str.contains(search_term, case=False, na=False)
            ]
            
            if len(filtered_foods) > 0:
                st.markdown(f"### Found {len(filtered_foods)} food(s)")
                
                # Prepare data for table
                table_data = []
                for _, row in filtered_foods.iterrows():
                    traffic_emoji = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}
                    fodmaps = get_fodmap_list(row)
                    
                    table_data.append({
                        "Food": row['name'],
                        "Category": row['category'],
                        "Status": f"{traffic_emoji.get(row['traffic_light'], '⚪')} {row['traffic_light']}",
                        "Safe Amount": row['safe_amount'],
                        "FODMAPs": fodmaps
                    })
                
                # Create DataFrame and display as table
                results_df = pd.DataFrame(table_data)
                
                # Sort by traffic light priority
                priority_map = {"🟢 Green": 0, "🟡 Amber": 1, "🔴 Red": 2}
                results_df['sort_priority'] = results_df['Status'].map(priority_map)
                results_df = results_df.sort_values(['sort_priority', 'Food']).drop('sort_priority', axis=1)
                
                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Food": st.column_config.TextColumn("Food", width="medium"),
                        "Category": st.column_config.TextColumn("Category", width="small"),
                        "Status": st.column_config.TextColumn("Status", width="small"),
                        "Safe Amount": st.column_config.TextColumn("Safe Amount", width="medium"),
                        "FODMAPs": st.column_config.TextColumn("FODMAPs", width="large")
                    }
                )
            else:
                st.info(f"No foods found containing '{search_term}'. Try different keywords.")
        else:
            st.markdown("### 💡 Start typing above to search for foods")
    
    else:
        st.error("❌ Unable to load FODMAP data. Please check that 'data.csv' exists and is properly formatted.")

if __name__ == "__main__":
    main()