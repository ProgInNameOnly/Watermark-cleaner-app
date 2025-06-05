import streamlit as st
import unicodedata

st.set_page_config(page_title="AI Text Cleaner", layout="centered")

st.title("🧼 AI Text Cleaner")
st.caption("Paste any text below to detect & replace hidden characters or em dashes to make it look more human-generated.")

# Toggle for em dash replacement style
replacement_style = st.radio(
    "How should em dashes (—) be replaced?",
    options=[
        "Comma with space (, )",
        "Period and space (. )",
        "Just a space ( )",
        "Remove completely"
    ]
)

# Input
raw_text = st.text_area("Paste AI-generated or suspicious text here:", height=300)

def clean_text(text, em_dash_style):
    hidden_char_log = []
    cleaned = ""

    for i, char in enumerate(text):
        codepoint = ord(char)

        if char == '\u2014':  # Em dash
            if em_dash_style == "Comma with space (, )":
                cleaned += ', '
            elif em_dash_style == "Period and space (. )":
                cleaned += '. '
            elif em_dash_style == "Just a space ( )":
                cleaned += ' '
            elif em_dash_style == "Remove completely":
                cleaned += ''  # Do nothing

            context = text[max(0, i-10):min(len(text), i+10)].replace('\n', '⏎')
            hidden_char_log.append((char, f"U+{codepoint:04X}", "EM DASH", context))

        elif char.isspace() and char not in [' ', '\n', '\t']:
            cleaned += ' '
            name = unicodedata.name(char, 'UNKNOWN')
            context = text[max(0, i-10):min(len(text), i+10)].replace('\n', '⏎')
            hidden_char_log.append((char, f"U+{codepoint:04X}", name, context))

        elif unicodedata.category(char)[0] == 'C' and char != '\n':
            cleaned += ''
            name = unicodedata.name(char, 'CONTROL CHARACTER')
            context = text[max(0, i-10):min(len(text), i+10)].replace('\n', '⏎')
            hidden_char_log.append((char, f"U+{codepoint:04X}", name, context))

        else:
            cleaned += char

    return cleaned, hidden_char_log

if raw_text:
    cleaned_text, findings = clean_text(raw_text, replacement_style)

    if findings:
        st.subheader("🔍 Hidden Characters Detected")
        for char, code, name, context in findings:
            st.code(f"{code} ({name}): ...{context}...")
    else:
        st.success("✅ No hidden characters detected.")

    st.subheader("🧾 Cleaned Text")
    st.text_area("You can copy your cleaned text here:", value=cleaned_text, height=300)

    # Download
    st.download_button("📥 Download cleaned text", cleaned_text, file_name="cleaned_text.txt", mime="text/plain")
