import streamlit as st
import openai
import re
import os
from dotenv import load_dotenv

# Load environment variables (optional, for local development)
load_dotenv()

def validate_api_key(api_key):
    """Validate the OpenAI API key by making a test request."""
    if not api_key or not api_key.strip():
        return False
    
    # Check if the API key follows the expected format
    if not api_key.startswith("sk-") or len(api_key) < 20:
        return False
    
    # Make a minimal API call to verify the key works
    try:
        client = openai.OpenAI(api_key=api_key)
        # Using a minimal request to check if the API key is valid
        models = client.models.list()
        return True
    except Exception as e:
        st.error(f"API key validation error: {str(e)}")
        return False

def enhance_prompt(role, context, task):
    """Generate an enhanced and intelligent prompt based on user inputs."""
    # Dictionary of domain-specific knowledge to enhance prompts
    domain_knowledge = {
        "iso": {
            "description": "International Organization for Standardization - a global standard-setting body",
            "context_add": "ISO standards are crucial for ensuring consistency, quality, and safety across industries worldwide.",
            "common_standards": ["ISO 9001 (Quality Management)", "ISO 14001 (Environmental Management)", 
                                "ISO 27001 (Information Security)", "ISO 22301 (Business Continuity)"]
        },
        "iso 22301": {
            "description": "Business Continuity Management System standard",
            "context_add": "ISO 22301 helps organizations prepare for, respond to, and recover from disruptive incidents.",
            "key_components": ["Risk Assessment", "Business Impact Analysis", "Business Continuity Strategy", 
                              "Business Continuity Plans", "Exercise and Testing", "Performance Evaluation"]
        },
        "iso 9001": {
            "description": "Quality Management System standard",
            "context_add": "ISO 9001 helps organizations ensure they meet customer requirements and enhance satisfaction."
        },
        "iso 27001": {
            "description": "Information Security Management System standard",
            "context_add": "ISO 27001 helps organizations protect their information assets."
        }
    }
    
    # Clean and normalize inputs
    role_clean = role.strip().lower()
    context_clean = context.strip().lower()
    task_clean = task.strip().lower()
    
    # Detect keywords in the inputs
    combined_text = f"{role_clean} {context_clean} {task_clean}"
    
    # Format role properly
    role_refined = role.strip()
    if not role_refined.lower().startswith(("you are", "as a", "as an")):
        if role_refined.lower().startswith("i am"):
            role_refined = role_refined.replace("I am", "You are")
        else:
            role_refined = f"You are a {role_refined}"
    
    # Remove redundant phrases
    role_refined = re.sub(r"You are a You are a", "You are a", role_refined)
    role_refined = re.sub(r"You are a As a", "You are a", role_refined)
    
    # Ensure first letter is capitalized
    role_refined = role_refined[0].upper() + role_refined[1:]
    
    # Enhance context with domain knowledge
    context_enhanced = context.strip()
    additional_context = []
    
    # Check for ISO-related keywords
    for keyword, info in domain_knowledge.items():
        if keyword in combined_text:
            additional_context.append(info.get("context_add", ""))
            
            # Add more specific information for ISO 22301 if relevant
            if keyword == "iso 22301" and "study" in task_clean:
                additional_context.append("An effective study plan should cover the standard's structure, key principles, implementation steps, and certification process.")
    
    # Add the enhanced context if we have any
    if additional_context:
        if context_enhanced and not context_enhanced.endswith(('.', '!', '?')):
            context_enhanced += '.'
        context_enhanced += " " + " ".join(additional_context)
    
    # Enhance task with specifics
    task_enhanced = task.strip()
    
    # Add specific enhancements for study plans
    if "study plan" in task_clean and "iso 22301" in combined_text:
        if not task_enhanced.endswith(('.', '!', '?')):
            task_enhanced += '.'
        task_enhanced += " The plan should include daily learning objectives, key concepts, practical exercises, and assessment methods. It should be structured to provide a comprehensive understanding of Business Continuity Management principles and ISO 22301 requirements."
    
    # Create the final enhanced prompt
    prompt = f"""{role_refined},

Context:
{context_enhanced}

Task:
{task_enhanced}

Please provide a detailed and structured response that addresses the task comprehensively. Include practical examples, implementation tips, and best practices where relevant. If you need any clarification or additional information, please ask specific questions.

The response should be well-organized with clear headings, bullet points where appropriate, and a logical flow of information."""

    return prompt.strip()

def main():
    st.set_page_config(page_title="AI Prompt Generator", layout="wide")
    
    st.title("AI Prompt Generator")
    st.write("Generate enhanced, intelligent prompts for AI models based on role, context, and task.")
    
    # Initialize session state for API key validation and prompt storage
    if 'api_key_valid' not in st.session_state:
        st.session_state.api_key_valid = False
    if 'generated_prompt' not in st.session_state:
        st.session_state.generated_prompt = ""
    
    # API Key input section
    with st.container():
        st.subheader("API Key Validation")
        api_key = st.text_input("Enter your OpenAI API Key", type="password", help="Your API key will not be stored")
        
        # Check if there's an API key in environment variables
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key and not api_key:
            st.info("Using API key from environment variables. You can override it by entering a new key above.")
            api_key = env_api_key
            
        # Validate API key only when the button is clicked
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Validate API Key"):
                if not api_key:
                    st.error("Please enter an API key")
                else:
                    with st.spinner("Validating API Key..."):
                        st.session_state.api_key_valid = validate_api_key(api_key)
                    
                    if st.session_state.api_key_valid:
                        st.success("API Key is valid!")
                    else:
                        st.error("Invalid API Key. Please check and try again.")
    
    # Prompt creation section
    st.write("---")
    st.subheader("Create Your Prompt")
    
    # User inputs
    role = st.text_area("Role", 
                       placeholder="Describe the role that the AI should assume (e.g., 'ISO Consultant')")
    
    context = st.text_area("Context/Background", 
                          placeholder="Provide relevant background information or context")
    
    task = st.text_area("Task", 
                       placeholder="Specify the task or question you want the AI to address")
    
    # Generate prompt button
    if st.button("Generate Enhanced Prompt"):
        if not (role and context and task):
            st.warning("Please fill in all fields")
        else:
            st.session_state.generated_prompt = enhance_prompt(role, context, task)
            
            # Display the generated prompt
            st.write("---")
            st.subheader("Enhanced Prompt")
            st.code(st.session_state.generated_prompt, language="markdown")
            
            # Copy button
            st.markdown("""
            <div style="text-align: right;">
                <button onclick="navigator.clipboard.writeText(document.querySelector('code').innerText); alert('Copied to clipboard!');" class="css-1x8cf1d edgvbvh10">Copy to clipboard</button>
            </div>
            """, unsafe_allow_html=True)
    
    # OpenAI testing section
    if st.session_state.generated_prompt and ((api_key and st.session_state.api_key_valid) or env_api_key):
        st.write("---")
        st.subheader("Test with OpenAI")
        if st.button("Send to OpenAI for testing", key="test_openai"):
            with st.spinner("Getting response from OpenAI..."):
                try:
                    client = openai.OpenAI(api_key=api_key or env_api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": st.session_state.generated_prompt}
                        ]
                    )
                    st.write("### OpenAI Response")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error when calling OpenAI: {str(e)}")

if __name__ == "__main__":
    main()