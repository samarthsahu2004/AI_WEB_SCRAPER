import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")
        
        dom_chunk = scrape_website(url)

        if dom_chunk is None:
            dom_content = ""
        elif isinstance(dom_chunk, str):

            dom_content = dom_chunk
        elif isinstance(dom_chunk, list):
            dom_content = "\n".join(str(chunk) for chunk in dom_chunk)
        else:
            raise TypeError(f"Unexpected type for dom_chunk: {type(dom_chunk)}")
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with GEMINI
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_gemini(dom_chunks, parse_description)
            st.write(parsed_result)
