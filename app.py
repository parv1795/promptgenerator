import streamlit as st
import openai
import time
import re
import random

def validate_api_key(api_key):
    """Validate the OpenAI API key by making a small test request."""
    if not api_key or len(api_key) < 30:  # Basic format check
        return False
    
    openai.api_key = api_key
    try:
        # Make a minimal API call to check if the key works
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        st.error(f"API Key validation failed: {str(e)}")
        return False

def transform_prompt(role, context, task):
    """Transform the inputs into a completely enhanced prompt."""
    
    # Extract key information from inputs
    role_lower = role.lower()
    context_lower = context.lower()
    task_lower = task.lower()
    
    # Identify domain/expertise
    domains = {
        "develop": "software development",
        "program": "programming",
        "code": "coding",
        "tech": "technology",
        "market": "marketing",
        "business": "business strategy",
        "write": "content creation",
        "content": "content strategy",
        "data": "data analysis",
        "analy": "analytics",
        "research": "research",
        "design": "design",
        "product": "product management",
        "teach": "education",
        "learn": "learning",
        "consult": "consulting"
    }
    
    identified_domain = None
    for key, domain in domains.items():
        if key in role_lower or key in task_lower:
            identified_domain = domain
            break
    
    if not identified_domain:
        identified_domain = "professional consulting"
    
    # Determine experience level
    experience_levels = ["expert", "senior", "experienced", "specialist", "professional"]
    experience_level = next((level for level in experience_levels if level in role_lower), "experienced")
    
    # Determine if this is a learning/teaching scenario
    is_learning = any(term in context_lower for term in ["learn", "beginner", "newbie", "starting", "new to"])
    
    # Determine project type
    project_types = {
        "app": "application development",
        "website": "web development",
        "platform": "platform development",
        "tool": "tool creation",
        "dashboard": "dashboard development",
        "script": "script development",
        "system": "system design",
        "framework": "framework development",
        "api": "API development",
        "database": "database solution",
        "automation": "automation solution",
        "ai": "AI solution",
        "ml": "machine learning solution",
        "analytics": "analytics solution"
    }
    
    project_type = None
    for key, proj_type in project_types.items():
        if key in task_lower:
            project_type = proj_type
            break
    
    if not project_type:
        project_type = "solution"
    
    # Determine technologies/tools mentioned
    technologies = {
        "python": "Python",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "react": "React",
        "node": "Node.js",
        "flask": "Flask",
        "django": "Django",
        "streamlit": "Streamlit",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "pandas": "pandas",
        "numpy": "NumPy",
        "sql": "SQL",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "Google Cloud",
        "api": "API"
    }
    
    tech_stack = []
    all_text = f"{role_lower} {context_lower} {task_lower}"
    for key, tech in technologies.items():
        if key in all_text:
            tech_stack.append(tech)
    
    # Generate a compelling title
    titles = [
        f"Creating a {project_type.title()} for {identified_domain.title()}",
        f"Developing a Custom {project_type.title()} Solution",
        f"{identified_domain.title()} {project_type.title()} Project",
        f"Building a Specialized {project_type.title()} for {identified_domain.title()}"
    ]
    
    title = random.choice(titles)
    
    # Generate persona
    personas = [
        f"As an {experience_level} {identified_domain} specialist with a focus on {', '.join(tech_stack) if tech_stack else 'cutting-edge technologies'}",
        f"Taking the perspective of a seasoned {identified_domain} professional with deep expertise in {', '.join(tech_stack) if tech_stack else 'modern development practices'}",
        f"Working as a {experience_level} developer specializing in {identified_domain} and {', '.join(tech_stack) if tech_stack else 'innovative solutions'}"
    ]
    
    persona = random.choice(personas)
    
    # Generate project description
    task_description = task.strip().rstrip('.')
    if not task_description.lower().startswith(("create", "develop", "build", "design", "implement")):
        task_description = f"develop {task_description}"
    
    # Generate objectives
    objectives = []
    
    if is_learning:
        objectives.append("Create a solution that serves as both a functional tool and a learning resource")
        objectives.append("Provide clear code structure with comments that explain the implementation")
        objectives.append("Include step-by-step setup instructions for beginners")
    else:
        objectives.append(f"Deliver a high-quality {project_type} that meets industry standards")
        objectives.append("Ensure the solution is robust, scalable, and maintainable")
        objectives.append("Optimize for performance and user experience")
    
    if "streamlit" in all_text:
        objectives.append("Develop an intuitive Streamlit interface with responsive design")
        objectives.append("Implement effective state management for a seamless user experience")
    
    if "api" in all_text:
        objectives.append("Create secure API integration with proper validation and error handling")
    
    # Generate requirements
    requirements = []
    
    if "app" in all_text or "application" in all_text:
        requirements.append("Intuitive user interface with clear navigation and feedback")
        requirements.append("Responsive design that works across different devices")
        requirements.append("Proper error handling and user guidance")
    
    if "python" in all_text:
        requirements.append("Clean, well-organized Python code following PEP 8 standards")
        requirements.append("Modular architecture with separation of concerns")
        requirements.append("Comprehensive documentation and inline comments")
    
    if "streamlit" in all_text:
        requirements.append("Efficient Streamlit components and layouts")
        requirements.append("State management for user session data")
        requirements.append("Properly structured app with clear sections and navigation")
    
    # Generate final prompt
    prompt = f"""# {title}

{persona}, I need your expertise to {task_description}.

## Project Context
I'm {context.strip().rstrip('.')}. This project is intended to {task_description.lower()} that will help me {context.strip().lower()}.

## Key Objectives
{'. '.join(objectives)}

## Technical Requirements
The solution should include:
- {'. '.join(requirements)}
- Proper security measures including input validation and data protection
- Clean, maintainable code with appropriate documentation
- Scalable architecture that can accommodate future enhancements

## Deliverables
Please provide:
1. A complete, working solution with all necessary code and components
2. Clear explanation of the solution architecture and key design decisions
3. Step-by-step instructions for setting up and running the application
4. Recommendations for future improvements and expansions

## Additional Considerations
- The solution should be accessible to users with varying levels of technical expertise
- Include best practices for code organization and project structure
- Consider performance optimization for a smooth user experience
- Address potential security concerns and implementation challenges

If you need any clarification or additional information about my requirements, technical background, or project goals, please let me know.
"""
    
    return prompt

# Set page config
st.set_page_config(page_title="Smart Prompt Enhancer", layout="wide")

# App title and description
st.title("🚀 Smart Prompt Enhancer")
st.markdown("""
This app transforms your basic prompt concepts into sophisticated, professionally crafted prompts
that will generate superior AI responses. Enter your OpenAI API key to get started.
""")

# API Key input
api_key = st.text_input("OpenAI API Key:", type="password", help="Your key will be used only for validation and won't be stored.")

# Validate key when provided
key_valid = False
if api_key:
    with st.spinner("Validating API key..."):
        key_valid = validate_api_key(api_key)
    
    if key_valid:
        st.success("✅ API key is valid!")
    else:
        st.error("❌ Invalid API key. Please check and try again.")

# Only show the prompt builder if key is valid
if key_valid:
    st.markdown("---")
    st.header("Define Your Prompt Components")
    
    # Prompt components
    role = st.text_area(
        "Role:",
        placeholder="Who should the AI act as? (e.g., 'Python Developer' or 'Marketing Specialist')",
        help="The expertise or perspective you want the AI to adopt."
    )
    
    context = st.text_area(
        "Context/Background:",
        placeholder="Your situation or relevant details (e.g., 'Beginner looking to build my first app')",
        help="Your background, situation, or relevant context."
    )
    
    task = st.text_area(
        "Task:",
        placeholder="What do you want the AI to do? (e.g., 'Create a data visualization app')",
        help="The specific outcome you want from the AI."
    )
    
    # Generate button
    if st.button("Generate Enhanced Prompt"):
        if not (role and context and task):
            st.warning("Please fill in all three prompt components.")
        else:
            with st.spinner("Creating your enhanced prompt..."):
                # Add a small delay for UX
                time.sleep(0.8)
                transformed_prompt = transform_prompt(role, context, task)
                
                # Display the enhanced prompt
                st.markdown("## 🎯 Your Enhanced Prompt")
                st.text_area("Copy this prompt to use with your preferred AI:", transformed_prompt, height=400)
                
                # Copy button functionality
                st.markdown("Click the clipboard icon in the top-right of the text box to copy the prompt.")
                
                # Add example usage
                with st.expander("How to use your enhanced prompt"):
                    st.markdown("""
                    ### Getting the best results:
                    
                    1. **Copy the entire prompt** using the clipboard icon
                    2. **Paste it directly** into your favorite AI tool (ChatGPT, Claude, etc.)
                    3. **Review the response** and iterate if needed
                    
                    This enhanced prompt is designed to elicit detailed, actionable responses tailored to your specific needs.
                    """)
else:
    st.info("Please enter a valid OpenAI API key to continue.")

# Footer
st.markdown("---")
st.markdown("*This app only validates your API key but doesn't store it or use it beyond validation.*")
