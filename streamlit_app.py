import streamlit as st
import os
from dotenv import load_dotenv
import json
from agents.symptom_interpreter import SymptomInterpreterAgent
from agents.condition_mapper import ConditionMapperAgent
from agents.doctor_note import DoctorNoteAgent

# Load environment variables
load_dotenv()

# Get API keys from environment variables
LANGFUSE_SECRET_KEY = os.environ.get('Langfuse_secretkey')
LANGFUSE_PUBLIC_KEY = os.environ.get('Langfuse_publickey')
GROQ_API_KEY = os.environ.get('Groq_key')
OPENAI_API_KEY = os.environ.get('OpenAI_key')

# Configure Streamlit page
st.set_page_config(
    page_title="Symptom Checker & Doctor Prep Bot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

@st.cache_resource
def initialize_agents():
    """Initialize the agents (cached for performance)"""
    if not all([LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, GROQ_API_KEY]):
        st.error("⚠️ Missing API keys. Please check your environment variables.")
        st.stop()
    
    symptom_interpreter = SymptomInterpreterAgent(
        GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
    )
    condition_mapper = ConditionMapperAgent(
        GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
    )
    doctor_note_agent = DoctorNoteAgent(
        GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
    )
    
    return symptom_interpreter, condition_mapper, doctor_note_agent

def process_symptoms(user_input, symptom_interpreter, condition_mapper, doctor_note_agent):
    """Process user symptoms through the entire agent pipeline"""
    try:
        # Step 1: Interpret symptoms
        structured_symptoms = symptom_interpreter.process_symptoms(user_input)
        
        # Step 2: Map to potential conditions
        mapped_conditions = condition_mapper.map_conditions(structured_symptoms)
        
        # Step 3: Create doctor note
        doctor_note = doctor_note_agent.create_doctor_note(
            structured_symptoms, mapped_conditions
        )
        
        return {
            "structured_symptoms": structured_symptoms,
            "mapped_conditions": mapped_conditions,
            "doctor_note": doctor_note,
            "success": True
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

def parse_json_safely(json_string):
    """Safely parse JSON from agent responses"""
    try:
        if isinstance(json_string, str):
            # Remove markdown code blocks if present
            if '```json' in json_string:
                json_string = json_string.split('```json')[1].split('```')[0].strip()
            elif '```' in json_string:
                json_string = json_string.split('```')[1].split('```')[0].strip()
            
            return json.loads(json_string)
        return json_string
    except:
        return json_string

def display_results(results):
    """Display the results in a formatted way"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Structured Symptoms")
        symptoms = parse_json_safely(results['structured_symptoms'])
        if isinstance(symptoms, dict):
            for key, value in symptoms.items():
                if value:  # Only show non-empty values
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.write(symptoms)
        
        st.subheader("🏥 Medical Considerations")
        conditions = parse_json_safely(results['mapped_conditions'])
        if isinstance(conditions, dict):
            # Priority display for key medical information
            priority_fields = ['urgency_level', 'probable_conditions', 'suggested_tests', 'doctor_specialties']
            
            for key in priority_fields:
                if key in conditions and conditions[key]:
                    if key == 'urgency_level':
                        color = {'low': 'green', 'medium': 'orange', 'high': 'red'}.get(str(conditions[key]).lower(), 'blue')
                        st.write(f"**{key.replace('_', ' ').title()}:** :{color}[{conditions[key]}]")
                    elif key == 'probable_conditions':
                        st.write(f"**🔍 Conditions to Discuss:**")
                        if isinstance(conditions[key], list):
                            for condition in conditions[key]:
                                st.write(f"  • {condition}")
                        else:
                            st.write(f"  {conditions[key]}")
                    elif key == 'suggested_tests':
                        st.write(f"**🧪 Tests to Consider:**")
                        if isinstance(conditions[key], list):
                            for test in conditions[key]:
                                st.write(f"  • {test}")
                        else:
                            st.write(f"  {conditions[key]}")
                    else:
                        st.write(f"**{key.replace('_', ' ').title()}:** {conditions[key]}")
            
            # Show other fields
            for key, value in conditions.items():
                if key not in priority_fields and value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.write(conditions)
    
    with col2:
        st.subheader("📋 Doctor Visit Summary")
        note = parse_json_safely(results['doctor_note'])
        if isinstance(note, dict) and 'readable_format' in note:
            st.write(note['readable_format'])
            
            # Show JSON format in an expandable section
            with st.expander("View Detailed JSON Summary"):
                if 'json_format' in note:
                    st.json(note['json_format'])
        else:
            st.write(note)
        
        # Download button for the summary
        if isinstance(note, dict) and 'readable_format' in note:
            summary_text = f"""
SYMPTOM CHECKER & DOCTOR PREP BOT - VISIT SUMMARY
Generated on: {note.get('json_format', {}).get('preparation_date', 'N/A')}

{note['readable_format']}

STRUCTURED SYMPTOMS:
{json.dumps(symptoms, indent=2) if isinstance(symptoms, dict) else symptoms}

POTENTIAL AREAS OF CONCERN:
{json.dumps(conditions, indent=2) if isinstance(conditions, dict) else conditions}

DISCLAIMER: This is NOT a medical diagnosis. Always consult healthcare professionals.
"""
            st.download_button(
                label="📥 Download Summary",
                data=summary_text,
                file_name="symptom_summary.txt",
                mime="text/plain"
            )

def main():
    """Main Streamlit application"""
    # Header
    st.title("🏥 Symptom Checker & Doctor Prep Bot")
    st.markdown("---")
    
    # Important disclaimer
    st.warning("""
    **⚠️ IMPORTANT DISCLAIMER:** 
    This tool is NOT a diagnostic tool and does not replace professional medical advice. 
    Always consult healthcare professionals for proper diagnosis and treatment.
    """)
    
    # Sidebar
    st.sidebar.title("About This Tool")
    st.sidebar.info("""
    This AI-powered tool helps you:
    - Organize your symptoms
    - Identify potential areas of concern
    - Prepare for your doctor visit
    - Generate a summary to share with healthcare providers
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("How It Works")
    st.sidebar.markdown("""
    1. **Symptom Interpretation**: Extracts structured information from your description
    2. **Condition Mapping**: Identifies potential areas of concern (NOT diagnosis)
    3. **Doctor Note Creation**: Generates a professional summary for your visit
    """)
    
    # Initialize agents
    try:
        symptom_interpreter, condition_mapper, doctor_note_agent = initialize_agents()
        st.sidebar.success("✅ System initialized successfully!")
    except Exception as e:
        st.error(f"❌ Failed to initialize: {str(e)}")
        st.stop()
    
    # Main input area
    st.subheader("Describe Your Symptoms")
    
    # Input options
    input_method = st.radio(
        "Choose input method:",
        ["Text Description", "Guided Form"],
        horizontal=True
    )
    
    user_input = ""
    
    if input_method == "Text Description":
        user_input = st.text_area(
            "Describe your symptoms in detail:",
            placeholder="Example: I've been having a headache for 3 days. It gets worse in the afternoon and I feel nauseous...",
            height=150
        )
    else:
        # Guided form
        st.markdown("**Fill out the form below to describe your symptoms:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            main_symptom = st.text_input("Main symptom:")
            duration = st.selectbox("Duration:", ["", "Less than 1 day", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"])
            severity = st.slider("Severity (1-10):", 1, 10, 5)
        
        with col2:
            affected_areas = st.multiselect("Affected body areas:", 
                ["Head", "Neck", "Chest", "Back", "Abdomen", "Arms", "Legs", "Other"])
            triggers = st.text_input("What makes it worse?")
            timing = st.selectbox("When does it occur?", ["", "Morning", "Afternoon", "Evening", "Night", "All day"])
        
        associated_symptoms = st.text_area("Other symptoms:")
        
        if main_symptom:
            user_input = f"""
            Main symptom: {main_symptom}
            Duration: {duration}
            Severity: {severity}/10
            Affected areas: {', '.join(affected_areas)}
            Triggers: {triggers}
            Timing: {timing}
            Associated symptoms: {associated_symptoms}
            """
    
    # Process button
    if st.button("🔍 Analyze Symptoms", type="primary", disabled=not user_input.strip()):
        if user_input.strip():
            st.session_state.processing = True
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process symptoms
            status_text.text("🔍 Step 1: Interpreting symptoms...")
            progress_bar.progress(33)
            
            results = process_symptoms(user_input, symptom_interpreter, condition_mapper, doctor_note_agent)
            
            status_text.text("🗺️ Step 2: Mapping to potential areas...")
            progress_bar.progress(66)
            
            status_text.text("📋 Step 3: Creating doctor visit summary...")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            if results['success']:
                st.session_state.results = results
                st.success("✅ Analysis complete!")
            else:
                st.error(f"❌ Error: {results.get('error', 'Unknown error occurred')}")
            
            st.session_state.processing = False
    
    # Display results
    if st.session_state.results and st.session_state.results['success']:
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        display_results(st.session_state.results)
        
        # Clear results button
        if st.button("🔄 Start New Analysis"):
            st.session_state.results = None
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("*Remember to share your summary with your healthcare provider!*")

if __name__ == "__main__":
    main()
