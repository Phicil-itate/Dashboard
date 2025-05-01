import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if Supabase credentials are set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are not set in environment variables. Please set SUPABASE_URL and SUPABASE_KEY.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_patient_interview_table():
    """Create the Patient_interview table in Supabase if it doesn't exist"""
    
    # SQL for creating the table as specified in the requirements
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS "Patient_interview"(
      "PatientID" TEXT,
      "Age" INTEGER,
      "Location" TEXT,
      "Gender" TEXT,
      "DiabetesType" TEXT,
      "YearsSinceDiagnosis" INTEGER,
      "TreatmentPlan" TEXT,
      "HbA1c" FLOAT,
      "BloodPressure" TEXT,
      "BMI" FLOAT,
      "Diet" TEXT,
      "Exercise" TEXT,
      "StressLevel" TEXT,
      "TechUsage" TEXT,
      "MainChallenges" TEXT,
      "Goals" TEXT,
      "Sentiment" TEXT,
      "UserQuote" TEXT,
      "Q1_MemorableExperience" TEXT,
      "Q2_ToolSelectionFactors" TEXT,
      "Q3_SupportSatisfaction" TEXT,
      "Q4_MotivationFromTech" TEXT,
      "Q5_CostFrustrations" TEXT,
      "Q6_DailyIntegration" TEXT,
      "Q7_ConfidenceMoment" TEXT,
      "Q8_DesiredFeatures" TEXT,
      "Q9_TechIssuesImpact" TEXT,
      "Q10_EmotionalImpact" TEXT,
      "Q11_PrivacyConcerns" TEXT,
      "Q12_AdviceToStartups" TEXT,
      "Q13_ProviderCommunication" TEXT,
      "Q14_PeerSupportExperience" TEXT,
      "Notes" TEXT
    );
    """
    
    print("Creating Patient_interview table if it doesn't exist...")
    
    try:
        # Check if table exists by trying to select a row
        response = supabase.table("Patient_interview").select("*", count="exact").limit(1).execute()
        print(f"Table already exists, found {response.count} rows")
        return True
    except Exception as e:
        print(f"Error checking table existence: {e}")
        
        # Try to create the table
        try:
            # Note: Direct SQL execution might require special permissions in Supabase
            # This might need to be done manually in the Supabase dashboard
            print("Attempting to create table...")
            print("If this fails, please create the table manually using the following SQL:")
            print(create_table_sql)
            return False
        except Exception as create_err:
            print(f"Error creating table: {create_err}")
            return False

def clean_and_transform_data(csv_path):
    """Load and preprocess the CSV data"""
    
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Rename the question columns to match the database schema
    print("Mapping columns to match database schema...")
    column_mapping = {
        "Q1 Can you share a memorable experience—good or bad—that you've had with a health tech solution for managing your diabetes?": "Q1_MemorableExperience",
        "Q2 When choosing a digital health tool, what factors are most important to you, and why?": "Q2_ToolSelectionFactors",
        "Q3 How do you feel about the level of support and guidance provided by health tech solutions, such as tutorials or customer service?": "Q3_SupportSatisfaction", 
        "Q4 In what ways, if any, do digital health tools help you stay motivated or engaged in your diabetes management?": "Q4_MotivationFromTech",
        "Q5 What challenges or frustrations have you encountered regarding the cost or insurance coverage of health tech solutions?": "Q5_CostFrustrations",
        "Q6 Could you describe how you integrate health technology into your daily routine, and what makes this process easy or difficult?": "Q6_DailyIntegration",
        "Q7 Tell me about a moment when you felt especially confident or in control of your health due to a digital tool. What made that experience stand out?": "Q7_ConfidenceMoment",
        "Q8 What improvements or additional features would you like to see in the health tech tools you currently use?": "Q8_DesiredFeatures",
        "Q9 How do you typically handle technical difficulties or glitches in the health tech tools you use, and how do these issues affect your overall experience?": "Q9_TechIssuesImpact",
        "Q10 In your experience, how do digital health solutions impact your emotional well-being or stress levels?": "Q10_EmotionalImpact",
        "Q11 Could you share your thoughts on data privacy and security when using digital platforms to manage your health?": "Q11_PrivacyConcerns",
        "Q12 If you had the opportunity to advise a new health tech startup, what would you tell them about meeting the needs of patients with diabetes?": "Q12_AdviceToStartups",
        "Q13 How has communication with healthcare professionals changed for you, if at all, since you began using digital health tools?": "Q13_ProviderCommunication",
        "Q14 Have you found any technology-based diabetes support communities or peer groups, and how have they influenced your day-to-day management?": "Q14_PeerSupportExperience"
    }
    
    # Make a copy of column_mapping keys for safe iteration
    # This fixes the "dictionary keys changed during iteration" error
    updated_mapping = {}
    for old_col in list(column_mapping.keys()):
        if old_col not in df.columns:
            print(f"Warning: Column '{old_col}' not found in CSV file")
            # Try to find a similar column (for example if quotes are different)
            for csv_col in df.columns:
                if csv_col.startswith(old_col[:10]):  # Check first 10 chars
                    print(f"Found similar column: '{csv_col}'")
                    # Add the new mapping instead of modifying during iteration
                    updated_mapping[csv_col] = column_mapping[old_col]
                    break
        else:
            # Keep the original mapping
            updated_mapping[old_col] = column_mapping[old_col]
    
    # Replace the original mapping with the updated one
    column_mapping = updated_mapping
    
    # Print column names before renaming for debugging
    print("Original columns:")
    for col in df.columns:
        if col.startswith('Q') and len(col) > 2:
            print(f"- {col}")
    
    # Rename columns
    df = df.rename(columns=column_mapping)
    
    # Ensure all expected columns exist after renaming
    for new_col in ["Q1_MemorableExperience", "Q2_ToolSelectionFactors", "Q3_SupportSatisfaction", 
                    "Q4_MotivationFromTech", "Q5_CostFrustrations", "Q6_DailyIntegration", 
                    "Q7_ConfidenceMoment", "Q8_DesiredFeatures", "Q9_TechIssuesImpact", 
                    "Q10_EmotionalImpact", "Q11_PrivacyConcerns", "Q12_AdviceToStartups", 
                    "Q13_ProviderCommunication", "Q14_PeerSupportExperience"]:
        if new_col not in df.columns:
            print(f"Warning: Expected column '{new_col}' not found after renaming")
    
    # Print column names after renaming for debugging
    print("Renamed columns:")
    for col in df.columns:
        if col.startswith('Q') and len(col) > 2:
            print(f"- {col}")
    
    # Convert data types to match schema and handle NaN values
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(0).astype(int)
    df["YearsSinceDiagnosis"] = pd.to_numeric(df["YearsSinceDiagnosis"], errors="coerce").fillna(0).astype(int)
    df["HbA1c"] = pd.to_numeric(df["HbA1c"], errors="coerce").fillna(0.0)
    df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce").fillna(0.0)
    
    # Convert all NaN values to appropriate empty values based on column type
    # This fixes the "Token "NaN" is invalid" error
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # For numeric columns, replace NaN with 0
            df[col] = df[col].fillna(0)
        else:
            # For text/object columns, replace NaN with empty string
            df[col] = df[col].fillna("")
    
    # Force selection of only the columns needed for the table
    # This ensures no extra columns are sent to Supabase
    required_columns = [
        "PatientID", "Age", "Location", "Gender", "DiabetesType", 
        "YearsSinceDiagnosis", "TreatmentPlan", "HbA1c", "BloodPressure", 
        "BMI", "Diet", "Exercise", "StressLevel", "TechUsage", 
        "MainChallenges", "Goals", "Sentiment", "UserQuote", 
        "Q1_MemorableExperience", "Q2_ToolSelectionFactors", "Q3_SupportSatisfaction", 
        "Q4_MotivationFromTech", "Q5_CostFrustrations", "Q6_DailyIntegration", 
        "Q7_ConfidenceMoment", "Q8_DesiredFeatures", "Q9_TechIssuesImpact", 
        "Q10_EmotionalImpact", "Q11_PrivacyConcerns", "Q12_AdviceToStartups", 
        "Q13_ProviderCommunication", "Q14_PeerSupportExperience", "Notes"
    ]
    
    # Check which required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Warning: Missing columns: {missing_columns}")
        # Add missing columns with empty values
        for col in missing_columns:
            df[col] = ""
    
    # Select only required columns in the right order
    df = df[required_columns]
    
    print(f"Processed {len(df)} rows of data")
    return df

def insert_data_in_batches(df, table_name, batch_size=25):
    """Insert data into Supabase in batches, with upsert logic to handle duplicates"""
    
    # Convert DataFrame to list of dictionaries for insertion
    records = df.to_dict(orient="records")
    total_batches = (len(records) - 1) // batch_size + 1
    
    print(f"Upserting {len(records)} records in {total_batches} batches...")
    
    successful_operations = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            # Use upsert operation instead of insert
            # This will update existing rows (based on PatientID) or insert new ones
            response = supabase.table(table_name).upsert(
                batch,
                on_conflict="PatientID"  # Assuming PatientID is the primary/unique key
            ).execute()
            successful_operations += len(batch)
            print(f"Upserted batch {i//batch_size + 1}/{total_batches} ({successful_operations}/{len(records)} records)")
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
        except Exception as e:
            print(f"Error upserting batch {i//batch_size + 1}: {e}")
            # Print the first record from the batch to debug
            if batch:
                print(f"Sample record keys: {list(batch[0].keys())[:5]}...")
                print(f"Sample record PatientID: {batch[0].get('PatientID', 'No ID found')}")
    
    print(f"Data upsert complete: {successful_operations}/{len(records)} records successfully processed")
    return successful_operations

def ingest_patient_data():
    """Main function to ingest patient data from CSV to Supabase"""
    
    csv_path = "./csv/patient.csv"
    table_name = "Patient_interview"
    
    print("Starting patient data ingestion pipeline...")
    
    # Step 1: Create table if it doesn't exist
    table_exists = create_patient_interview_table()
    
    # Step 2: Transform the data
    transformed_data = clean_and_transform_data(csv_path)
    
    # Step 3: Insert the data
    if table_exists or input("Table may not exist. Try inserting data anyway? (y/n): ").lower() == 'y':
        insert_data_in_batches(transformed_data, table_name)
    else:
        print("Aborting ingestion. Please create the table manually and run this script again.")

if __name__ == "__main__":
    ingest_patient_data()