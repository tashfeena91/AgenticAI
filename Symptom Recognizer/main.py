
import os
from dotenv import load_dotenv
import json
from agents.symptom_interpreter import SymptomInterpreterAgent
from agents.condition_mapper import ConditionMapperAgent
from agents.doctor_note import DoctorNoteAgent
from crewai import Crew, Task

# Load environment variables
load_dotenv()

# Get API keys from environment variables
LANGFUSE_SECRET_KEY = os.environ.get('Langfuse_secretkey')
LANGFUSE_PUBLIC_KEY = os.environ.get('Langfuse_publickey')
GROQ_API_KEY = os.environ.get('Groq_key')
OPENAI_API_KEY = os.environ.get('OpenAI_key')

# Verify keys are loaded
if not all([LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, GROQ_API_KEY]):
    print("Warning: Some API keys are missing from environment variables")
    print(f"LANGFUSE_SECRET_KEY: {'✓' if LANGFUSE_SECRET_KEY else '✗'}")
    print(f"LANGFUSE_PUBLIC_KEY: {'✓' if LANGFUSE_PUBLIC_KEY else '✗'}")
    print(f"GROQ_API_KEY: {'✓' if GROQ_API_KEY else '✗'}")
    exit(1)
else:
    print("All API keys loaded successfully!")

class SymptomCheckerCrew:
    def __init__(self):
        """Initialize the Symptom Checker Crew with all agents"""
        self.symptom_interpreter = SymptomInterpreterAgent(
            GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
        )
        self.condition_mapper = ConditionMapperAgent(
            GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
        )
        self.doctor_note_agent = DoctorNoteAgent(
            GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
        )
    
    def process_symptoms(self, user_input):
        """Process user symptoms through the entire agent pipeline"""
        print(f"\n{'='*50}")
        print("SYMPTOM CHECKER & DOCTOR PREP BOT")
        print(f"{'='*50}")
        
        try:
            # Step 1: Interpret symptoms
            print("\n🔍 Step 1: Interpreting symptoms...")
            structured_symptoms = self.symptom_interpreter.process_symptoms(user_input)
            print("✓ Symptoms interpreted and structured")
            
            # Step 2: Map to potential conditions
            print("\n🗺️  Step 2: Mapping to potential areas of concern...")
            mapped_conditions = self.condition_mapper.map_conditions(structured_symptoms)
            print("✓ Potential areas identified")
            
            # Step 3: Create doctor note
            print("\n📋 Step 3: Creating doctor visit summary...")
            doctor_note = self.doctor_note_agent.create_doctor_note(
                structured_symptoms, mapped_conditions
            )
            print("✓ Doctor visit summary created")
            
            # Display results
            self.display_results(structured_symptoms, mapped_conditions, doctor_note)
            
            return {
                "structured_symptoms": structured_symptoms,
                "mapped_conditions": mapped_conditions,
                "doctor_note": doctor_note
            }
            
        except Exception as e:
            print(f"❌ Error in processing: {str(e)}")
            return {"error": str(e)}
    
    def display_results(self, symptoms, conditions, note):
        """Display the results in a formatted way"""
        print(f"\n{'='*50}")
        print("RESULTS SUMMARY")
        print(f"{'='*50}")
        
        print("\n📊 STRUCTURED SYMPTOMS:")
        print("-" * 30)
        try:
            if isinstance(symptoms, str):
                symptoms_json = json.loads(symptoms)
                for key, value in symptoms_json.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print(symptoms)
        except:
            print(symptoms)
        
        print("\n🏥 POTENTIAL AREAS OF CONCERN:")
        print("-" * 35)
        try:
            if isinstance(conditions, str):
                conditions_json = json.loads(conditions)
                for key, value in conditions_json.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print(conditions)
        except:
            print(conditions)
        
        print("\n📋 DOCTOR VISIT SUMMARY:")
        print("-" * 30)
        try:
            if isinstance(note, str):
                note_json = json.loads(note)
                if 'readable_format' in note_json:
                    print(note_json['readable_format'])
                else:
                    print(note)
            else:
                print(note)
        except:
            print(note)

def main():
    """Main application entry point"""
    crew = SymptomCheckerCrew()
    
    print("Welcome to the Symptom Checker & Doctor Prep Bot!")
    print("This tool helps you organize your symptoms for your doctor visit.")
    print("\nIMPORTANT: This is NOT a diagnostic tool. Always consult healthcare professionals.")
    
    while True:
        print(f"\n{'='*50}")
        user_input = input("\nDescribe your symptoms (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thank you for using Symptom Checker. Take care!")
            break
        
        if not user_input:
            print("Please provide a symptom description.")
            continue
        
        # Process the symptoms
        results = crew.process_symptoms(user_input)
        
        # Ask if user wants to continue
        continue_choice = input("\nWould you like to analyze more symptoms? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break
    
    print("\nRemember to share your summary with your healthcare provider!")

if __name__ == "__main__":
    main()
