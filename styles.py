mishtee_css = """
/* General Container Styling */
.gradio-container {
    background-color: #FAF9F6 !important;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #333333;
}

/* Headings: Spaced-out Serif for a Luxury Look */
h1, h2, h3 {
    font-family: 'Georgia', 'serif' !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    color: #333333;
    margin-bottom: 1.5rem !important;
}

/* Buttons: Sober Terracotta, Sharp Edges */
button.primary {
    background: #C06C5C !important;
    color: white !important;
    border: 1px solid #C06C5C !important;
    border-radius: 0px !important;
    padding: 10px 24px !important;
    font-family: 'Georgia', serif !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all 0.3s ease;
    box-shadow: none !important;
}

button.primary:hover {
    background: transparent !important;
    color: #C06C5C !important;
}

/* Form Elements & Inputs */
input, textarea, .svelte-1kvv3n6 {
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Tables: Lightweight Sans-Serif */
table {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
    font-weight: 300 !important;
    border-collapse: collapse !important;
}

th, td {
    border: 1px solid #333333 !important;
    padding: 12px !important;
}

/* Layout Padding & Whitespace */
.gap {
    gap: 2.5rem !important;
}

.block {
    padding: 2rem !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 0px !important;
    background: #FAF9F6 !important;
    box-shadow: none !important;
}

/* Removing Bubbly Gradio Defaults */
* {
    border-radius: 0px !important;
}
"""
