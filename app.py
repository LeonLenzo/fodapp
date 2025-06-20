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
    
    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
        border-radius: 15px;
        color: #be185d;
        border: 2px solid #f9a8d4;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #db2777 0%, #c084fc 100%);
        color: white;
        border-color: #db2777;
    }
    
    /* Recipe cards */
    .recipe-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(219, 39, 119, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #f9a8d4;
    }
    
    .recipe-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #be185d;
        margin-bottom: 0.5rem;
    }
    
    .recipe-meta {
        color: #9333ea;
        font-size: 0.9rem;
        margin-bottom: 1rem;
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
    
    /* Style expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%);
        border: 1px solid #f9a8d4;
        border-radius: 12px;
        color: #be185d;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
        border: 1px solid #f9a8d4;
        border-top: none;
        border-radius: 0 0 12px 12px;
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
        
        .recipe-card {
            padding: 1rem;
        }
        
        .recipe-title {
            font-size: 1.1rem;
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

@st.cache_data
def load_recipes():
    """Load recipes from JSON file"""
    try:
        import json
        with open("recipes.json", "r", encoding="utf-8") as f:
            recipes = json.load(f)
        return recipes
    except FileNotFoundError:
        st.error("❌ Could not find 'recipes.json' file. Please make sure it's in the same directory as your app.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading recipes file: {e}")
        return None

def get_category_emoji(category):
    """Convert category to emoji"""
    category_map = {
        'Vegetables': 'Veggies🥕',
        'Pulses': 'Pulses🫘', 
        'Grains': 'Grains🌾',
        'Fruits': 'Fruits🍓',
        'Dairy': 'Dairy🥛',
        'Condiments': 'Condiments🧂',
        'Beverages': 'Beverages🍹',
        'Additives': 'Additives✨'
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

def parse_recipes(recipes_data):
    """Parse the recipes JSON data into display format"""
    if not recipes_data:
        return {}
    
    recipes_by_category = {}
    
    # Category mapping
    category_mapping = {
        "seafood": "🐟 Seafood Dishes",
        "red_meat": "🥩 Red Meat Dishes", 
        "chicken": "🐔 Chicken Dishes",
        "vegetarian": "🥗 Vegetarian Sides & Salads"
    }
    
    for category_key, category_name in category_mapping.items():
        if category_key in recipes_data:
            recipes_by_category[category_name] = recipes_data[category_key]
    
    return recipes_by_category

def display_recipe(recipe):
    """Display a single recipe in a nice format"""
    st.markdown(f"""
    <div class="recipe-card">
        <div class="recipe-title">✨ {recipe['title']} ✨</div>
        <div class="recipe-meta">{recipe['serves']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**💕 Ingredients:**")
        for ingredient in recipe['ingredients']:
            st.markdown(f"• {ingredient}")
    
    with col2:
        st.markdown("**👩‍🍳 Instructions:**")
        for i, instruction in enumerate(recipe['instructions'], 1):
            # Clean up instruction numbering
            clean_instruction = instruction
            if instruction.startswith(f"{i}."):
                clean_instruction = instruction[len(f"{i}."):]
            elif instruction[0].isdigit() and ". " in instruction:
                clean_instruction = instruction.split(". ", 1)[1]
            
            st.markdown(f"{i}. {clean_instruction}")

def fodmap_search_tab():
    """FODMAP food search functionality"""
    # Load data
    df = load_fodmap_data()
    
    if df is not None:
        # Create a searchable FODMAP text column
        df['fodmap_text'] = df.apply(get_fodmap_list, axis=1)

        # Search input
        search_term = st.text_input(
            "🔍 Search:",
            placeholder="Search for foods by name, category, or FODMAPs...",
            help="💕 Type to search for your favorite foods!",
            key="food_search"
        )
        
        # Show search results in table
        if search_term:
            # Filter foods that contain the search term in either name OR category
            filtered_foods = df[
                df['name'].str.contains(search_term, case=False, na=False) |
                df['category'].str.contains(search_term, case=False, na=False) |
                df['fodmap_text'].str.contains(search_term, case=False, na=False)
            ]
            
            if len(filtered_foods) > 0:
                st.markdown(f"### 💖 Found {len(filtered_foods)} result(s)!")
                
                # Prepare data for table
                table_data = []
                for _, row in filtered_foods.iterrows():
                    traffic_emoji = {"Green": "💚", "Amber": "💛", "Red": "❤️"}
                    fodmaps = get_fodmap_list(row)
                    
                    # Simplified safe amount with traffic light info
                    safe_amount = str(row['safe_amount'])  # Convert to string first
                    if safe_amount == 'Any':
                        safe_amount = "💚"
                    elif safe_amount == 'None' or safe_amount == 'nan' or pd.isna(row['safe_amount']):
                        safe_amount = "💔"
                    else:
                        safe_amount = f"💛 {safe_amount}"  # Show amount with amber emoji
                    
                    table_data.append({
                        "🍽️": row['name'],
                        "🏷️": get_category_emoji(row['category']),
                        "🚦": safe_amount,
                        "🧬": fodmaps if fodmaps != 'None detected' else ''
                    })
                
                # Create DataFrame and display as table
                results_df = pd.DataFrame(table_data)
                
                # Sort by traffic light priority
                def get_priority(safe_amount):
                    if safe_amount == "💚":
                        return 0
                    elif safe_amount == "💔":
                        return 2
                    else:
                        return 1  # All amber foods
                
                results_df['sort_priority'] = results_df['🚦'].apply(get_priority)
                results_df = results_df.sort_values(['sort_priority', '🍽️']).drop('sort_priority', axis=1)
                
                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "🍽️": st.column_config.TextColumn("🍽️", width=140),
                        "🏷️": st.column_config.TextColumn("🏷️", width=80),
                        "🚦": st.column_config.TextColumn("🚦", width=80),
                        "🧬": st.column_config.TextColumn("🧬", width=100)
                    }
                )
            else:
                st.info(f"💭 No foods found containing '{search_term}'. Try different keywords, beautiful! 💕")
        else:
            st.markdown("### I love you darling! 💖")
    
    else:
        st.error("❌ Unable to load FODMAP data. Please check that 'data.csv' exists and is properly formatted.")

def recipes_tab():
    """Recipe browser functionality"""
    recipes_data = load_recipes()
    
    if recipes_data:
        recipes_by_category = parse_recipes(recipes_data)
        
        if recipes_by_category:
            # Recipe search
            recipe_search = st.text_input(
                "🔍 Search Recipes:",
                placeholder="Search by recipe name or ingredient...",
                help="💕 Find the perfect meal for you and dad!",
                key="recipe_search"
            )
            
            # Filter recipes based on search
            if recipe_search:
                filtered_recipes = {}
                search_lower = recipe_search.lower()
                
                for category, recipes in recipes_by_category.items():
                    matching_recipes = []
                    for recipe in recipes:
                        # Search in title and ingredients
                        if (search_lower in recipe['title'].lower() or 
                            any(search_lower in ingredient.lower() for ingredient in recipe['ingredients'])):
                            matching_recipes.append(recipe)
                    
                    if matching_recipes:
                        filtered_recipes[category] = matching_recipes
                
                if filtered_recipes:
                    st.markdown(f"### 💖 Found recipes matching '{recipe_search}'!")
                    for category, recipes in filtered_recipes.items():
                        st.markdown(f"#### {category}")
                        for recipe in recipes:
                            with st.expander(f"✨ {recipe['title']} ✨"):
                                display_recipe(recipe)
                else:
                    st.info(f"💭 No recipes found matching '{recipe_search}'. Try different keywords, beautiful! 💕")
            
            else:
                # Show all recipes by category
                st.markdown("### 💖 Low-FODMAP Recipes 💖")
                st.markdown("*Delicious recipes for your poopy butt* ✨")
                
                for category, recipes in recipes_by_category.items():
                    st.markdown(f"#### {category}")
                    
                    for recipe in recipes:
                        with st.expander(f"✨ {recipe['title']} ✨"):
                            display_recipe(recipe)
        else:
            st.error("❌ Unable to parse recipes. Please check the format of your recipes.json file.")
    else:
        st.error("❌ Unable to load recipes. Please check that 'recipes.json' exists and is properly formatted.")

def main():
    # Main search interface
    st.markdown("""
    <div class="main-search">
        <div class="search-title">🌸 FODapp 🌸</div>
        <div class="search-subtitle">✨ Safe foods & recipes for Caitlin ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["🍽️ FODMAP Foods", "👩‍🍳 Recipes"])
    
    with tab1:
        fodmap_search_tab()
    
    with tab2:
        recipes_tab()

if __name__ == "__main__":
    main()