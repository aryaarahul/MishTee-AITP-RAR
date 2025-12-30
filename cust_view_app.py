import gradio as gr
import pandas as pd
import requests
from supabase import create_client, Client

# --- 1. ASSETS & CREDENTIALS ---
SUPABASE_URL = "https://bqgauixrvfuerczvavdn.supabase.co"
SUPABASE_KEY = "sb_publishable_h5ayYpa4SdMTvoUVPw0cQA_rYJrAOoN"
LOGO_URL = "https://github.com/aryaarahul/MishTee-AITP-RAR/blob/main/Gemini_Generated_Image_rnuh7yrnuh7yrnuh.png?raw=true"
STYLE_URL = "https://raw.githubusercontent.com/aryaarahul/MishTee-AITP-RAR/refs/heads/main/styles.py"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch Custom CSS from GitHub
try:
    response = requests.get(STYLE_URL)
    content = response.text
    if 'mishtee_css = """' in content:
        mishtee_css = content.split('mishtee_css = """')[1].split('"""')[0]
    else:
        mishtee_css = content
except Exception:
    # Fallback Sober Minimalist CSS
    mishtee_css = """
    .gradio-container { background-color: #FAF9F6 !important; font-family: 'Georgia', serif; }
    button.primary { background: #C06C5C !important; border: none !important; border-radius: 0px !important; color: white !important; }
    input, .svelte-1kvv3n6 { border-radius: 0px !important; border: 1px solid #333333 !important; }
    h1, h2 { color: #333; letter-spacing: 2px; text-transform: uppercase; text-align: center; }
    """

# --- 2. CORE FUNCTIONS ---

def get_customer_data(phone_number):
    """Retrieves customer name and order history."""
    if not phone_number or not phone_number.startswith('9') or len(phone_number) != 10:
        return "Please enter a valid 10-digit number starting with 9.", pd.DataFrame()

    # Fetch Name
    cust_res = supabase.table("customers").select("full_name").eq("phone", phone_number).execute()
    if not cust_res.data:
        return "Welcome to MishTee-Magic! Please visit a store to register.", pd.DataFrame()
    
    name = cust_res.data[0]['full_name']
    greeting = f"## Namaste, {name} ji! \n*Great to see you again.*"

    # Fetch Orders with Product Join
    order_res = supabase.table("orders").select(
        "order_id, order_date, qty_kg, order_value_inr, status, products(sweet_name)"
    ).eq("cust_phone", phone_number).order("order_date", desc=True).execute()

    if order_res.data:
        df = pd.DataFrame(order_res.data)
        df['Sweet Name'] = df['products'].apply(lambda x: x['sweet_name'] if x else "Artisanal Blend")
        df = df[['order_id', 'order_date', 'Sweet Name', 'qty_kg', 'order_value_inr', 'status']]
        df.columns = ['ID', 'Date', 'Product', 'Qty (kg)', 'Total (₹)', 'Status']
        return greeting, df
    
    return greeting, pd.DataFrame(columns=['ID', 'Date', 'Product', 'Qty (kg)', 'Total (₹)', 'Status'])

def get_trending_items():
    """Retrieves top 4 products by quantity sold."""
    res = supabase.table("orders").select("qty_kg, products(sweet_name, variant_type, price_per_kg)").execute()
    if not res.data:
        return pd.DataFrame()

    raw = [{"Name": e['products']['sweet_name'], "Variant": e['products']['variant_type'], 
            "Price": e['products']['price_per_kg'], "Qty": e['qty_kg']} for e in res.data]
    
    df = pd.DataFrame(raw)
    trending = df.groupby(['Name', 'Variant', 'Price']).agg({'Qty': 'sum'}).reset_index()
    trending = trending.sort_values(by='Qty', ascending=False).head(4)
    trending.columns = ['Sweet Name', 'Variant', 'Price (₹/kg)', 'Popularity (Total Kg)']
    return trending

# --- 3. GRADIO UI LAYOUT ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic | Customer Portal") as demo:
    
    # Header Section
    with gr.Column():
        gr.Image(LOGO_URL, show_label=False, container=False, width=180, elem_id="main-logo")
        gr.Markdown("# MISH TEE MAGIC")
        gr.Markdown("<p style='text-align: center; color: #C06C5C;'>Purity and Health: The Golden Standard of Artisanal Sweets</p>")
    
    gr.HTML("<hr style='border: 0; border-top: 1px solid #E0E0E0; margin: 30px 0;'>")

    # Welcome & Login Logic
    with gr.Row(variant="compact"):
        with gr.Column(scale=3):
            phone_input = gr.Textbox(label="Registered Mobile", placeholder="9XXXXXXXXX")
        with gr.Column(scale=1):
            login_btn = gr.Button("ACCESS MY MAGIC", variant="primary")

    # Personalized Greeting Output
    welcome_msg = gr.Markdown("### Welcome to the Member Lounge")

    # Tabbed Navigation for Data
    with gr.Tabs():
        with gr.TabItem("My Order History"):
            history_table = gr.Dataframe(interactive=False, wrap=True)
            
        with gr.TabItem("Trending Today"):
            trending_table = gr.Dataframe(value=get_trending_items(), interactive=False)
            gr.Markdown("<p style='font-size: 0.8em; color: #666;'>*Based on weekly artisanal demand across Ahmedabad hubs.</p>")

    # Trigger Logic
    login_btn.click(
        fn=get_customer_data,
        inputs=phone_input,
        outputs=[welcome_msg, history_table]
    )

    # Footer
    gr.HTML("""
        <div style='text-align: center; margin-top: 60px; font-size: 0.7em; letter-spacing: 3px; color: #333;'>
            SATELLITE • BOPAL • AMBAWADI • VASTRAPUR
        </div>
    """)

if __name__ == "__main__":
    demo.launch()
